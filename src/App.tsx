// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import BoardView from './components/BoardView';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/board"
          element={
            <ProtectedRoute>
              <BoardView />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}