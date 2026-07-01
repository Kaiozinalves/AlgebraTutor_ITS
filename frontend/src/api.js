import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const iniciarSessao = async (nome) => {
    const res = await axios.post(`${API_URL}/iniciar`, { nome });
    return res.data;
};

export const obterProximaQuestao = async (nome, conceitoId = null, nivelMaximo = null) => {
    let url = `${API_URL}/proxima/${nome}?`;
    if (conceitoId) {
        url += `conceito_id=${conceitoId}&`;
    }
    if (nivelMaximo) {
        url += `nivel_maximo=${nivelMaximo}&`;
    }
    const res = await axios.get(url);
    return res.data;
};

export const responderQuestao = async (nome, questaoId, respostaLog, usouDica = false) => {
    const res = await axios.post(`${API_URL}/responder`, {
        nome_aluno: nome,
        questao_id: questaoId,
        resposta: respostaLog,
        usou_dica: usouDica
    });
    return res.data;
};

export const obterResumoTeoria = async (nome, conceitoId) => {
    const res = await axios.get(`${API_URL}/resumo/${nome}/${conceitoId}`);
    return res.data;
};

export const obterProgresso = async (nome) => {
    const res = await axios.get(`${API_URL}/progresso/${nome}`);
    return res.data;
};

export const enviarDuvida = async (enunciado, duvida) => {
    const res = await axios.post(`${API_URL}/duvida`, { enunciado, duvida });
    return res.data;
};
