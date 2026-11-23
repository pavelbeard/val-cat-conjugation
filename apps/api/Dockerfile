# Imagen de desarrollo para @vcc/api (Express + Mongoose).
# Contexto de build: la raíz del monorepo (ver docker-compose.yml).
FROM node:24-alpine

RUN corepack enable && corepack prepare pnpm@10.17.1 --activate

WORKDIR /app

# Solo las dependencias del paquete @vcc/api y sus dependencias del workspace
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY apps/api/package.json apps/api/
RUN pnpm install --frozen-lockfile --filter @vcc/api...

# Código fuente y dump (para `pnpm import:dump`)
COPY apps/api apps/api
COPY dump dump

EXPOSE 3001
CMD ["pnpm", "--filter", "@vcc/api", "dev"]
