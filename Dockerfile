# Estágio de build
FROM node:20-alpine AS build

WORKDIR /app

# Copia os arquivos de manifesto de pacotes
COPY package.json pnpm-lock.yaml* ./

# Usando pnpm conforme solicitado
RUN npm install -g pnpm && pnpm install

COPY . .

RUN pnpm run build

# Estágio de produção
FROM nginx:stable-alpine AS production

# Copia os arquivos estáticos gerados no Estágio 1 para o diretório de serviço do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Exponha a porta 80
EXPOSE 80

# Comando padrão para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]