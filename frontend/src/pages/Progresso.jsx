import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { obterProgresso } from '../api';
import { Trophy, Lock, PlayCircle, CheckCircle2 } from 'lucide-react';

function Progresso() {
  const [nome, setNome] = useState('');
  const [progresso, setProgresso] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const aluno = localStorage.getItem('aluno_nome');
    if (!aluno) {
      navigate('/');
      return;
    }
    setNome(aluno);
    carregarProgresso(aluno);
  }, []);

  const carregarProgresso = async (aluno) => {
    setLoading(true);
    try {
      const data = await obterProgresso(aluno);
      setProgresso(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const levels = [1, 2, 3, 4];

  if (loading) return <div className="text-center pt-20 text-slate-400">Carregando mapa de conceitos...</div>;

  return (
    <div className="flex-1 flex flex-col pb-10">
      <div className="flex items-center justify-between mb-8 mt-4">
        <div>
          <h2 className="text-3xl font-bold mb-1">Seu Progresso</h2>
          <p className="text-slate-400">Acompanhe seu desenvolvimento, {nome}.</p>
        </div>
        <button onClick={() => navigate('/exercicio')} className="px-5 py-2 bg-brand-500 hover:bg-brand-600 font-medium rounded-xl flex items-center gap-2 transition">
          <PlayCircle size={20} /> Continuar Estudando
        </button>
      </div>

      <div className="space-y-12">
        {levels.map(nivel => {
          const conceitos = progresso.filter(c => c.nivel === nivel);
          if(conceitos.length === 0) return null;
          
          return (
            <div key={nivel} className="space-y-4">
              <h3 className="text-xl font-semibold text-brand-300 flex items-center gap-2">
                Nível {nivel}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {conceitos.map(c => (
                  <div 
                    key={c.conceito_id} 
                    onClick={() => {
                      if (c.status !== 'bloqueado') {
                        navigate(`/exercicio?conceito=${c.conceito_id}`);
                      }
                    }}
                    title={c.status !== 'bloqueado' ? "Clique para revisar este módulo" : ""}
                    className={`glass-panel p-5 rounded-xl border transition-all duration-300 ${c.status === 'bloqueado' ? 'opacity-60 border-dark-700 cursor-not-allowed' : 'cursor-pointer hover:border-brand-500/50 hover:bg-dark-800/50'} ${c.status === 'dominado' ? 'border-brand-500/30 bg-brand-900/10' : 'border-dark-600'}`}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <h4 className="font-medium pr-4">{c.conceito}</h4>
                      {c.status === 'bloqueado' && <Lock size={20} className="text-slate-500" />}
                      {c.status === 'dominado' && <CheckCircle2 size={20} className="text-brand-500" />}
                    </div>
                    
                    <div className="w-full h-3 bg-dark-900 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${c.status === 'dominado' ? 'bg-brand-500' : 'bg-slate-400'}`}
                        style={{ width: `${Math.max(5, c.dominio * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between mt-2 text-xs text-slate-400 font-medium">
                      <span>{(c.dominio * 100).toFixed(0)}% domínio</span>
                      <span>Meta: 70%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Progresso;
