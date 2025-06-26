import React from 'react';
import { DragDropContext, DropResult } from 'react-beautiful-dnd';
import Column from './Column';
import { Task, Status, STATUS_ORDER, STATUS_MAP } from '../types';

interface BoardProps {
  tasks: Task[];
  onDragEnd: (result: DropResult) => void; // Callback para App.tsx lidar com a lógica de mover
}

const Board: React.FC<BoardProps> = ({ tasks, onDragEnd }) => {
  // Organiza as tarefas por status
  const columnsData = STATUS_ORDER.reduce((acc, statusKey) => {
    acc[statusKey] = tasks.filter(task => task.status === statusKey);
    return acc;
  }, {} as Record<Status, Task[]>);

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex p-4 space-x-4 bg-gray-50 min-h-screen overflow-x-auto">
        {STATUS_ORDER.map(statusKey => {
          const columnTasks = columnsData[statusKey];
          const columnTitle = STATUS_MAP[statusKey];
          return (
            <Column
              key={statusKey}
              columnId={statusKey}
              title={columnTitle}
              tasks={columnTasks}
            />
          );
        })}
      </div>
    </DragDropContext>
  );
};

export default Board;
