import json
import random
import os

def gerar_c01(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        operacao1 = "+" if random.random() > 0.5 else "-"
        operacao2 = "+" if random.random() > 0.5 else "-"
        
        # Formatar a string cuidadosamente
        def fmt(num): return f"({num})" if num < 0 else str(num)
        
        expr = f"{fmt(a)} {operacao1} {fmt(b)} {operacao2} {fmt(c)}"
        val_b = b if operacao1 == "+" else -b
        val_c = c if operacao2 == "+" else -c
        ans = a + val_b + val_c
        
        questoes.append({
            "conceito_id": 1,
            "enunciado": f"Calcule: {expr}",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c02(qtd):
    questoes = []
    for _ in range(qtd):
        n1 = random.randint(1, 5)
        d1 = random.choice([2, 4, 5, 10])
        n2 = random.randint(1, 5)
        d2 = random.choice([2, 4, 5, 10])
        op = "+" if random.random() > 0.5 else "-"
        
        ans = (n1/d1) + (n2/d2) if op == "+" else (n1/d1) - (n2/d2)
        
        questoes.append({
            "conceito_id": 2,
            "enunciado": f"Calcule: {n1}/{d1} {op} {n2}/{d2}. Responda como decimal.",
            "gabarito": round(float(ans), 2),
            "dificuldade": 1
        })
    return questoes

def gerar_c03(qtd):
    questoes = []
    for _ in range(qtd):
        if random.random() > 0.5:
            # Potencia
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            ans = base ** exp
            questoes.append({
                "conceito_id": 3,
                "enunciado": f"Quanto é {base} elevado a {exp}?",
                "gabarito": float(ans),
                "dificuldade": 1
            })
        else:
            # Raiz exata
            val = random.randint(2, 12)
            sq = val * val
            questoes.append({
                "conceito_id": 3,
                "enunciado": f"Calcule a raiz quadrada de {sq}.",
                "gabarito": float(val),
                "dificuldade": 1
            })
    return questoes

def gerar_c04(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(2, 6)
        b = random.randint(-10, 10)
        x = random.randint(2, 8)
        ans = a * x + b
        
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        questoes.append({
            "conceito_id": 4,
            "enunciado": f"Se x = {x}, quanto vale {a}x {b_str}?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c05(qtd):
    questoes = []
    for _ in range(qtd):
        c1 = random.randint(2, 5)
        e1 = random.randint(2, 5)
        c2 = random.randint(2, 5)
        e2 = random.randint(2, 5)
        
        ans = e1 + e2
        questoes.append({
            "conceito_id": 5,
            "enunciado": f"Multiplique: {c1}x^{e1} * {c2}x^{e2}. Qual o expoente de x no resultado?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c06(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(1, 5)
        d = random.randint(-5, 5)
        op = "+" if random.random() > 0.5 else "-"
        
        ans = a + c if op == "+" else a - c
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        d_str = f"+ {d}" if d >= 0 else f"- {abs(d)}"
        
        questoes.append({
            "conceito_id": 6,
            "enunciado": f"Calcule ({a}x² {b_str}x) {op} ({c}x² {d_str}x). Qual o coeficiente de x²?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c07(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        ans = a * b
        questoes.append({
            "conceito_id": 7,
            "enunciado": f"Multiplique: (x + {a})(x + {b}). Qual o termo independente?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c08(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(2, 7)
        ans = a * a
        questoes.append({
            "conceito_id": 8,
            "enunciado": f"Expanda (x + {a})². Qual o termo independente?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c09(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(2, 8)
        ans = a
        sq = a * a
        questoes.append({
            "conceito_id": 9,
            "enunciado": f"Fatore x² - {sq}. Qual o valor numérico positivo que aparece nos fatores?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c10(qtd):
    questoes = []
    for _ in range(qtd):
        a = random.randint(2, 6)
        ans = random.randint(-5, 5)
        b = -a * ans
        
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        questoes.append({
            "conceito_id": 10,
            "enunciado": f"Resolva: {a}x {b_str} = 0. Qual o valor de x?",
            "gabarito": float(ans),
            "dificuldade": 1
        })
    return questoes

def gerar_c11(qtd):
    questoes = []
    for _ in range(qtd):
        x = random.randint(2, 8)
        y = random.randint(1, 7)
        soma = x + y
        sub = x - y
        questoes.append({
            "conceito_id": 11,
            "enunciado": f"Sistema: x + y = {soma} e x - y = {sub}. Qual o valor de x?",
            "gabarito": float(x),
            "dificuldade": 1
        })
    return questoes

def gerar_c12(qtd):
    questoes = []
    for _ in range(qtd):
        r1 = random.randint(1, 5)
        r2 = random.randint(-5, -1)
        s = r1 + r2
        p = r1 * r2
        
        s_str = f"- {s}x" if s > 0 else (f"+ {-s}x" if s < 0 else "")
        p_str = f"+ {p}" if p > 0 else (f"- {-p}" if p < 0 else "")
        
        questoes.append({
            "conceito_id": 12,
            "enunciado": f"Resolva: x² {s_str} {p_str} = 0. Qual a raiz positiva?",
            "gabarito": float(max(r1, r2)),
            "dificuldade": 2
        })
    return questoes

def gerar_todas_as_questoes(output_file="questoes_geradas.json", qtd_por_conceito=30):
    todas = []
    todas.extend(gerar_c01(qtd_por_conceito))
    todas.extend(gerar_c02(qtd_por_conceito))
    todas.extend(gerar_c03(qtd_por_conceito))
    todas.extend(gerar_c04(qtd_por_conceito))
    todas.extend(gerar_c05(qtd_por_conceito))
    todas.extend(gerar_c06(qtd_por_conceito))
    todas.extend(gerar_c07(qtd_por_conceito))
    todas.extend(gerar_c08(qtd_por_conceito))
    todas.extend(gerar_c09(qtd_por_conceito))
    todas.extend(gerar_c10(qtd_por_conceito))
    todas.extend(gerar_c11(qtd_por_conceito))
    todas.extend(gerar_c12(qtd_por_conceito))
    
    # Adicionar ID
    for i, q in enumerate(todas):
        q["id"] = i + 1
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(todas, f, indent=2, ensure_ascii=False)
    
    print(f"Foram geradas {len(todas)} questões com sucesso no arquivo {output_file}.")

if __name__ == "__main__":
    gerar_todas_as_questoes()
