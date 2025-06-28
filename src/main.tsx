import React, { Suspense } from 'react'; // Adicionado Suspense
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend';

i18n
  .use(HttpBackend) // Usa o backend para carregar traduções
  .use(initReactI18next) // Passa a instância i18n para react-i18next
  .init({
    // backend: {
    //   loadPath: '/locales/{{lng}}/{{ns}}.json' // Caminho para os arquivos de tradução na pasta public
    // },
    // O HttpBackend por padrão tentará carregar de /locales/{{lng}}/{{ns}}.json
    // Se seus arquivos estão em public/locales/en/translation.json, etc.
    // o Astro deve servir a pasta 'public' na raiz, então /locales/... deve funcionar.
    lng: 'pt', // Idioma padrão
    fallbackLng: 'pt', // Idioma de fallback se a tradução não for encontrada
    supportedLngs: ['pt', 'en', 'es'], // Idiomas suportados
    ns: ['translation'], // Namespaces (padrão é 'translation')
    defaultNS: 'translation',
    interpolation: {
      escapeValue: false, // React já faz o escape por padrão
    },
    debug: import.meta.env.DEV, // Ativa logs de debug em desenvolvimento
  });

// Renderiza a aplicação após a inicialização do i18n (é assíncrono com HttpBackend)
// O Suspense é usado para lidar com o carregamento das traduções
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Suspense fallback="Carregando traduções...">
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Suspense>
  </React.StrictMode>
);
