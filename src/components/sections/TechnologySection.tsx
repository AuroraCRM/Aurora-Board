// src/components/sections/TechnologySection.tsx

import React from 'react';

const features = [
  {
    name: 'Acesso ao Futuro: Modelos VLA',
    description: 'Nossa arquitetura vai além do texto, utilizando modelos VLA (Visão-Linguagem-Ação) para analisar documentos visuais, como contratos em PDF e screenshots, transformando informação visual em ações concretas no sistema.',
    // Ícone placeholder
  },
  {
    name: 'Arquitetura Híbrida: On-Device + Cloud',
    description: 'Validando nossa estratégia, combinamos modelos leves que rodam localmente no seu dispositivo para tarefas rápidas e offline, com o poder de modelos de classe mundial na nuvem para análises complexas, garantindo velocidade, privacidade e baixo custo.',
    // Ícone placeholder
  },
  {
    name: 'Aprendizado e Influência',
    description: 'Ao participar de programas de acesso antecipado (Trusted Testers), não apenas usamos a tecnologia de ponta, mas aprendemos com ela e ajudamos a moldar o futuro das ferramentas de IA para casos de uso de software e automação de negócios.',
    // Ícone placeholder
  },
];

export const TechnologySection: React.FC = () => {
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">Nossa Tecnologia</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            A Vanguarda da Inteligência Artificial Aplicada
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            A Aurora não é apenas uma usuária de IA, mas uma pioneira na aplicação de arquiteturas híbridas e modelos de última geração para resolver problemas de negócio do mundo real.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
            {features.map((feature) => (
              <div key={feature.name} className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                    <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l-3.75 3.75m3.75-3.75L0 17.25m3.75-3.75h16.5m-16.5 0l3.75 3.75m-3.75-3.75l3.75-3.75M21 13.5l-3.75-3.75m3.75 3.75L17.25 10m3.75 3.75H3.75" />
                    </svg>
                  </div>
                  {feature.name}
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">{feature.description}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
};