import React from 'react';
import { Task } from '../types'; // Importa a interface Task

interface TaskCardProps {
  task: Task;
  index: number; // Necessário para react-beautiful-dnd Draggable
}

const TaskCard: React.FC<TaskCardProps> = ({ task, index }) => {
  // A prop index é usada por react-beautiful-dnd, mas não diretamente na renderização aqui.
  // O aviso pode ser removido se a prop index sempre for fornecida corretamente.
  // if (index === undefined) {
  //   console.warn("TaskCard: index prop is undefined. This is required for react-beautiful-dnd.");
  // }

  return (
    <div
      className="bg-white p-3 rounded-md shadow border border-gray-200 hover:shadow-lg transition-shadow duration-150 ease-in-out"
      // mb-4 removido, será controlado pelo container no Column.tsx
    >
      <h3 className="font-semibold text-slate-700 mb-1 text-base">{task.title}</h3>
      <p className="text-sm text-gray-600 mb-2">{task.description}</p>
      <div className="text-xs text-gray-500">
        <span>ID: {task.id}</span> | <span>Assignee: {task.assignee}</span>
      </div>
    </div>
  );
};

export default TaskCard;
