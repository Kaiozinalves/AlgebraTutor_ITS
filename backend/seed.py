import json
import os
from database import SessionLocal, engine, Base
from models import Conceito, PreRequisito, Questao
from gerador_questoes import gerar_todas_as_questoes

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

conceitos_iniciais = [
    {
        "id": 1, 
        "nome": "Números inteiros e operações básicas", 
        "nivel": 1,
        "resumo_teorico": "## O que são?\nSão números sem parte decimal (ex: -2, -1, 0, 1, 2). \n\n## Regra dos Sinais\n- Na multiplicação/divisão, sinais iguais: **+**\n- Sinais diferentes: **-**\n\n## Exemplo Prático\n`(-3) * (-4) = 12`\n\n## Dica de Ouro\nLembre-se sempre: menos com menos dá mais!"
    },
    {
        "id": 2, 
        "nome": "Frações e decimais", 
        "nivel": 1,
        "resumo_teorico": "## O que é?\nFrações representam partes de um todo. Decimais são outra forma de escrever frações.\n\n## Como somar?\nSe os denominadores forem diferentes, encontre o MMC antes de somar.\n\n## Exemplo Prático\n`1/2 + 1/4 = 2/4 + 1/4 = 3/4`"
    },
    {
        "id": 3, 
        "nome": "Potenciação e radiciação", 
        "nivel": 1,
        "resumo_teorico": "## O que é?\nA potenciação é uma multiplicação repetida. A radiciação é o inverso da potenciação.\n\n## Fórmulas\n`a^m * a^n = a^(m+n)`\n\n## Exemplo Prático\n`2^3 = 2 * 2 * 2 = 8`"
    },
    {
        "id": 4, 
        "nome": "Expressões algébricas e variáveis", 
        "nivel": 2,
        "resumo_teorico": "## O que são?\nLetras (variáveis) são usadas para representar números desconhecidos.\n\n## Como simplificar?\nVocê só pode somar variáveis exatamente iguais.\n\n## Exemplo Prático\n`2x + 3x = 5x`."
    },
    {
        "id": 5, 
        "nome": "Operações com monômios", 
        "nivel": 2,
        "resumo_teorico": "## O que são?\nMonômios são expressões algébricas com um único termo, ex: `3x²`.\n\n## Multiplicação\nMultiplica-se os números e soma-se os expoentes das letras iguais.\n\n## Exemplo Prático\n`(2x) * (3x) = 6x²`"
    },
    {
        "id": 6, 
        "nome": "Polinômios — adição e subtração", 
        "nivel": 2,
        "resumo_teorico": "## O que são?\nPolinômios são somas de vários monômios.\n\n## Adição/Subtração\nJunte os termos semelhantes (mesma letra e mesmo expoente).\n\n## Exemplo Prático\n`(3x + 2) + (x - 1) = 4x + 1`"
    },
    {
        "id": 7, 
        "nome": "Multiplicação de polinômios", 
        "nivel": 2,
        "resumo_teorico": "## Como fazer?\nUse a propriedade distributiva (o famoso 'chuveirinho'). Multiplique cada termo do primeiro polinômio por cada termo do segundo.\n\n## Exemplo Prático\n`x(x + 2) = x² + 2x`"
    },
    {
        "id": 8, 
        "nome": "Produtos notáveis", 
        "nivel": 3,
        "resumo_teorico": "## O que são?\nSão multiplicações frequentes que possuem regras rápidas para resolver sem precisar usar o chuveirinho.\n\n## Principal Regra\nQuadrado da soma: `(a+b)² = a² + 2ab + b²`\n\n## Dica de Ouro\nNunca diga que `(a+b)² = a² + b²`. Isso é o erro mais comum da matemática! Você sempre esquece do 2ab no meio."
    },
    {
        "id": 9, 
        "nome": "Fatoração", 
        "nivel": 3,
        "resumo_teorico": "## O que é?\nÉ o processo de transformar uma soma em uma multiplicação (o inverso do chuveirinho).\n\n## Fator Comum em Evidência\nColoca-se o número ou variável que repete em evidência.\n\n## Exemplo Prático\n`2x + 4 = 2(x + 2)`"
    },
    {
        "id": 10, 
        "nome": "Equações de 1.º grau", 
        "nivel": 3,
        "resumo_teorico": "## O que é?\nÉ uma igualdade com uma variável desconhecida `x` que não tem expoente maior que 1.\n\n## Como resolver?\nIsole o `x` passando os números para o outro lado com a operação inversa (se está somando, passa subtraindo).\n\n## Exemplo Prático\n`2x + 4 = 10` \n `2x = 6` \n `x = 3`"
    },
    {
        "id": 11, 
        "nome": "Sistemas de equações", 
        "nivel": 4,
        "resumo_teorico": "## O que é?\nUm conjunto de duas ou mais equações com várias variáveis (x, y).\n\n## Método da Substituição\nIsole uma letra em uma equação e jogue o valor na outra.\n\n## Exemplo Prático\n`x + y = 3` e `x = 1`\nSubstituindo o x: `1 + y = 3` -> `y = 2`"
    },
    {
        "id": 12, 
        "nome": "Equações de 2.º grau / Bhaskara", 
        "nivel": 4,
        "resumo_teorico": "## O que é?\nUma equação no formato `ax² + bx + c = 0`.\n\n## Fórmula de Bhaskara\n`x = (-b ± √(b² - 4ac)) / 2a`\n\n## Dica de Ouro\nO termo dentro da raiz é chamado de Delta (Δ). Se o Delta for negativo, a equação não tem nenhuma raiz real!"
    }
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
            novo_conceito = Conceito(id=c["id"], nome=c["nome"], nivel=c["nivel"], resumo_teorico=c["resumo_teorico"])
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
