// src/pages/LandingPage.tsx
import React from 'react';
import Login from '../components/Login';

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 text-white">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-4">Bem-vindo ao Aurora Board</h1>
        <p className="text-xl">Sua plataforma de gerenciamento de projetos intuitiva.</p>
      </div>
      <Login />
    </div>
  );
}