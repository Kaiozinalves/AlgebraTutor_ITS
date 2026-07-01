import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { obterProgresso, obterResumoTeoria } from '../api';
import ReactMarkdown from 'react-markdown';
import { BookOpen, Lock, ChevronRight, GraduationCap } from 'lucide-react';

export default function Teoria() {
  const [nome, setNome] = useState('');
  const [conceitos, setConceitos] = useState([]);
  const [resumoAtual, setResumoAtual] = useState(null);
  const [loadingResumo, setLoadingResumo] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const aluno = localStorage.getItem('aluno_nome');
    if (!aluno) {
      navigate('/');
      return;
    }
    setNome(aluno);
    
    // Puxa o progresso para saber quais conceitos existem e estão desbloqueados
    obterProgresso(aluno).then(data => {
      setConceitos(data.modulos);
    }).catch(err => {
      console.error(err);
    });
  }, [navigate]);

  const handleAbrirResumo = async (modulo) => {
    if (modulo.status === 'bloqueado') return;
    
    setLoadingResumo(true);
    setResumoAtual({ nome: modulo.conceito, texto: null }); // mostra o skeleton
    
    try {
      const data = await obterResumoTeoria(nome, modulo.conceito_id);
      setResumoAtual({ nome: modulo.conceito, texto: data.resumo });
    } catch (err) {
      console.error(err);
      setResumoAtual({ nome: modulo.conceito, texto: "Erro ao buscar resumo." });
    } finally {
      setLoadingResumo(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-6 animate-in fade-in duration-500">
      
      {/* Menu Lateral de Conceitos */}
      <div className="w-full md:w-1/3 bg-dark-800 border border-dark-600 rounded-2xl p-6 flex flex-col min-h-[500px]">
        <div className="flex items-center gap-3 mb-6">
          <BookOpen className="text-brand-500" size={28} />
          <h2 className="text-xl font-bold text-white">Módulos</h2>
        </div>
        
        <div className="space-y-3 flex-1 overflow-y-auto pr-2">
          {conceitos.map((c) => (
            <button
              key={c.conceito_id}
              onClick={() => handleAbrirResumo(c)}
              disabled={c.status === 'bloqueado'}
              className={`w-full text-left p-4 rounded-xl border transition flex items-center justify-between
                ${c.status === 'bloqueado'
                  ? 'bg-dark-900 border-dark-700 opacity-60 cursor-not-allowed' 
                  : resumoAtual?.nome === c.conceito
                    ? 'bg-brand-500/10 border-brand-500/50 text-brand-300'
                    : 'bg-dark-700/50 border-dark-600 hover:bg-dark-700 hover:border-brand-500/30'
                }
              `}
            >
              <div>
                <span className={`font-semibold ${c.status === 'bloqueado' ? 'text-slate-500' : 'text-slate-200'}`}>
                  {c.conceito}
                </span>
              </div>
              {c.status === 'bloqueado' ? (
                <Lock size={18} className="text-slate-500" />
              ) : (
                <ChevronRight size={18} className={resumoAtual?.nome === c.conceito ? 'text-brand-400' : 'text-slate-400'} />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Painel de Leitura */}
      <div className="w-full md:w-2/3 bg-dark-800 border border-dark-600 rounded-2xl p-8 min-h-[500px] flex flex-col relative overflow-hidden">
        {!resumoAtual ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-center">
            <GraduationCap size={64} className="mb-4 opacity-50" />
            <h3 className="text-xl font-medium mb-2">Biblioteca do Conhecimento</h3>
            <p className="max-w-xs">Selecione um módulo desbloqueado ao lado para gerar um resumo dinâmico via IA.</p>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto">
            <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400 mb-8 pb-4 border-b border-dark-600">
              {resumoAtual.nome}
            </h1>
            
            {loadingResumo && !resumoAtual.texto ? (
              <div className="space-y-4 animate-pulse">
                <div className="h-4 bg-dark-600 rounded w-3/4"></div>
                <div className="h-4 bg-dark-600 rounded w-full"></div>
                <div className="h-4 bg-dark-600 rounded w-5/6"></div>
                <div className="h-4 bg-dark-600 rounded w-full mb-8"></div>
                
                <div className="h-8 bg-dark-600 rounded w-1/3 mb-4"></div>
                <div className="h-32 bg-dark-600 rounded-xl w-full"></div>
                
                <p className="text-brand-500 font-medium mt-6">A Inteligência Artificial está escrevendo o seu resumo...</p>
              </div>
            ) : (
              <div className="prose prose-invert prose-brand max-w-none">
                <ReactMarkdown>{resumoAtual.texto}</ReactMarkdown>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
