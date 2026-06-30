import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { obterProximaQuestao, responderQuestao, enviarDuvida } from '../api';
import { CheckCircle2, XCircle, ChevronRight, BrainCircuit, MessageCircle, Send, LogOut } from 'lucide-react';

function Exercicio() {
  const [nome, setNome] = useState('');
  const [questao, setQuestao] = useState(null);
  const [ofensiva, setOfensiva] = useState(0);
  const [questoesHoje, setQuestoesHoje] = useState(0);
  const [resposta, setResposta] = useState('');
  const [loading, setLoading] = useState(true);
  const [mostrarResposta, setMostrarResposta] = useState(false);
  
  // Chat Tutor
  const [duvidaAberto, setDuvidaAberto] = useState(false);
  const [textoDuvida, setTextoDuvida] = useState('');
  const [respostaDuvida, setRespostaDuvida] = useState('');
  const [loadingDuvida, setLoadingDuvida] = useState(false);
  const [usouDica, setUsouDica] = useState(false);

  const [feedback, setFeedback] = useState(null);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const conceitoId = searchParams.get('conceito');

  useEffect(() => {
    const aluno = localStorage.getItem('aluno_nome');
    if (!aluno) {
      navigate('/');
      return;
    }
    setNome(aluno);
    carregarQuestao(aluno);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('aluno_nome');
    navigate('/');
  };

  const carregarQuestao = async (aluno) => {
    setLoading(true);
    setFeedback(null);
    setResposta('');
    setMostrarResposta(false);
    setDuvidaAberto(false);
    setTextoDuvida('');
    setRespostaDuvida('');
    setUsouDica(false);
    
    try {
      const data = await obterProximaQuestao(aluno, conceitoId);
      if (data.ofensiva !== undefined) {
        setOfensiva(data.ofensiva);
      }
      
      if (data.mensagem) {
        setQuestao(null); // Concluído
      } else {
        setQuestao(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResponder = async (e) => {
    e.preventDefault();
    if (!resposta.trim()) return;
    
    const ans = parseFloat(resposta.replace(',', '.'));
    if (isNaN(ans)) {
      alert("Por favor, digite um número válido.");
      return;
    }

    setLoading(true);
    try {
      const res = await responderQuestao(nome, questao.questao_id, ans, usouDica);
      setFeedback(res);
      if (res.questoes_hoje !== undefined) {
        setQuestoesHoje(res.questoes_hoje);
        // Atualiza a ofensiva na interface caso ele tenha batido a meta agora
        if (res.questoes_hoje === 5) {
          setOfensiva(prev => prev + 1);
        }
      }
    } catch (err) {
      console.error(err);
      alert('Erro ao enviar resposta');
    } finally {
      setLoading(false);
    }
  };

  const handleDuvida = async (e) => {
    e.preventDefault();
    if (!textoDuvida.trim()) return;
    
    setUsouDica(true);
    setLoadingDuvida(true);
    try {
      const res = await enviarDuvida(questao.enunciado, textoDuvida);
      setRespostaDuvida(res.resposta_ia);
    } catch (err) {
      console.error(err);
      setRespostaDuvida("Erro ao tentar contatar o professor. Verifique se a chave do Gemini está configurada.");
    } finally {
      setLoadingDuvida(false);
    }
  };

  if (loading && !feedback) {
    return (
      <div className="flex-1 flex items-center justify-center text-slate-400 gap-2">
        <BrainCircuit className="animate-pulse" size={24} /> Carregando próxima questão...
      </div>
    );
  }

  if (!questao && !loading && !feedback) {
    return (
      <div className="flex-1 flex items-center justify-center flex-col gap-6">
        <div className="w-20 h-20 bg-brand-500/20 text-brand-400 rounded-full flex items-center justify-center">
          <CheckCircle2 size={40} />
        </div>
        <h2 className="text-3xl font-bold">Parabéns, {nome}!</h2>
        <p className="text-slate-400">
          {conceitoId ? "Você já respondeu ou re-revisou as questões desse módulo." : "Você concluiu todos os conteúdos de álgebra básica."}
        </p>
        <button onClick={() => navigate('/progresso')} className="px-6 py-3 bg-brand-500 rounded-xl font-semibold hover:bg-brand-600 transition">
          Ver meu progresso
        </button>
      </div>
    );
  }

  return (
    <div className="flex-1 max-w-2xl mx-auto w-full flex flex-col pt-4 sm:pt-8">
      <div className="flex justify-between items-center mb-4">
        <div className="flex gap-2">
          <div className="px-3 py-1 bg-brand-500/10 border border-brand-500/30 rounded-lg flex items-center gap-1">
            <span className="text-brand-400 font-bold text-sm">🎯 {Math.min(questoesHoje, 5)}/5</span>
          </div>
          {ofensiva > 0 && (
            <div className="px-3 py-1 bg-orange-500/10 border border-orange-500/30 rounded-lg flex items-center gap-1">
              <span className="text-orange-500 font-bold text-sm">🔥 {ofensiva} Dia{ofensiva > 1 ? 's' : ''}</span>
            </div>
          )}
        </div>
        <button onClick={handleLogout} className="text-slate-500 hover:text-slate-300 transition flex items-center gap-1 text-sm bg-dark-800 px-3 py-1.5 rounded-lg">
          <LogOut size={14} /> Trocar de Aluno
        </button>
      </div>

      {questao && !feedback && (
        <div className="glass-panel p-6 sm:p-8 rounded-2xl animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="inline-block px-3 py-1 bg-dark-700 text-brand-300 text-xs font-semibold rounded-full mb-4">
            {questao.conceito} (Nível {questao.dificuldade})
          </div>
          <h2 className="text-2xl font-semibold leading-relaxed mb-8">
            {questao.enunciado}
          </h2>
          
          <form onSubmit={handleResponder} className="flex gap-4">
            <input
              type="text"
              placeholder="Digite o número (ex: 3.14)"
              value={resposta}
              onChange={(e) => setResposta(e.target.value)}
              className="flex-1 px-4 py-3 bg-dark-900 border border-dark-700 rounded-xl focus:outline-none focus:border-brand-500 transition-all text-lg"
              autoFocus
            />
            <button
              type="submit"
              disabled={loading || !resposta.trim()}
              className="px-8 py-3 bg-brand-500 hover:bg-brand-600 font-semibold rounded-xl transition disabled:opacity-50"
            >
              Responder
            </button>
          </form>

          {/* Chat Contextual */}
          <div className="mt-8 border-t border-dark-700 pt-6">
            {!duvidaAberto ? (
              <button 
                onClick={() => setDuvidaAberto(true)}
                type="button"
                className="flex items-center gap-2 text-slate-400 hover:text-brand-400 transition text-sm font-medium"
              >
                <MessageCircle size={18} /> Precisa de ajuda com um passo?
              </button>
            ) : (
              <div className="animate-in fade-in slide-in-from-top-2">
                <h3 className="text-sm font-semibold text-brand-300 flex items-center gap-2 mb-3">
                  <MessageCircle size={18} /> Pergunte ao Tutor IA
                </h3>
                
                <form onSubmit={handleDuvida} className="flex gap-3 mb-4">
                  <input
                    type="text"
                    placeholder="Ex: Não entendi o que fazer com o sinal negativo..."
                    value={textoDuvida}
                    onChange={(e) => setTextoDuvida(e.target.value)}
                    className="flex-1 px-4 py-2 bg-dark-900 border border-dark-700 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                  />
                  <button
                    type="submit"
                    disabled={loadingDuvida || !textoDuvida.trim()}
                    className="px-4 py-2 bg-dark-700 hover:bg-dark-600 rounded-lg text-brand-400 transition disabled:opacity-50 flex items-center gap-2"
                  >
                    {loadingDuvida ? <BrainCircuit className="animate-pulse" size={18} /> : <Send size={18} />}
                  </button>
                </form>

                {respostaDuvida && (
                  <div className="p-4 bg-brand-500/10 border border-brand-500/20 rounded-xl text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                    {respostaDuvida}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {feedback && (
        <div className="glass-panel p-6 sm:p-8 rounded-2xl animate-in fade-in zoom-in-95 duration-500">
          <div className="flex items-center gap-4 mb-4">
            {feedback.correto ? (
              <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-500 flex items-center justify-center">
                <CheckCircle2 size={24} />
              </div>
            ) : (
              <div className="w-12 h-12 rounded-full bg-red-500/20 text-red-500 flex items-center justify-center">
                <XCircle size={24} />
              </div>
            )}
            <div>
              <h3 className={`text-xl font-bold ${feedback.correto ? 'text-emerald-500' : 'text-red-500'}`}>
                {feedback.correto ? 'Resposta Correta!' : 'Resposta Incorreta'}
              </h3>
              <p className="text-sm text-slate-400">
                Seu domínio agora é de {(feedback.dominio_atualizado * 100).toFixed(0)}%
              </p>
            </div>
          </div>
          
          <div className="bg-dark-900 p-5 rounded-xl border border-dark-700 mb-6">
            <p className="text-slate-200 leading-relaxed">{feedback.feedback_ia}</p>
          </div>
          
          {!feedback.correto && !mostrarResposta && (
            <button
              onClick={() => setMostrarResposta(true)}
              className="w-full mb-4 py-2 border border-dark-600 text-slate-300 hover:bg-dark-700 font-medium rounded-xl transition"
            >
              Desistir e Mostrar Resposta
            </button>
          )}

          {!feedback.correto && mostrarResposta && (
            <div className="mb-6 space-y-4">
              <div className="p-4 bg-brand-500/10 border border-brand-500/30 rounded-xl">
                <p className="text-brand-300 font-semibold">Gabarito: {feedback.gabarito}</p>
              </div>
              {feedback.resolucao_ia && (
                <div className="p-5 bg-dark-800 border border-dark-600 rounded-xl animate-in fade-in slide-in-from-top-2 duration-500">
                  <h4 className="text-brand-300 font-semibold mb-3 flex items-center gap-2">
                    <BrainCircuit size={18} /> Resolução da IA:
                  </h4>
                  <p className="text-slate-300 whitespace-pre-wrap text-sm leading-relaxed font-mono">
                    {feedback.resolucao_ia}
                  </p>
                </div>
              )}
            </div>
          )}
          
          <button
            onClick={() => carregarQuestao(nome)}
            className="w-full flex items-center justify-center gap-2 py-3 bg-dark-700 hover:bg-dark-600 font-semibold rounded-xl transition"
          >
            Próxima Questão
            <ChevronRight size={20} />
          </button>
        </div>
      )}
    </div>
  );
}

export default Exercicio;
