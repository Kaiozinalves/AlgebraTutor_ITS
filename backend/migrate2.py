import sqlite3

def migrate():
    conn = sqlite3.connect('its.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE alunos ADD COLUMN questoes_hoje INTEGER DEFAULT 0")
        print("Coluna questoes_hoje adicionada.")
    except Exception as e:
        print(f"Erro questoes_hoje: {e}")
        
    try:
        c.execute("ALTER TABLE alunos ADD COLUMN ultima_ofensiva DATE")
        print("Coluna ultima_ofensiva adicionada.")
    except Exception as e:
        print(f"Erro ultima_ofensiva: {e}")
        
    # Resetar ofensiva atual por causa da nova regra de datas
    c.execute("UPDATE alunos SET ofensiva_dias = 0, questoes_hoje = 0")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
