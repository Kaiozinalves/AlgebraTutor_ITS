# 🧠 ITS Álgebra Básica - Tutor Inteligente

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)

Um Sistema Tutor Inteligente (ITS - Intelligent Tutoring System) focado no ensino de Álgebra Básica. O sistema utiliza as teorias de Aprendizado para o Domínio (Mastery Learning) em conjunto com a Inteligência Artificial Genenativa (Google Gemini) para proporcionar uma experiência de aprendizado adaptativa, rigorosa e hiper-personalizada.

## ✨ Principais Funcionalidades

- **🌳 Árvore de Conhecimento Guiada:** O currículo é estruturado em módulos interdependentes (ex: *Operações Básicas → Soma de Frações → Equações do 1º Grau*). O aluno só avança se atingir a proficiência mínima de 70% em cada conceito-base.
- **📉 Efeito Cascata (Avaliação Rigorosa):** Se durante uma revisão o aluno errar conceitos fundamentais e sua nota cair abaixo do limite estipulado, todos os módulos avançados que dependem daquela base serão imediatamente bloqueados e sua pontuação neles será zerada, forçando o resgate da base do conhecimento.
- **🤖 Chat Contextual "Tira-Dúvidas":** Integrado com o modelo `gemini-2.5-flash`, o aluno pode fazer perguntas abertas sobre o passo-a-passo da questão em que estiver com dúvida. A IA atua como um professor particular socrático: ela avalia o enunciado da questão e a dúvida do estudante, devolvendo dicas matemáticas valiosas sem nunca revelar a resposta final.
- **📊 Mapa de Progresso Interativo:** Uma interface rica e fluida que permite ao aluno navegar por seus módulos ativos, revisar os concluídos com questões ilimitadas, e entender claramente onde estão os bloqueios em sua árvore de habilidades.

## 🛠️ Tecnologias Utilizadas

- **Front-end:** React.js, Tailwind CSS, Vite, Lucide-React.
- **Back-end:** FastAPI (Python), SQLAlchemy (ORM).
- **Banco de Dados:** SQLite (escalável e auto-contido).
- **Inteligência Artificial:** Google GenAI SDK.

## 🚀 Como Executar o Projeto Localmente

### 1. Clonando o repositório
```bash
git clone https://github.com/Kaiozinalves/AlgebraTutor_ITS.git
cd AlgebraTutor_ITS
```

### 2. Configurando o Back-end
```bash
cd backend
# Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env na pasta backend com sua chave do Gemini
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Rode o script de seed para criar o banco de dados e popular as questões
python seed.py

# Inicie o servidor local
uvicorn main:app --reload --port 8000
```

### 3. Configurando o Front-end (Em outro terminal)
```bash
cd frontend

# Instale as dependências npm
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

### 4. Acessando a Aplicação
Abra seu navegador em: `http://localhost:5173`

---

Desenvolvido para fins acadêmicos na criação de sistemas adaptativos focados em metodologias ativas de ensino.
