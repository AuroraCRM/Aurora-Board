export interface Task {
  id: string;
  title: string;
  description: string;
  status: string; // "Backlog", "Em Andamento", "Em Revisão", "Concluído"
  assignee: string;
}

// Futuramente, podemos adicionar outros tipos aqui, como para Colunas, etc.
export type Status = "Backlog" | "Em Andamento" | "Em Revisão" | "Concluído";

export const STATUS_MAP: Record<Status, string> = {
  "Backlog": "Backlog",
  "Em Andamento": "Em Andamento",
  "Em Revisão": "Em Revisão",
  "Concluído": "Concluído",
};

export const STATUS_ORDER: Status[] = ["Backlog", "Em Andamento", "Em Revisão", "Concluído"];
