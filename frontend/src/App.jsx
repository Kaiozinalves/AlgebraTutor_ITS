import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { BookOpen } from 'lucide-react';
import Login from './pages/Login';
import Exercicio from './pages/Exercicio';
import Progresso from './pages/Progresso';
import Teoria from './pages/Teoria';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-dark-900 text-slate-100 selection:bg-brand-500 selection:text-white flex flex-col">
        <header className="border-b border-dark-700 bg-dark-800/50 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
            <h1 className="text-xl font-bold bg-gradient-to-r from-brand-500 to-emerald-300 bg-clip-text text-transparent">
              ITS Álgebra Básica
            </h1>
            <div className="flex gap-4">
              <a href="/teoria" className="text-sm text-slate-400 hover:text-brand-400 transition-colors flex items-center gap-1"><BookOpen size={16} /> Biblioteca</a>
              <a href="/progresso" className="text-sm text-slate-400 hover:text-brand-400 transition-colors">Progresso</a>
              <a href="/exercicio" className="text-sm text-slate-400 hover:text-brand-400 transition-colors">Praticar</a>
            </div>
          </div>
        </header>
        
        <main className="flex-1 flex flex-col max-w-5xl mx-auto w-full p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/exercicio" element={<Exercicio />} />
            <Route path="/progresso" element={<Progresso />} />
            <Route path="/teoria" element={<Teoria />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
