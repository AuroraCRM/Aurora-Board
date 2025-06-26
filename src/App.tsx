import React, { useState, useEffect } from 'react';
import { DropResult } from 'react-beautiful-dnd';
import Board from './components/Board';
import { Task, Status } from './types';
import './App.css'; // Pode ser usado para estilos globais adicionais se necessário

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        // O Vite serve arquivos da pasta `public` diretamente na raiz.
        const response = await fetch('/tasks.json');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Validação simples dos dados recebidos
        if (Array.isArray(data) && data.every(item => item.id && item.title && item.status)) {
          setTasks(data as Task[]);
        } else {
          throw new Error("Formato de tasks.json inválido.");
        }
        setError(null);
      } catch (e) {
        console.error("Falha ao carregar tarefas:", e);
        setError(e instanceof Error ? e.message : String(e));
        setTasks([]); // Garante que tasks seja um array vazio em caso de erro
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const handleDragEnd = (result: DropResult) => {
    const { source, destination, draggableId } = result;

    // Se não houver destino (arrastou para fora de uma área válida)
    if (!destination) {
      return;
    }

    // Se a tarefa foi solta na mesma posição em que começou
    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) {
      return;
    }

    const taskToMove = tasks.find(task => task.id === draggableId);

    if (taskToMove) {
      const newStatus = destination.droppableId as Status;

      // Atualiza o status da tarefa
      const updatedTasks = tasks.map(task =>
        task.id === draggableId ? { ...task, status: newStatus } : task
      );
      setTasks(updatedTasks);

      // Log para depuração
      console.log(`Task ${draggableId} moved from ${source.droppableId} to ${destination.droppableId}`);
      // Para o MVP, não salvamos de volta no tasks.json
    }
  };

  if (loading) {
    return <div className="p-4 text-center">Carregando tarefas...</div>;
  }

  if (error) {
    return <div className="p-4 text-center text-red-500">Erro ao carregar tarefas: {error}</div>;
  }

  if (tasks.length === 0 && !loading && !error) {
    return <div className="p-4 text-center">Nenhuma tarefa encontrada. Verifique o arquivo tasks.json.</div>;
  }

  return (
    <div className="App">
      <header className="bg-blue-600 p-4 shadow-md">
        <h1 className="text-2xl font-bold text-white text-center">Aurora Board</h1>
      </header>
      <Board tasks={tasks} onDragEnd={handleDragEnd} />
    </div>
  );
}

export default App;
