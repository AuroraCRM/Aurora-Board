import React from 'react';

export default function Hero() {
  return (
    <section className="bg-black text-white py-24 px-8 md:px-16">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
          Sua empresa. Mais inteligente. Mais sensível.
        </h1>
        <p className="text-lg md:text-xl text-gray-300 leading-relaxed">
          Aurora atua como uma IA parceira, sentindo padrões e antecipando necessidades para que você decida com confiança.
        </p>
      </div>
    </section>
  );
}
