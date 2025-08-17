# Dockerfile for Background Agents - Enhanced QnA Agent System
FROM python:3.9-slim

# Set up user and working directory
RUN useradd -m -s /bin/bash ubuntu
USER ubuntu
WORKDIR /home/ubuntu

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    wget \
    git \
    postgresql-client \
    nodejs \
    npm \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Switch back to ubuntu user
USER ubuntu

# Install uv (Python package manager used by this project)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/ubuntu/.cargo/bin:$PATH"

# Install Node.js version manager (nvm) for React frontend development
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR="/home/ubuntu/.nvm"
RUN . "$NVM_DIR/nvm.sh" && nvm install 18 && nvm use 18

# Set up shell environment
RUN echo 'export PATH="/home/ubuntu/.cargo/bin:$PATH"' >> ~/.bashrc
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
RUN echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
RUN echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc

# Create common development directories
RUN mkdir -p /home/ubuntu/projects
RUN mkdir -p /home/ubuntu/.ssh
RUN mkdir -p /home/ubuntu/.config

# Set proper permissions
USER root
RUN chown -R ubuntu:ubuntu /home/ubuntu
USER ubuntu

# Default shell
CMD ["/bin/bash"]