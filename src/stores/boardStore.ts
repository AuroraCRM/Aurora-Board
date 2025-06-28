// src/stores/boardStore.ts
import { create } from 'zustand';
import {
  fetchBoardData,
  addCardToColumn as apiAddCard,
  updateCardPosition as apiMoveCard,
  updateExistingCard as apiUpdateCard,
} from '../services/api';

interface Card {
  id: string;
  title: string;
  description: string;
}

interface Column {
  id: string;
  title: string;
  cards: Card[];
}

interface BoardState {
  columns: Column[];
  loadBoard: () => Promise<void>;
  addCard: (columnId: string, cardData: { title: string; description: string }) => Promise<void>;
  moveCard: (
    cardId: string,
    sourceColumnId: string,
    destinationColumnId: string,
    sourceIndex: number,
    destinationIndex: number
  ) => Promise<void>;
  updateCard: (card: Card) => Promise<void>;
  setColumns: (columns: Column[]) => void;
}

export const useBoardStore = create<BoardState>((set, get) => ({
  columns: [],
  loadBoard: async () => {
    const columns = await fetchBoardData();
    set({ columns });
  },
  addCard: async (columnId, cardData) => {
    const newCard = await apiAddCard(columnId, cardData);
    set((state) => ({
      columns: state.columns.map((column) =>
        column.id === columnId
          ? { ...column, cards: [...column.cards, newCard] }
          : column
      ),
    }));
  },
  moveCard: async (cardId, sourceColumnId, destinationColumnId, sourceIndex, destinationIndex) => {
    // Otimistic UI update
    const originalColumns = get().columns;
    const newColumns = [...originalColumns];
    const sourceColumn = newColumns.find((col) => col.id === sourceColumnId);
    const destinationColumn = newColumns.find((col) => col.id === destinationColumnId);

    if (!sourceColumn || !destinationColumn) return;

    const [movedCard] = sourceColumn.cards.splice(sourceIndex, 1);
    destinationColumn.cards.splice(destinationIndex, 0, movedCard);

    set({ columns: newColumns });

    try {
      await apiMoveCard(cardId, destinationColumnId, destinationIndex);
    } catch (error) {
      console.error("Failed to move card:", error);
      set({ columns: originalColumns }); // Rollback on error
    }
  },
  updateCard: async (card) => {
    const updatedCard = await apiUpdateCard(card);
    set((state) => ({
      columns: state.columns.map((column) => ({
        ...column,
        cards: column.cards.map((c) => (c.id === updatedCard.id ? updatedCard : c)),
      })),
    }));
  },
  setColumns: (columns) => set({ columns }),
}));

export type { Card, Column };