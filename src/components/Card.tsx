// src/components/Card.tsx
import React from 'react';
import { Draggable } from 'react-beautiful-dnd';
import { Card as CardType } from '../stores/boardStore';

interface CardProps {
  card: CardType;
  index: number;
}

const Card: React.FC<CardProps> = ({ card, index }) => {
  return (
    <Draggable draggableId={card.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`bg-white rounded-md shadow-md p-4 mb-2 ${snapshot.isDragging ? 'ring-2 ring-purple-500' : ''}`}>
          <h3 className="font-semibold">{card.title}</h3>
          <p className="text-sm text-gray-600">{card.description}</p>
        </div>
      )}
    </Draggable>
  );
};

export default Card;