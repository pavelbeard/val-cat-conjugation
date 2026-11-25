# Imagen de desarrollo para @vcc/conjugator (Express + Mongoose).
# Contexto de build: la raíz del monorepo (ver docker-compose.yml).
FROM node:24-alpine

RUN corepack enable && corepack prepare pnpm@10.17.1 --activate

WORKDIR /app

# Solo las dependencias del paquete @vcc/conjugator y sus dependencias del workspace
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY apps/conjugator/package.json apps/conjugator/
COPY packages/api-builder/package.json packages/api-builder/
RUN pnpm install --frozen-lockfile --filter @vcc/conjugator...

# Código fuente y dump (para `pnpm import:dump`)
COPY apps/conjugator apps/conjugator
COPY dump dump

EXPOSE 3001
CMD ["pnpm", "--filter", "@vcc/conjugator", "dev"]
