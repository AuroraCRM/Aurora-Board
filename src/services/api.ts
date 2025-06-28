// src/services/api.ts
import axios from 'axios';
import { Column, Card } from '../stores/boardStore';

const api = axios.create({
  baseURL: 'http://localhost:3000', // Assumindo que o backend roda na porta 3000
});

// Interceptor para adicionar o token JWT a cada requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros 401 (Unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('authToken');
      // Força o recarregamento da página para redirecionar ao login
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const login = async (username: string, password: string): Promise<void> => {
  const response = await api.post('/auth/token', { username, password });
  const { token } = response.data;
  if (token) {
    localStorage.setItem('authToken', token);
  }
};

// Funções da API para o board
export const fetchBoardData = async (): Promise<Column[]> => {
  const response = await api.get('/boards'); // Endpoint para buscar o board completo
  return response.data;
};

export const updateCardPosition = async (cardId: string, newColumnId: string, newIndex: number): Promise<void> => {
  // O endpoint pode variar, ex: /cards/:cardId/move
  await api.put(`/cards/${cardId}/move`, { newColumnId, newIndex });
};

export const addCardToColumn = async (columnId: string, cardData: { title: string; description: string }): Promise<Card> => {
  const response = await api.post(`/columns/${columnId}/cards`, cardData);
  return response.data;
};

export const updateExistingCard = async (card: Card): Promise<Card> => {
  const response = await api.put(`/cards/${card.id}`, { title: card.title, description: card.description });
  return response.data;
};

export default api;