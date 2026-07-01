from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Conceito(Base):
    __tablename__ = "conceitos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    nivel = Column(Integer)
    resumo_teorico = Column(String, nullable=True)
    
    # Relação para pegar os pré-requisitos onde este conceito é o alvo
    pre_requisitos = relationship("PreRequisito", foreign_keys="PreRequisito.conceito_id", back_populates="conceito")
    questoes = relationship("Questao", back_populates="conceito")

class PreRequisito(Base):
    __tablename__ = "pre_requisitos"
    id = Column(Integer, primary_key=True, index=True)
    conceito_id = Column(Integer, ForeignKey("conceitos.id"))
    pre_requisito_id = Column(Integer, ForeignKey("conceitos.id"))
    
    conceito = relationship("Conceito", foreign_keys=[conceito_id], back_populates="pre_requisitos")
    pre_requisito = relationship("Conceito", foreign_keys=[pre_requisito_id])

class Questao(Base):
    __tablename__ = "questoes"
    id = Column(Integer, primary_key=True, index=True)
    conceito_id = Column(Integer, ForeignKey("conceitos.id"))
    enunciado = Column(String)
    gabarito = Column(Float)
    dificuldade = Column(Integer)
    
    conceito = relationship("Conceito", back_populates="questoes")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    ofensiva_dias = Column(Integer, default=0)
    ultimo_acesso = Column(Date, nullable=True)
    questoes_hoje = Column(Integer, default=0)
    ultima_ofensiva = Column(Date, nullable=True)
    
    progresso = relationship("AlunoProgresso", back_populates="aluno")
    respostas = relationship("RespostaLog", back_populates="aluno")

class AlunoProgresso(Base):
    __tablename__ = "aluno_progresso"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    conceito_id = Column(Integer, ForeignKey("conceitos.id"))
    dominio = Column(Float, default=0.0) # de 0.0 a 1.0
    
    aluno = relationship("Aluno", back_populates="progresso")
    conceito = relationship("Conceito")

class RespostaLog(Base):
    __tablename__ = "resposta_logs"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    questao_id = Column(Integer, ForeignKey("questoes.id"))
    acertou = Column(Boolean)
    
    aluno = relationship("Aluno", back_populates="respostas")
    questao = relationship("Questao")
