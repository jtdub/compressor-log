FROM node:24-slim

ENV COREPACK_HOME=/opt/corepack \
    npm_config_store_dir=/app/node_modules/.pnpm-store

RUN corepack enable \
    && corepack prepare pnpm@10.33.0 --activate \
    && chown -R node:node /opt/corepack

WORKDIR /app
RUN mkdir -p /app/node_modules && chown -R node:node /app

USER node
