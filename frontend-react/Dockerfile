# React Frontend Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend-react/package*.json ./

# Install dependencies
RUN npm install --omit=dev

# Copy source code
COPY frontend-react/ ./

# Set build-time environment variables
ARG REACT_APP_BACKEND_URL
ARG REACT_APP_MOCK_API_URL
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
ENV REACT_APP_MOCK_API_URL=$REACT_APP_MOCK_API_URL

# Build the app
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]
