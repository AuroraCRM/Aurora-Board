import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import TaskCard from './TaskCard';
import { Task, Status } from '../types';

interface ColumnProps {
  columnId: Status; // Usar o tipo Status como ID da coluna
  title: string;
  tasks: Task[];
}

const Column: React.FC<ColumnProps> = ({ columnId, title, tasks }) => {
  return (
    <div className="bg-gray-100 p-4 rounded-lg shadow-md w-80 flex-shrink-0 mr-4">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">{title}</h2>
      <Droppable droppableId={columnId}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`min-h-[400px] p-3 transition-colors duration-200 ease-in-out rounded-b-md ${ // Adicionado p-3 e rounded-b-md
              snapshot.isDraggingOver ? 'bg-sky-100' : 'bg-gray-100' // Mudado para sky-100 para um azul mais suave
            }`}
          >
            {tasks.map((task, index) => (
              <Draggable key={task.id} draggableId={task.id} index={index}>
                {(providedDraggable, snapshotDraggable) => (
                  <div
                    ref={providedDraggable.innerRef}
                    {...providedDraggable.draggableProps}
                    {...providedDraggable.dragHandleProps}
                    className={`mb-2 ${snapshotDraggable.isDragging ? 'opacity-80 shadow-lg' : ''}`}
                  >
                    <TaskCard task={task} index={index} />
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
};

export default Column;
