import json
import os
from database import SessionLocal, engine, Base
from models import Conceito, PreRequisito, Questao
from gerador_questoes import gerar_todas_as_questoes

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

conceitos_iniciais = [
    {
        "id": 1, "nome": "Números inteiros e operações básicas", "nivel": 1,
        "resumo_teorico": "## O que são?\nO conjunto dos Números Inteiros (representado pela letra **Z**) inclui todos os números naturais (0, 1, 2, 3...) e também os seus opostos negativos (-1, -2, -3...).\nDiferente dos decimais e frações, eles não possuem partes \"quebradas\".\n\n## Regras de Sinais (Adição e Subtração)\nAqui, você pode pensar em **dinheiro**. Valores positivos são o seu saldo no banco, valores negativos são dívidas.\n- **`5 - 8 = -3`**: Você tinha 5 reais, mas gastou 8. Ficou devendo 3.\n- **`-2 - 4 = -6`**: Você estava devendo 2 reais e pegou mais 4 emprestados. Sua dívida aumentou para 6.\n\n## Regras de Sinais (Multiplicação e Divisão)\nA regra aqui é matemática pura e fixa:\n- **Sinais Iguais resultam em Positivo (+)**: `(+) * (+) = +` e `(-) * (-) = +`\n- **Sinais Diferentes resultam em Negativo (-)**: `(+) * (-) = -` e `(-) * (+) = -`\n\n## Exemplo Prático\nResolva a expressão: `(-3) * (-4) + (-5)`\n1. Primeiro a multiplicação: `(-3) * (-4) = +12` (sinais iguais fica positivo).\n2. Agora a adição: `12 + (-5) = 12 - 5 = 7`.\n\n## Dica de Ouro\nO maior erro dos alunos é usar a regra de multiplicação na soma! Lembra: `-2 - 3` NÃO é `+5`. Você deve 2 e deve 3, então deve 5 (`-5`)."
    },
    {
        "id": 2, "nome": "Frações e decimais", "nivel": 1,
        "resumo_teorico": "## O que é uma Fração?\nUma fração representa a parte de um todo que foi dividido em pedaços iguais. Ela possui:\n- **Numerador (topo):** Quantas partes temos.\n- **Denominador (base):** Em quantas partes o todo foi dividido.\n\nNa fração `3/4`, a pizza foi dividida em 4 pedaços e nós comemos 3. A barra da fração significa **divisão** (`3 ÷ 4 = 0,75`).\n\n## Como Somar e Subtrair?\n**1. Denominadores Iguais:** Some ou subtraia os numeradores e mantenha o denominador.\n*Exemplo:* `2/5 + 1/5 = 3/5`\n\n**2. Denominadores Diferentes:** Você não pode somar \"fatias\" de tamanhos diferentes. Antes de somar, use o **MMC (Mínimo Múltiplo Comum)**.\n*Exemplo:* `1/2 + 1/3`\n- O MMC de 2 e 3 é 6.\n- Ajuste as frações multiplicando em cima e embaixo: `(1*3)/(2*3) + (1*2)/(3*2) = 3/6 + 2/6 = 5/6`.\n\n## Como Multiplicar e Dividir?\n- **Multiplicação:** O de cima pelo de cima, o de baixo pelo de baixo. `(1/2) * (3/4) = 3/8`.\n- **Divisão:** Repita a primeira fração e multiplique pelo **inverso** da segunda. `(1/2) ÷ (3/4) = (1/2) * (4/3) = 4/6 = 2/3`.\n\n## Dica de Ouro\nPara converter qualquer decimal exato em fração, coloque o número sem vírgula em cima e o número 1 acompanhado de zeros (de acordo com as casas decimais) embaixo. `0,75 = 75/100`. Simplificando por 25, temos `3/4`."
    },
    {
        "id": 3, "nome": "Potenciação e radiciação", "nivel": 1,
        "resumo_teorico": "## O que é Potenciação?\nA potenciação é a multiplicação de um número (a base) por ele mesmo várias vezes (indicado pelo expoente).\n*Exemplo:* `2³ = 2 * 2 * 2 = 8`. (Não cometa o crime de dizer que é 2 * 3 = 6).\n\n## Principais Propriedades das Potências\nSendo as bases iguais, você pode aplicar \"atalhos\":\n1. **Multiplicação:** Soma os expoentes. `a² * a³ = a⁵`\n2. **Divisão:** Subtrai os expoentes. `a⁵ / a³ = a²`\n3. **Potência de Potência:** Multiplica os expoentes. `(a²)³ = a⁶`\n4. **Expoente Zero:** Qualquer número (diferente de zero) elevado a zero é igual a 1. `5⁰ = 1`.\n5. **Expoente Negativo:** Inverte-se a base e o expoente fica positivo. `2⁻¹ = 1/2`.\n\n## O que é Radiciação?\nÉ a operação inversa da potenciação. A raiz quadrada (`√x`) procura um número que, multiplicado por ele mesmo, resulte em `x`.\n*Exemplo:* `√16 = 4`, porque `4² = 16`.\n\n## Dica de Ouro\nUma raiz pode ser escrita como uma potência com expoente fracionário! A regra do sol e da sombra: \"Quem está no sol (índice da raiz) vai para a sombra (embaixo na fração), quem está na sombra (expoente de dentro) vai para o sol\". \n*Exemplo:* `³√x² = x^(2/3)`."
    },
    {
        "id": 4, "nome": "Expressões algébricas e variáveis", "nivel": 2,
        "resumo_teorico": "## O que é a Álgebra?\nA Álgebra é o ramo da matemática onde letras (chamadas de **variáveis** ou incógnitas) são usadas para representar números desconhecidos ou valores que podem mudar. O \"x\" é a variável mais famosa, mas você pode usar qualquer letra.\n\n## O que são Expressões Algébricas?\nSão expressões matemáticas que misturam números, letras e operações (adição, subtração, etc).\n*Exemplo:* `2x + 5y - 3`.\n\n## Como Simplificar (Redução de Termos Semelhantes)\nA regra de ouro da álgebra é: **Você só pode somar ou subtrair \"coisas iguais\"**. \n- Você pode somar `x` com `x` (ex: `2x + 3x = 5x`).\n- Você NÃO pode somar `x` com `y` ou `x` com `x²`. (ex: `2x + 3y` já está simplificado).\n\nPense em laranjas e maçãs: 2 maçãs + 3 maçãs = 5 maçãs. Mas 2 maçãs + 3 laranjas não dá 5 \"maçaranjas\".\n\n## Valor Numérico\nSe o problema te disser o valor da letra, basta substituir e calcular.\n*Exemplo:* Qual o valor numérico de `2x + 5` quando `x = 3`?\n`2 * (3) + 5 = 6 + 5 = 11`.\n\n## Dica de Ouro\nQuando uma letra está colada em um número, existe um sinal de multiplicação invisível entre eles! `5x` significa \"5 vezes x\". Se não há número na frente do x, ele vale 1 (ou seja, `x = 1x`)."
    },
    {
        "id": 5, "nome": "Operações com monômios", "nivel": 2,
        "resumo_teorico": "## O que é um Monômio?\nUm monômio é a expressão algébrica mais simples possível. Ele é formado por apenas um único termo, que contém uma parte numérica (coeficiente) e uma parte literal (as letras).\n*Exemplo:* Em `-5x²y`, o `-5` é o coeficiente numérico e o `x²y` é a parte literal.\n\n## Operações Básicas\n**1. Adição e Subtração:**\nSó é possível se as partes literais forem **exatamente idênticas**! \n- Certo: `3x² + 5x² = 8x²`\n- Errado: `3x² + 5x` (não se misturam).\n\n**2. Multiplicação:**\nNa multiplicação, você não precisa de termos semelhantes! A regra é: **Multiplica número com número e letra com letra** (usando a propriedade das potências).\n*Exemplo:* `(2x) * (4x²) = (2 * 4) * (x¹ * x²) = 8x³`\n\n**3. Divisão:**\nDivide-se número com número e letra com letra (subtraindo os expoentes).\n*Exemplo:* `(10x³) ÷ (2x) = (10 ÷ 2) * (x³ / x¹) = 5x²`\n\n## Dica de Ouro\nCuidado com os sinais na hora de multiplicar e dividir! Aplique a regra de sinais dos números inteiros (menos com menos dá mais) nos coeficientes antes de mexer nas letras."
    },
    {
        "id": 6, "nome": "Polinômios — adição e subtração", "nivel": 2,
        "resumo_teorico": "## O que é um Polinômio?\nA palavra polinômio significa \"muitos termos\" (poli = muitos, nômio = termo). É uma expressão algébrica formada pela adição ou subtração de vários monômios.\n*Exemplo:* `2x² - 3x + 5` (um polinômio de 3 termos, também chamado de trinômio).\n\n## Como Adicionar Polinômios?\nA regra é a mesma dos monômios: agrupe e some apenas os termos **semelhantes** (mesma letra, mesmo expoente).\n*Exemplo:* `(3x² + 2x - 1) + (x² - 5x + 4)`\n1. Agrupe os quadrados: `3x² + 1x² = 4x²`\n2. Agrupe os 'x' simples: `2x - 5x = -3x`\n3. Agrupe os números: `-1 + 4 = 3`\n**Resultado Final:** `4x² - 3x + 3`\n\n## Como Subtrair Polinômios?\nA subtração é perigosa por causa do sinal de menos na frente do parêntese. O sinal de menos atua como um \"inversor\", trocando o sinal de todos os termos lá dentro!\n*Exemplo:* `(5x + 3) - (2x - 4)`\n1. Aplique o sinal: `- (2x - 4)` vira `-2x + 4`.\n2. Agora some: `(5x + 3) - 2x + 4 = 3x + 7`.\n\n## Dica de Ouro\nUm erro clássico na subtração de polinômios é esquecer de trocar o sinal do segundo, terceiro ou quarto termo dentro do parêntese. Sempre distribua o sinal negativo como se ele fosse um `-1` multiplicando tudo!"
    },
    {
        "id": 7, "nome": "Multiplicação de polinômios", "nivel": 2,
        "resumo_teorico": "## Como Funciona a Multiplicação de Polinômios?\nQuando multiplicamos um polinômio por outro, devemos aplicar a **Propriedade Distributiva**, muito conhecida no Brasil como o método do \"Chuveirinho\". A regra é: cada termo do primeiro parêntese deve multiplicar cada termo do segundo parêntese.\n\n## Passo a Passo (Monômio por Polinômio)\n*Exemplo:* `2x(x + 3)`\n- O `2x` multiplica o `x`: `2x * x = 2x²`\n- O `2x` multiplica o `3`: `2x * 3 = 6x`\n**Resultado:** `2x² + 6x`\n\n## Passo a Passo (Polinômio por Polinômio)\n*Exemplo Clássico:* `(x + 2)(x - 5)`\n1. O primeiro com o primeiro: `x * x = x²`\n2. O primeiro com o segundo: `x * (-5) = -5x`\n3. O segundo com o primeiro: `2 * x = +2x`\n4. O segundo com o segundo: `2 * (-5) = -10`\n\nJuntando tudo: `x² - 5x + 2x - 10`.\nPor fim, reduza os termos semelhantes do meio (`-5x + 2x = -3x`).\n**Resultado Final:** `x² - 3x - 10`\n\n## Dica de Ouro\nSeja muito organizado. Se você estiver multiplicando um polinômio de 3 termos por outro de 3 termos, você terá 9 multiplicações para fazer antes de juntar tudo. Faça setinhas com o lápis para não se perder!"
    },
    {
        "id": 8, "nome": "Produtos notáveis", "nivel": 3,
        "resumo_teorico": "## O que são Produtos Notáveis?\nEm matemática, \"notável\" significa \"digno de nota\" ou \"importante\". Os produtos notáveis são multiplicações de polinômios que aparecem com tanta frequência que nós criamos \"fórmulas rápidas\" para resolvê-los sem precisar fazer todo o chuveirinho.\n\n## As 3 Regras de Ouro\n**1. Quadrado da Soma:** `(a + b)² = a² + 2ab + b²`\n- \"O quadrado do primeiro, mais duas vezes o primeiro pelo segundo, mais o quadrado do segundo.\"\n\n**2. Quadrado da Diferença:** `(a - b)² = a² - 2ab + b²`\n- \"O quadrado do primeiro, menos duas vezes o primeiro pelo segundo, mais o quadrado do segundo.\"\n\n**3. Produto da Soma pela Diferença:** `(a + b)(a - b) = a² - b²`\n- O meio se anula! \"O quadrado do primeiro menos o quadrado do segundo.\"\n\n## Exemplo Prático\nResolva `(x + 3)²`\nAplicando a regra 1: O primeiro é `x` e o segundo é `3`.\n`x² + 2*(x)*(3) + 3² = x² + 6x + 9`. (Se fizer o chuveirinho `(x+3)(x+3)`, vai chegar no mesmo resultado!).\n\n## Dica de Ouro Crítica\n**NUNCA, JAMAIS Diga que `(a + b)² = a² + b²`**. O expoente não \"cai\" para dentro da soma. Você sempre estará esquecendo do termo central `2ab`. Isso anula a sua nota na prova inteira!"
    },
    {
        "id": 9, "nome": "Fatoração", "nivel": 3,
        "resumo_teorico": "## O que é Fatoração?\nFatorar é exatamente o processo oposto da multiplicação e dos produtos notáveis. Se a distributiva é você \"misturar os ingredientes para fazer o bolo\", a fatoração é \"separar o bolo de volta nos seus ingredientes originais\". \nO objetivo é transformar uma soma algébrica em um produto (multiplicação).\n\n## Principais Métodos\n\n**1. Fator Comum em Evidência:**\nProcure algo que se repete em todos os termos e coloque para fora do parêntese.\n*Exemplo:* `3x² + 6x`\n- O que repete? O número 3 divide os dois, e o `x` está nos dois. Fator comum: `3x`.\n- Dividindo os termos pelo fator comum: `3x(x + 2)`.\n\n**2. Agrupamento:**\nQuando há 4 termos e nenhum fator comum a todos eles, agrupe de 2 em 2.\n*Exemplo:* `ax + ay + bx + by` -> Fatorando em pares -> `a(x+y) + b(x+y)` -> `(a+b)(x+y)`.\n\n**3. Diferença de Quadrados:**\nReconhecimento do produto notável `a² - b²`.\n*Exemplo:* `x² - 25`. Ambos têm raiz exata e um menos no meio. O resultado é `(x + 5)(x - 5)`.\n\n## Dica de Ouro\nSempre confira a sua fatoração fazendo o chuveirinho mentalmente! Se você fatorou `x² - 9` como `(x - 3)(x + 3)`, faça a multiplicação rápida de volta para ver se o resultado volta ao original."
    },
    {
        "id": 10, "nome": "Equações de 1.º grau", "nivel": 3,
        "resumo_teorico": "## O que é uma Equação de 1º Grau?\nÉ uma afirmação matemática de igualdade contendo uma letra desconhecida (incógnita), cujo maior expoente é 1. O formato padrão é `ax + b = 0`. Resolver a equação significa descobrir qual número a letra representa para que a balança fique equilibrada.\n\n## Como Resolver (O Método da Balança)\nPara isolar o `x` e descobrir seu valor, devemos passar os números para o outro lado do sinal de igual. A regra principal é: **tudo que muda de lado, muda para a operação matemática inversa**.\n\n- Se está somando (`+`), passa subtraindo (`-`).\n- Se está subtraindo (`-`), passa somando (`+`).\n- Se está multiplicando (`*`), passa dividindo (`/`).\n- Se está dividindo (`/`), passa multiplicando (`*`).\n\n## Passo a Passo\nResolva: `3x - 5 = 10`\n1. Passe o número solto para o outro lado: o `-5` vira `+5`.\n   `3x = 10 + 5`\n   `3x = 15`\n2. Isole o `x`: o `3` que está multiplicando passa dividindo.\n   `x = 15 / 3`\n   `x = 5`\n\n## Dica de Ouro\nSe você tem `x` nos dois lados da igualdade (ex: `4x = 2x + 8`), coloque todos os \"letrados\" de um lado e todos os números do outro. Passando o `2x` para a esquerda: `4x - 2x = 8` -> `2x = 8` -> `x = 4`."
    },
    {
        "id": 11, "nome": "Sistemas de equações", "nivel": 4,
        "resumo_teorico": "## O que é um Sistema de Equações?\nUm sistema ocorre quando você tem duas (ou mais) variáveis desconhecidas (ex: `x` e `y`) e duas equações amarradas entre si. O desafio é encontrar um par de valores que torne ambas as equações verdadeiras ao mesmo tempo.\n\n## Método da Substituição (O mais intuitivo)\nEste método consiste em isolar uma letra em uma equação e substituí-la na outra.\n**Exemplo Prático:**\n1) `x + y = 5`\n2) `2x - y = 4`\n\n**Passo 1:** Isole o `x` na primeira equação:\n`x = 5 - y`\n\n**Passo 2:** Substitua essa expressão inteira no lugar do `x` na segunda equação:\n`2(5 - y) - y = 4`\n\n**Passo 3:** Resolva a nova equação (que agora só tem y):\n`10 - 2y - y = 4`\n`10 - 3y = 4`\n`-3y = -6`  ->  `y = 2`\n\n**Passo 4:** Volte lá no Passo 1 para descobrir o x:\n`x = 5 - 2`  ->  `x = 3`. \nPronto, `x=3` e `y=2`.\n\n## Método da Adição (O mais rápido)\nSe as variáveis tiverem coeficientes opostos (ex: `+y` e `-y`), basta somar as duas equações como uma conta de mais, e uma letra irá sumir magicamente!\n\n## Dica de Ouro\nSe o problema for sobre galinhas e vacas em uma fazenda (\"temos 10 cabeças e 26 pernas\"), chame as galinhas de `x` e as vacas de `y`. \nCabeças: `x + y = 10`. \nPernas: `2x + 4y = 26`. Monte o sistema e seja feliz!"
    },
    {
        "id": 12, "nome": "Equações de 2.º grau / Bhaskara", "nivel": 4,
        "resumo_teorico": "## O que é uma Equação de 2º Grau?\nÉ uma equação onde o maior expoente da incógnita é 2. O seu formato geral e obrigatório para resolver é:\n`ax² + bx + c = 0`\n\nOnde `a`, `b` e `c` são números fixos (chamados de coeficientes).\n*Exemplo:* Em `2x² - 5x + 3 = 0`, temos `a = 2`, `b = -5` e `c = 3`.\n\n## A Famosa Fórmula de Bhaskara\nPara encontrar as raízes (os valores de x que resolvem o problema), usamos a fórmula dividida em duas etapas:\n\n**Etapa 1: Calcular o Delta (O Discriminante - Δ)**\n`Δ = b² - 4ac`\n*(Dica: se o Δ der negativo, pare a conta! A equação não tem raiz real).*\n\n**Etapa 2: A Fórmula Final**\n`x = (-b ± √Δ) / 2a`\nO símbolo `±` significa que a equação vai \"se ramificar\" e ter dois resultados: um somando a raiz e outro subtraindo a raiz. (x1 e x2).\n\n## Exemplo Prático\nResolva: `x² - 5x + 6 = 0` (Aqui, a=1, b=-5, c=6)\n1. `Δ = (-5)² - 4*(1)*(6) = 25 - 24 = 1`\n2. `x = ( -(-5) ± √1 ) / 2*(1)`\n3. `x = (5 ± 1) / 2`\nResultados:\n`x1 = (5+1)/2 = 3`\n`x2 = (5-1)/2 = 2`\n\n## Dica de Ouro\nA equação precisa estar sempre igualada a zero antes de começar. Se vier `x² = 5x - 6`, você deve jogar tudo para a esquerda antes de tirar os coeficientes: `x² - 5x + 6 = 0`."
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
        else:
            exist.resumo_teorico = c["resumo_teorico"]
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
