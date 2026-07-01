import sqlite3

resumos = {
    1: "## O que são?\nSão números sem parte decimal (ex: -2, -1, 0, 1, 2). \n\n## Regra dos Sinais\n- Na multiplicação/divisão, sinais iguais: **+**\n- Sinais diferentes: **-**\n\n## Exemplo Prático\n`(-3) * (-4) = 12`\n\n## Dica de Ouro\nLembre-se sempre: menos com menos dá mais!",
    2: "## O que é?\nFrações representam partes de um todo. Decimais são outra forma de escrever frações.\n\n## Como somar?\nSe os denominadores forem diferentes, encontre o MMC antes de somar.\n\n## Exemplo Prático\n`1/2 + 1/4 = 2/4 + 1/4 = 3/4`",
    3: "## O que é?\nA potenciação é uma multiplicação repetida. A radiciação é o inverso da potenciação.\n\n## Fórmulas\n`a^m * a^n = a^(m+n)`\n\n## Exemplo Prático\n`2^3 = 2 * 2 * 2 = 8`",
    4: "## O que são?\nLetras (variáveis) são usadas para representar números desconhecidos.\n\n## Como simplificar?\nVocê só pode somar variáveis exatamente iguais.\n\n## Exemplo Prático\n`2x + 3x = 5x`.",
    5: "## O que são?\nMonômios são expressões algébricas com um único termo, ex: `3x²`.\n\n## Multiplicação\nMultiplica-se os números e soma-se os expoentes das letras iguais.\n\n## Exemplo Prático\n`(2x) * (3x) = 6x²`",
    6: "## O que são?\nPolinômios são somas de vários monômios.\n\n## Adição/Subtração\nJunte os termos semelhantes (mesma letra e mesmo expoente).\n\n## Exemplo Prático\n`(3x + 2) + (x - 1) = 4x + 1`",
    7: "## Como fazer?\nUse a propriedade distributiva (o famoso 'chuveirinho'). Multiplique cada termo do primeiro polinômio por cada termo do segundo.\n\n## Exemplo Prático\n`x(x + 2) = x² + 2x`",
    8: "## O que são?\nSão multiplicações frequentes que possuem regras rápidas para resolver sem precisar usar o chuveirinho.\n\n## Principal Regra\nQuadrado da soma: `(a+b)² = a² + 2ab + b²`\n\n## Dica de Ouro\nNunca diga que `(a+b)² = a² + b²`. Isso é o erro mais comum da matemática! Você sempre esquece do 2ab no meio.",
    9: "## O que é?\nÉ o processo de transformar uma soma em uma multiplicação (o inverso do chuveirinho).\n\n## Fator Comum em Evidência\nColoca-se o número ou variável que repete em evidência.\n\n## Exemplo Prático\n`2x + 4 = 2(x + 2)`",
    10: "## O que é?\nÉ uma igualdade com uma variável desconhecida `x` que não tem expoente maior que 1.\n\n## Como resolver?\nIsole o `x` passando os números para o outro lado com a operação inversa (se está somando, passa subtraindo).\n\n## Exemplo Prático\n`2x + 4 = 10` \n `2x = 6` \n `x = 3`",
    11: "## O que é?\nUm conjunto de duas ou mais equações com várias variáveis (x, y).\n\n## Método da Substituição\nIsole uma letra em uma equação e jogue o valor na outra.\n\n## Exemplo Prático\n`x + y = 3` e `x = 1`\nSubstituindo o x: `1 + y = 3` -> `y = 2`",
    12: "## O que é?\nUma equação no formato `ax² + bx + c = 0`.\n\n## Fórmula de Bhaskara\n`x = (-b ± √(b² - 4ac)) / 2a`\n\n## Dica de Ouro\nO termo dentro da raiz é chamado de Delta (Δ). Se o Delta for negativo, a equação não tem nenhuma raiz real!"
}

conn = sqlite3.connect('its.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE conceitos ADD COLUMN resumo_teorico TEXT")
    print("Coluna adicionada ao banco.")
except sqlite3.OperationalError:
    print("Coluna já existe no banco.")

for cid, resumo in resumos.items():
    c.execute("UPDATE conceitos SET resumo_teorico = ? WHERE id = ?", (resumo, cid))
    
conn.commit()
conn.close()
print("Resumos migrados e aplicados com sucesso!")
