import React from 'react';

export default function ROI() {
  return (
    <section className="bg-black text-white py-20 px-6 md:px-20">
      <div className="max-w-5xl mx-auto space-y-10">
        <h2 className="text-3xl md:text-4xl font-semibold">O Impacto da Conexão</h2>
        <div className="space-y-8">
          <div>
            <h3 className="text-2xl font-medium">Vendas (B2B)</h3>
            <p className="text-gray-300">Vendedores que antecipam as emoções fecham negócios maiores em menos tempo.</p>
          </div>
          <div>
            <h3 className="text-2xl font-medium">Jurídico</h3>
            <p className="text-gray-300">Advogados que automatizam a revisão de documentos identificam riscos 10x mais rápido.</p>
          </div>
          <div>
            <h3 className="text-2xl font-medium">Setor Público (B2G)</h3>
            <p className="text-gray-300">Gestores que transformam feedback em insights otimizam serviços essenciais.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
