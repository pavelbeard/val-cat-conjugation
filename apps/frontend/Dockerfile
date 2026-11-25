# Imagen de desarrollo para @vcc/frontend (Vite + React + TanStack Router).
# Contexto de build: la raíz del monorepo (ver docker-compose.yml).
FROM node:24-alpine

RUN corepack enable && corepack prepare pnpm@10.17.1 --activate

WORKDIR /app

# Solo las dependencias del paquete @vcc/frontend y sus dependencias del workspace
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY apps/frontend/package.json apps/frontend/
COPY packages/web-builder/package.json packages/web-builder/
RUN pnpm install --frozen-lockfile --filter @vcc/frontend...

COPY apps/frontend apps/frontend

EXPOSE 5173
CMD ["pnpm", "--filter", "@vcc/frontend", "dev", "--", "--host", "0.0.0.0"]
