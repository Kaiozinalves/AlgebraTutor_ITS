import json
import os
from database import SessionLocal, engine, Base
from models import Conceito, PreRequisito, Questao
from gerador_questoes import gerar_todas_as_questoes

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

conceitos_iniciais = [
    {"id": 1, "nome": "Números inteiros e operações básicas", "nivel": 1},
    {"id": 2, "nome": "Frações e decimais", "nivel": 1},
    {"id": 3, "nome": "Potenciação e radiciação", "nivel": 1},
    {"id": 4, "nome": "Expressões algébricas e variáveis", "nivel": 2},
    {"id": 5, "nome": "Operações com monômios", "nivel": 2},
    {"id": 6, "nome": "Polinômios — adição e subtração", "nivel": 2},
    {"id": 7, "nome": "Multiplicação de polinômios", "nivel": 2},
    {"id": 8, "nome": "Produtos notáveis", "nivel": 3},
    {"id": 9, "nome": "Fatoração", "nivel": 3},
    {"id": 10, "nome": "Equações de 1.º grau", "nivel": 3},
    {"id": 11, "nome": "Sistemas de equações", "nivel": 4},
    {"id": 12, "nome": "Equações de 2.º grau / Bhaskara", "nivel": 4},
]

pre_requisitos_map = {
    2: [1],
    3: [1],
    4: [1, 2],
    5: [4],
    6: [5],
    7: [6],
    8: [7],
    9: [8],
    10: [4, 5],
    11: [10],
    12: [10, 8]
}

def seed_db():
    db = SessionLocal()
    
    # 1. Inserir Conceitos
    for c in conceitos_iniciais:
        exist = db.query(Conceito).filter(Conceito.id == c["id"]).first()
        if not exist:
            novo_conceito = Conceito(id=c["id"], nome=c["nome"], nivel=c["nivel"])
            db.add(novo_conceito)
    db.commit()
    print("Conceitos inseridos com sucesso.")
    
    # 2. Inserir Pré-requisitos
    for conceito_id, pre_reqs in pre_requisitos_map.items():
        for pr_id in pre_reqs:
            exist = db.query(PreRequisito).filter(
                PreRequisito.conceito_id == conceito_id,
                PreRequisito.pre_requisito_id == pr_id
            ).first()
            if not exist:
                novo_pr = PreRequisito(conceito_id=conceito_id, pre_requisito_id=pr_id)
                db.add(novo_pr)
    db.commit()
    print("Pré-requisitos inseridos com sucesso.")
    
    # 3. Gerar Questões
    json_path = "questoes_geradas.json"
    gerar_todas_as_questoes(json_path, qtd_por_conceito=30)
    
    with open(json_path, "r", encoding="utf-8") as f:
        questoes = json.load(f)
        
    count = 0
    for q in questoes:
        exist = db.query(Questao).filter(Questao.id == q["id"]).first()
        if not exist:
            nova_questao = Questao(
                id=q["id"],
                conceito_id=q["conceito_id"],
                enunciado=q["enunciado"],
                gabarito=q["gabarito"],
                dificuldade=q["dificuldade"]
            )
            db.add(nova_questao)
            count += 1
            
    db.commit()
    db.close()
    print(f"{count} Questões inseridas com sucesso.")

if __name__ == "__main__":
    seed_db()
