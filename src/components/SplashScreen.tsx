// src/components/SplashScreen.tsx

import React, { useState } from 'react';

type SplashScreenProps = {
  onVideoEnd: () => void;
};

const SplashScreen = ({ onVideoEnd }: SplashScreenProps) => {
  const [isFadingOut, setIsFadingOut] = useState(false);

  const handleVideoEnd = () => {
    setIsFadingOut(true);
    setTimeout(onVideoEnd, 1000); 
  };

  return (
    <div 
      // A classe w-full substitui w-screen para evitar a barra de rolagem horizontal
      className={`fixed top-0 left-0 w-full h-full bg-black z-50 transition-opacity duration-1000 ${isFadingOut ? 'opacity-0' : 'opacity-100'}`}
    >
      <video
        autoPlay
        muted
        playsInline
        preload="auto" // Novo atributo para sugerir o carregamento imediato
        onEnded={handleVideoEnd}
        className="w-full h-full object-cover"
      >
        <source src="/Video_script_8_202506251739.mp4" type="video/mp4" />
        Seu navegador não suporta o vídeo de abertura.
      </video>
      
      {/* O overlay foi REMOVIDO TEMPORARIAMENTE para este teste */}
      
    </div>
  );
};

export default SplashScreen;