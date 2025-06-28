# Aurora Homepage

Frontend institucional da plataforma Aurora: uma IA sensível, estratégica e co-criadora.  
Construído com **React + Vite + TailwindCSS**, com estrutura modular e foco em UX futurista.

## Estrutura

- `src/pages/` → Páginas do site (ex: Home, Manifesto)
- `src/components/sections/` → Componentes de blocos institucionais
- `scripts/` → Scripts de setup automatizado

## Scripts

```bash
npm run dev        # Inicia o servidor Vite
npm run build      # Gera build para produção
.\scripts\setup-aurora.ps1   # Script de setup no Windows (Codex/Dev)

## Como usar o Gemini CLI

1. **Clone o repositório e instale as dependências:**
   ```bash
   git clone https://github.com/AuroraCRM/aurora-homepage.git
   cd aurora-homepage
   npm install
   ```

2. **Use o REPL do Gemini CLI:**
   Execute o comando abaixo para abrir o REPL (Read-Eval-Print Loop) do Gemini CLI. Isso permite interagir diretamente com o modelo de IA.
   ```bash
   npm run cli
   ```

3. **Use os scripts de geração e ajuste:**
   Para facilitar tarefas comuns, foram criados scripts específicos:
   - `npm run gen:homepage`: Cria ou refina a homepage da Aurora utilizando React e Tailwind.
   - `npm run tweak:hero`: Ajusta o espaçamento da seção Hero (`Hero.tsx`) para melhor visualização em dispositivos móveis.

4. **Configuração da API Key e Contexto:**
   - **API Key:** O Gemini CLI procura a chave da API na variável de ambiente `GEMINI_API_KEY`. Certifique-se de configurá-la no seu ambiente de desenvolvimento.
   - **Contexto de Geração:** O arquivo `GEMINI.md` na raiz do projeto contém instruções e o contexto que o Gemini CLI utiliza para gerar ou modificar código. Você pode editar este arquivo para refinar o comportamento do assistente de IA de acordo com as necessidades do projeto.
