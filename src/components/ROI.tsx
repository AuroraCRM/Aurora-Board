import React from 'react';

export default function ROI() {
  return (
    <section className="bg-black text-white py-24 px-8 md:px-16">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold leading-tight mb-12">
          O Impacto da Conexão (ROI)
        </h2>

        <div className="space-y-12">
          <div>
            <h3 className="text-2xl font-semibold mb-2">Vendas (B2B)</h3>
            <p className="text-lg text-gray-300">
              Vendedores que antecipam as objeções não ditas de um cliente e entendem seu real sentimento, fecham negócios 30% maiores e em menos tempo.
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-semibold mb-2">Jurídico</h3>
            <p className="text-lg text-gray-300">
              Advogados que automatizam a revisão de milhares de documentos e comunicações encontram evidências e cláusulas cruciais 10x mais rápido, reduzindo drasticamente os custos de e-discovery e mitigando riscos.
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-semibold mb-2">Setor Público (B2G)</h3>
            <p className="text-lg text-gray-300">
              Gestores que transformam o feedback disperso dos cidadãos em insights claros aumentam a transparência, otimizam a alocação de recursos e melhoram a eficiência na entrega de serviços essenciais.
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-semibold mb-2">Suporte ao Cliente</h3>
            <p className="text-lg text-gray-300">
              Equipes que detectam a frustração latente em um cliente antes que ela se torne uma queixa formal aumentam a retenção e o lifetime value (LTV) em até 25%.
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-semibold mb-2">Liderança Estratégica</h3>
            <p className="text-lg text-gray-300">
              Executivos que compreendem a dinâmica real de suas equipes a partir de todas as interações tomam decisões estratégicas 2x mais rápido e com um nível de confiança sem precedentes.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
