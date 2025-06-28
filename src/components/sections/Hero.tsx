import React from 'react';

export default function Hero() {
  return (
    <section className="relative h-screen flex items-center justify-center text-white bg-cover bg-center" style={{backgroundImage: "url('/aurora-fundo.png')"}}>
      <div className="absolute inset-0 bg-black/50 backdrop-blur-md" />
      <h1 className="relative z-10 text-4xl md:text-6xl font-light text-center px-6">
        E se a sua empresa pudesse sentir?
      </h1>
    </section>
  );
}
