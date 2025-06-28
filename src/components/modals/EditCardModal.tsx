// src/components/modals/EditCardModal.tsx
import React from 'react';

interface EditCardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (id: string, title: string, description: string) => void;
  card?: {
    id: string;
    title: string;
    description: string;
  };
}

const EditCardModal: React.FC<EditCardModalProps> = ({ isOpen, onClose, onSave, card }) => {
  const [title, setTitle] = React.useState(card?.title || '');
  const [description, setDescription] = React.useState(card?.description || '');

  React.useEffect(() => {
    if (card) {
      setTitle(card.title);
      setDescription(card.description);
    }
  }, [card]);

  const handleSubmit = () => {
    if (card) {
      onSave(card.id, title, description);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-xl font-bold mb-4">Edit Card</h2>
        <div className="mb-4">
          <label htmlFor="edit-title" className="block text-gray-700 text-sm font-bold mb-2">Title</label>
          <input
            type="text"
            id="edit-title"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="edit-description" className="block text-gray-700 text-sm font-bold mb-2">Description</label>
          <textarea
            id="edit-description"
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="flex justify-end">
          <button
            className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-2"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            onClick={handleSubmit}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditCardModal;
