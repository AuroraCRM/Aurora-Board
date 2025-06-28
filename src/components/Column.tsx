// src/components/Column.tsx
import React from 'react';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import { Column as ColumnType } from '../stores/boardStore';
import Card from './Card';

interface ColumnProps {
  column: ColumnType;
}

const Column: React.FC<ColumnProps> = ({ column }) => {
  return (
    <div className="bg-gray-200 rounded-lg p-2 w-80 flex-shrink-0">
      <h2 className="font-bold text-lg mb-2 px-2">{column.title}</h2>
      <Droppable droppableId={column.id} type="card">
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`min-h-[100px] transition-colors duration-200 ${snapshot.isDraggingOver ? 'bg-blue-100' : ''}`}>
            {column.cards.map((card, index) => (
              <Card key={card.id} card={card} index={index} />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
};

export default Column;