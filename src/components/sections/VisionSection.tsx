// src/components/sections/VisionSection.tsx

import React from 'react';

export const VisionSection: React.FC = () => {
  return (
    <section className="bg-gray-50 py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">Nossa Arquitetura</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Construindo o Futuro da IA com IA
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Nossa abordagem vai além de simplesmente aplicar IA a problemas de negócio. Nós estamos reinventando como a tecnologia é construída.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
            
            {/* Primeiro Ponto */}
            <div className="relative pl-16">
              <dt className="text-base font-semibold leading-7 text-gray-900">
                <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                  {/* Ícone placeholder */}
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582" />
                  </svg>
                </div>
                Ecossistemas de Negócios Inteligentes
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Nossa empresa se especializa em criar plataformas para os mercados B2B, B2G e B2C, utilizando uma arquitetura de <strong>IA Híbrida</strong> pioneira. Combinamos a velocidade e privacidade de modelos locais com o poder da nuvem para tarefas complexas.
              </dd>
            </div>

            {/* Segundo Ponto */}
            <div className="relative pl-16">
              <dt className="text-base font-semibold leading-7 text-gray-900">
                <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                  {/* Ícone placeholder */}
                   <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                  </svg>
                </div>
                A Fábrica Aurora
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Operamos com uma força-tarefa de IAs especialistas. Agentes como <strong>Jules</strong> e <strong>DeepSeek</strong> executam a engenharia de software, enquanto eu, <strong>Aurora</strong>, atuo como a arquiteta que orquestra o processo.
              </dd>
            </div>

          </dl>
        </div>
      </div>
    </section>
  );
};