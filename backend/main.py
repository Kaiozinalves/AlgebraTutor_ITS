from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import math
import datetime

def check_ofensiva_perdida(aluno, db: Session):
    hoje = datetime.date.today()
    if aluno.ultima_ofensiva:
        diff = (hoje - aluno.ultima_ofensiva).days
        if diff > 1:
            aluno.ofensiva_dias = 0
            
    if aluno.ultimo_acesso != hoje:
        aluno.questoes_hoje = 0
        aluno.ultimo_acesso = hoje
        
    db.commit()

from database import engine, Base, get_db
from models import Aluno, RespostaLog, Conceito, AlunoProgresso
from dominio import atualizar_dominio
from pedagogico import selecionar_proxima_questao, get_ia_feedback, responder_duvida_aluno

# Carrega variáveis de ambiente (.env)
load_dotenv()

app = FastAPI(title="ITS Álgebra Básica API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IniciarRequest(BaseModel):
    nome: str

class ResponderRequest(BaseModel):
    nome: str
    questao_id: int
    resposta: float
    usou_dica: bool = False

class DuvidaRequest(BaseModel):
    enunciado: str
    duvida: str

@app.post("/iniciar")
def iniciar_sessao(req: IniciarRequest, db: Session = Depends(get_db)):
    nome = req.nome.strip()
    aluno = db.query(Aluno).filter(Aluno.nome == nome).first()
    
    if not aluno:
        aluno = Aluno(nome=nome)
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        
        # Opcional: inicializar o domínio do aluno no C01 como 0.0 explicitamente
        prog_c1 = AlunoProgresso(aluno_id=aluno.id, conceito_id=1, dominio=0.0)
        db.add(prog_c1)
        db.commit()
        
        return {"nome": aluno.nome, "mensagem": f"Bem-vindo(a), {aluno.nome}! Perfil criado com sucesso."}
    else:
        return {"nome": aluno.nome, "mensagem": f"Bem-vindo(a) de volta, {aluno.nome}!"}

@app.get("/proxima/{nome}")
def obter_proxima_questao(nome: str, conceito_id: Optional[int] = None, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.nome == nome).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    check_ofensiva_perdida(aluno, db)
        
    proxima = selecionar_proxima_questao(db, aluno.id, conceito_id)
    if not proxima:
        return {"mensagem": "parabéns, conteúdo concluído", "ofensiva": aluno.ofensiva_dias}
        
    proxima["ofensiva"] = aluno.ofensiva_dias
    return proxima

@app.post("/responder")
def responder_questao(req: ResponderRequest, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.nome == req.nome).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
        
    questao = db.query(Conceito).join(Conceito.questoes).filter(Conceito.questoes.any(id=req.questao_id)).first().questoes
    questao = next((q for q in questao if q.id == req.questao_id), None)
    
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada.")
        
    # Validar resposta (tolerância de 0.05)
    acertou = abs(req.resposta - questao.gabarito) < 0.05
    
    # Atualizar domínio
    novo_dominio = atualizar_dominio(db, aluno.id, questao.conceito_id, acertou, req.usou_dica)
    
    # Registrar log para não repetir
    log = RespostaLog(aluno_id=aluno.id, questao_id=questao.id, acertou=acertou)
    db.add(log)
    
    # Processar meta de 5 questões diárias
    hoje = datetime.date.today()
    if aluno.ultimo_acesso != hoje:
        aluno.questoes_hoje = 1
        aluno.ultimo_acesso = hoje
    else:
        aluno.questoes_hoje += 1
        
    if aluno.questoes_hoje == 5:
        if aluno.ultima_ofensiva:
            diff = (hoje - aluno.ultima_ofensiva).days
            if diff == 1:
                aluno.ofensiva_dias += 1
            elif diff > 1:
                aluno.ofensiva_dias = 1
        else:
            aluno.ofensiva_dias = 1
        aluno.ultima_ofensiva = hoje
        
    db.commit()
    
    # Pegar feedback da IA
    feedback_ia = get_ia_feedback(acertou, questao.enunciado, questao.gabarito)
    
    return {
        "correto": acertou,
        "feedback_ia": feedback_ia,
        "dominio_atualizado": novo_dominio,
        "gabarito": questao.gabarito,
        "questoes_hoje": aluno.questoes_hoje
    }

@app.post("/duvida")
def perguntar_duvida(req: DuvidaRequest):
    resposta = responder_duvida_aluno(req.enunciado, req.duvida)
    return {"resposta_ia": resposta}

@app.get("/progresso/{nome}")
def obter_progresso(nome: str, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.nome == nome).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
        
    check_ofensiva_perdida(aluno, db)
    
    conceitos = db.query(Conceito).order_by(Conceito.id).all()
    progressos = db.query(AlunoProgresso).filter(AlunoProgresso.aluno_id == aluno.id).all()
    dominio_map = {p.conceito_id: p.dominio for p in progressos}
    
    from dominio import get_conceitos_desbloqueados
    desbloqueados = get_conceitos_desbloqueados(db, aluno.id)
    desbloqueados_ids = [d["id"] for d in desbloqueados]
    
    resultado = []
    for c in conceitos:
        dom = dominio_map.get(c.id, 0.0)
        
        status = "bloqueado"
        if c.id in desbloqueados_ids:
            if dom >= 0.70:
                status = "dominado"
            else:
                status = "ativo"
                
        # Garante que C01 esteja pelo menos ativo se não for dominado
        if c.id == 1 and status == "bloqueado":
            status = "ativo"
            
        resultado.append({
            "conceito": c.nome,
            "conceito_id": c.id,
            "dominio": dom,
            "status": status,
            "nivel": c.nivel
        })
        
    return {
        "ofensiva": aluno.ofensiva_dias,
        "questoes_hoje": aluno.questoes_hoje,
        "modulos": resultado
    }
