import os
import json
from sqlalchemy.orm import Session
from models import Questao, RespostaLog, AlunoProgresso, Conceito
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

def gerar_resumo_ia(db: Session, conceito: Conceito):
    prompt = f"""Você é o autor de um livro didático de matemática muito moderno.
Escreva um resumo teórico sobre o conceito: "{conceito.nome}".

O resumo deve ser formatado em Markdown e conter as seguintes seções (usando títulos ##):
1. **O que é?**: Uma definição simples e direta do conceito.
2. **Fórmulas / Regras**: As principais fórmulas matemáticas, se aplicável, ou as regras básicas.
3. **Exemplo Prático**: Um passo a passo super didático resolvendo um problema clássico.
4. **Dica de Ouro**: Um parágrafo rápido com uma dica essencial para não errar.

Use formatação bonita (negrito, listas, blocos de código para matemática se necessário). Mantenha tudo no máximo em 400 palavras para o aluno não ficar com preguiça. Retorne APENAS o texto em Markdown.
"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: return "Erro: Chave de API não configurada."
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        texto = response.text.strip()
        return texto
    except Exception as e:
        print(f"Erro na IA ao gerar resumo: {e}")
        return "Desculpe, o sistema tutor está offline para buscar a teoria no momento. Tente novamente mais tarde."

def gerar_questao_ia(db: Session, conceito, dificuldade: int):
    prompt = f"""Você é um professor de matemática especialista na construção de itens de múltipla escolha ou resposta direta.
Sua missão é criar UMA (1) única questão de álgebra sobre o tema '{conceito.nome}'.
O nível de dificuldade deve ser {dificuldade} (em uma escala de 1 a 4). 
- Nível 1: Introdução ao conceito, números pequenos.
- Nível 4: Desafio avançado, mais abstração ou números complexos.

O resultado/gabarito final DEVE ser um número exato (inteiro ou decimal com precisão de até 2 casas).
Por favor, responda APENAS com um objeto JSON válido, contendo "enunciado" e "gabarito", sem markdown.
Exemplo: {{"enunciado": "Se 2x = 10, qual o valor de x?", "gabarito": 5}}
"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key: return None
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        texto = response.text.strip()
        if texto.startswith("```json"): texto = texto[7:-3]
        elif texto.startswith("```"): texto = texto[3:-3]
        
        dados = json.loads(texto)
        nova_questao = Questao(
            conceito_id=conceito.id,
            enunciado=dados["enunciado"],
            gabarito=float(dados["gabarito"]),
            dificuldade=dificuldade
        )
        db.add(nova_questao)
        db.commit()
        db.refresh(nova_questao)
        return nova_questao
    except Exception as e:
        print(f"Erro na IA ao gerar questao: {e}")
        return None

def selecionar_proxima_questao(db: Session, aluno_id: int, conceito_id: int = None, nivel_maximo: int = None):
    # 1. Definir o conceito alvo
    if conceito_id:
        conceito_alvo = db.query(Conceito).filter(Conceito.id == conceito_id).first()
        if not conceito_alvo: return None
    else:
        desbloqueados = get_conceitos_desbloqueados(db, aluno_id)
        if not desbloqueados: return None
        
        alvo_dict = min(desbloqueados, key=lambda x: x["dominio"])
        conceito_alvo = db.query(Conceito).filter(Conceito.id == alvo_dict["id"]).first()
        if not conceito_alvo: return None
        
    # 2. Definir a Dificuldade Ideal Baseada no Progresso
    progresso = db.query(AlunoProgresso).filter(
        AlunoProgresso.aluno_id == aluno_id,
        AlunoProgresso.conceito_id == conceito_alvo.id
    ).first()
    
    dom = progresso.dominio if progresso else 0.0
    
    dificuldade_ideal = 1
    if dom >= 0.80:
        dificuldade_ideal = 4
    elif dom >= 0.50:
        dificuldade_ideal = 3
    elif dom >= 0.30:
        dificuldade_ideal = 2
        
    if nivel_maximo is not None:
        dificuldade_ideal = min(dificuldade_ideal, nivel_maximo)
        
    # 3. Tentar gerar com a Inteligência Artificial
    questao_escolhida = gerar_questao_ia(db, conceito_alvo, dificuldade_ideal)
    
    # 4. Fallback de Segurança
    if not questao_escolhida:
        questoes_respondidas = [r.questao_id for r in db.query(RespostaLog).filter(RespostaLog.aluno_id == aluno_id).all()]
        filtros = [Questao.conceito_id == conceito_alvo.id]
        if questoes_respondidas:
            filtros.append(Questao.id.not_in(questoes_respondidas))
        if nivel_maximo is not None:
            filtros.append(Questao.dificuldade <= nivel_maximo)
            
        disponiveis = db.query(Questao).filter(*filtros).all()
        if not disponiveis:
            disponiveis = db.query(Questao).filter(Questao.conceito_id == conceito_alvo.id).all()
            
        if disponiveis:
            questao_escolhida = random.choice(disponiveis)
        else:
            return None
            
    return {
        "questao_id": questao_escolhida.id,
        "enunciado": questao_escolhida.enunciado,
        "dificuldade": questao_escolhida.dificuldade,
        "conceito": conceito_alvo.nome,
        "conceito_id": conceito_alvo.id
    }
