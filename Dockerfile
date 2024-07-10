FROM python:3-slim

ENV PYTHONUNBUFFERED 1
ENV PATH="/py/bin:$PATH"
ENV HF_HOME="/vol/cache/huggingface"

# Ensure /tmp directory exists and is writable, and set working directory
RUN mkdir -p /tmp && chmod 1777 /tmp && mkdir -p /project_root_directory

WORKDIR /project_root_directory

# Install system dependencies and create virtual environment
RUN apt update && apt install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        libc6-dev && \
    python -m venv /py && /py/bin/pip install --upgrade pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache if requirements haven't changed
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Install Python dependencies
RUN /py/bin/pip install -r /tmp/requirements.txt

# Install development dependencies conditionally
ARG DEV=false
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi

# Clean up unnecessary packages and files
RUN apt purge -y --auto-remove build-essential libpq-dev libc6-dev && \
    apt clean && rm -rf /tmp/* /var/tmp/*

# Copy project files
COPY ./project_root_directory /project_root_directory

# Add and configure django user
RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/cache/huggingface && \
    mkdir -p /vol/cache/gpt4all && \
    mkdir -p /vol/cache/llama3 && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Expose the port
EXPOSE 8000

# Switch to non-root user
USER django-user
