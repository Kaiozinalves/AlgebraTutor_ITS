import os
from sqlalchemy.orm import Session
from models import Questao, RespostaLog
import random
from dominio import get_conceitos_desbloqueados
from google import genai

# O python-dotenv será carregado no main.py, então a variável de ambiente estará disponível aqui
def get_ia_feedback(acertou: bool, enunciado: str, gabarito: float):
    
    prompt = f"""Você é um tutor de álgebra para estudantes brasileiros do ensino médio.
O aluno {'acertou' if acertou else 'errou'} a questão: "{enunciado}".
"""
    if acertou:
        prompt += 'Parabéns! Reforce o conceito central em 1 frase curta.'
    else:
        prompt += f'A resposta correta é {gabarito}. IMPORTANTE: NÃO revele a resposta correta no feedback. Explique o conceito em 2 frases simples e dê uma dica de como ele deve pensar para resolver a questão sozinho da próxima vez. APÓS a sua dica, pule uma linha, escreva exatamente a string "|||" e, nas linhas seguintes, forneça a resolução completa passo a passo mostrando matematicamente como chegar ao valor exato {gabarito}.'
        
    prompt += '\nSeja encorajador, direto e use linguagem simples.'
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Chave GEMINI_API_KEY não encontrada no .env")
            
        client = genai.Client(api_key=api_key)
        
        # Usamos o gemini-2.5-flash que é a versão mais moderna e garantida de existir na API nova
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        texto = response.text
        if acertou:
            return texto, None
        else:
            partes = texto.split("|||")
            feedback = partes[0].strip()
            resolucao = partes[1].strip() if len(partes) > 1 else "Resolução detalhada indisponível no momento."
            return feedback, resolucao
    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        if acertou:
            return "Parabéns! Você acertou a questão.", None
        else:
            return "Resposta incorreta. Tente revisar os passos e preste atenção aos sinais e operações! Se precisar, veja o gabarito.", "Resolução não pôde ser gerada devido a erro técnico na IA."

def responder_duvida_aluno(enunciado: str, duvida: str) -> str:
    prompt = f"""Você é um tutor de álgebra para estudantes brasileiros do ensino médio.
O aluno está tentando resolver a seguinte questão: "{enunciado}".
Ele ainda NÃO respondeu a questão e está com a seguinte dúvida: "{duvida}".

Responda à dúvida dele de forma clara, didática e encorajadora. 
IMPORTANTE: NUNCA DÊ A RESPOSTA FINAL DA QUESTÃO EM HIPÓTESE ALGUMA. Apenas explique o conceito, dê dicas matemáticas ou ajude a destravar o passo exato em que ele está em dúvida.
Seja conciso, usando no máximo 2 a 3 parágrafos curtos.
"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Parece que a conexão com o professor falhou (chave ausente). Tente revisar a teoria do módulo!"
            
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Erro na API do Gemini (Chat Dúvida): {e}")
        return "Desculpe, tive um pequeno problema técnico ao processar sua dúvida. Pode tentar de novo ou rever seus passos por enquanto?"

def selecionar_proxima_questao(db: Session, aluno_id: int, conceito_id: int = None):
    # Filtra as questões que o aluno já respondeu
    questoes_respondidas = [
        r.questao_id for r in db.query(RespostaLog).filter(RespostaLog.aluno_id == aluno_id).all()
    ]
    
    if conceito_id:
        from models import Conceito
        c = db.query(Conceito).filter(Conceito.id == conceito_id).first()
        if not c:
            return None
            
        questoes_disponiveis = db.query(Questao).filter(
            Questao.conceito_id == conceito_id,
            Questao.id.not_in(questoes_respondidas) if questoes_respondidas else True
        ).all()
        
        # Se já respondeu todas desse módulo, permite repeti-las na revisão
        if not questoes_disponiveis:
            questoes_disponiveis = db.query(Questao).filter(Questao.conceito_id == conceito_id).all()
            if not questoes_disponiveis:
                return None
                
        questao_escolhida = random.choice(questoes_disponiveis)
        return {
            "questao_id": questao_escolhida.id,
            "enunciado": questao_escolhida.enunciado,
            "dificuldade": questao_escolhida.dificuldade,
            "conceito": c.nome,
            "conceito_id": c.id
        }

    desbloqueados = get_conceitos_desbloqueados(db, aluno_id)
    conceitos_validos = []
    
    for c in desbloqueados:
        questoes_disponiveis = db.query(Questao).filter(
            Questao.conceito_id == c["id"],
            Questao.id.not_in(questoes_respondidas) if questoes_respondidas else True
        ).all()
        
        if questoes_disponiveis:
            conceitos_validos.append({
                "id": c["id"],
                "nome": c["nome"],
                "dominio": c["dominio"],
                "questoes": questoes_disponiveis
            })
            
    if not conceitos_validos:
        return None
        
    # Escolher o de menor domínio
    conceito_escolhido = min(conceitos_validos, key=lambda x: x["dominio"])
    
    # Sortear uma questão
    questao_escolhida = random.choice(conceito_escolhido["questoes"])
    
    return {
        "questao_id": questao_escolhida.id,
        "enunciado": questao_escolhida.enunciado,
        "dificuldade": questao_escolhida.dificuldade,
        "conceito": conceito_escolhido["nome"],
        "conceito_id": conceito_escolhido["id"]
    }
