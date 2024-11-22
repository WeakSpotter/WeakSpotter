# Build stage
FROM node:20-slim AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Add commit hash as an environment variable
ARG COMMIT_HASH
ENV COMMIT_HASH=${COMMIT_HASH}

ENV ENV=production

# Copy built assets from builder stage to nginx directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

COPY 11-only-serve-root.sh 21-generate-config-js.sh /docker-entrypoint.d/
RUN chmod +x docker-entrypoint.d -R && dos2unix /docker-entrypoint.d/*
