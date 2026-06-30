import sqlite3

def migrate():
    conn = sqlite3.connect('its.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE alunos ADD COLUMN ofensiva_dias INTEGER DEFAULT 0")
        print("Coluna ofensiva_dias adicionada.")
    except Exception as e:
        print(f"Erro ofensiva_dias: {e}")
        
    try:
        c.execute("ALTER TABLE alunos ADD COLUMN ultimo_acesso DATE")
        print("Coluna ultimo_acesso adicionada.")
    except Exception as e:
        print(f"Erro ultimo_acesso: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
