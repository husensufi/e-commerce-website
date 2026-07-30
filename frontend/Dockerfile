# ── Stage: Development ────────────────────────────────────────────────────────
FROM node:18-alpine

WORKDIR /app

# Copy package files first (cached layer)
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy source (overridden by volume mount in docker-compose for hot-reload)
COPY . .

EXPOSE 5173

# --host 0.0.0.0 makes Vite listen on all interfaces so Docker port mapping works
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
