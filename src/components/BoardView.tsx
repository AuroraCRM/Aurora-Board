// src/components/BoardView.tsx
import React, { useEffect } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';
import { useBoardStore } from '../stores/boardStore';
import Column from './Column';

const BoardView: React.FC = () => {
  const { columns, loadBoard, moveCard } = useBoardStore();

  useEffect(() => {
    loadBoard();
  }, [loadBoard]);

  const onDragEnd = (result: DropResult) => {
    const { source, destination, draggableId } = result;

    if (!destination) {
      return;
    }

    moveCard(
      draggableId,
      source.droppableId,
      destination.droppableId,
      source.index,
      destination.index
    );
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex space-x-4 p-4 bg-gray-100 min-h-screen">
        {columns.map((column) => (
          <Column key={column.id} column={column} />
        ))}
      </div>
    </DragDropContext>
  );
};

export default BoardView;