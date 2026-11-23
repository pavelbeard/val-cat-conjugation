# Imagen de desarrollo para @vcc/web (Vite + React + TanStack Router).
# Contexto de build: la raíz del monorepo (ver docker-compose.yml).
FROM node:24-alpine

RUN corepack enable && corepack prepare pnpm@10.17.1 --activate

WORKDIR /app

# Solo las dependencias del paquete @vcc/web y sus dependencias del workspace
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY apps/web/package.json apps/web/
RUN pnpm install --frozen-lockfile --filter @vcc/web...

COPY apps/web apps/web

EXPOSE 5173
CMD ["pnpm", "--filter", "@vcc/web", "dev", "--", "--host", "0.0.0.0"]
