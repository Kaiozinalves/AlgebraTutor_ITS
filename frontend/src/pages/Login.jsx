import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { iniciarSessao } from '../api';
import { User, LogIn } from 'lucide-react';

function Login() {
  const [nome, setNome] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!nome.trim()) return;
    
    setLoading(true);
    try {
      const res = await iniciarSessao(nome);
      localStorage.setItem('aluno_nome', res.nome);
      navigate('/exercicio');
    } catch (err) {
      console.error(err);
      alert('Erro ao iniciar sessão');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="glass-panel w-full max-w-md p-8 rounded-2xl flex flex-col items-center">
        <div className="w-16 h-16 bg-brand-500/20 text-brand-400 rounded-full flex items-center justify-center mb-6">
          <User size={32} />
        </div>
        <h2 className="text-2xl font-bold mb-2">Bem-vindo(a)</h2>
        <p className="text-slate-400 text-center mb-8">
          Digite seu nome para iniciar ou continuar seus estudos de álgebra básica.
        </p>
        
        <form onSubmit={handleLogin} className="w-full flex flex-col gap-4">
          <div>
            <input
              type="text"
              placeholder="Qual o seu nome?"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              className="w-full px-4 py-3 bg-dark-900 border border-dark-700 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all text-lg placeholder-slate-500"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading || !nome.trim()}
            className="w-full flex items-center justify-center gap-2 bg-brand-500 hover:bg-brand-600 text-white font-semibold py-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Entrando...' : 'Entrar'}
            {!loading && <LogIn size={20} />}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
