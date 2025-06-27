# In aegis-code/Dockerfile

# 1. Base Image
# Use an official Python runtime as a parent image.
# The slim-bullseye version is a good balance of size and functionality.
FROM python:3.11-slim-bullseye

# 2. Set Environment Variables
# Prevents Python from writing pyc files to disc (improves performance in containers)
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures Python output is sent straight to the terminal without being buffered
ENV PYTHONUNBUFFERED 1

# 3. Set Working Directory
# All subsequent commands will be run from this directory
WORKDIR /app

# 4. Install Dependencies
# First, copy only the dependency definition file to leverage Docker's layer caching.
# This layer will only be re-built if pyproject.toml changes.
COPY pyproject.toml poetry.lock* ./

# Install poetry and then the project dependencies.
# We use --no-root to avoid installing the project itself in editable mode.
# We also use a virtual environment within the project for better isolation.
RUN pip install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

# 5. Copy Application Code
# Copy the rest of the application source code into the container.
COPY ./api /app/api

# 6. Expose Port
# The port that the container will listen on.
# FastAPI's default server (Uvicorn) runs on port 8000.
EXPOSE 8000

# 7. Define Run Command
# The command to run when the container starts.
# We use poetry to run uvicorn.
# --host 0.0.0.0 makes the server accessible from outside the container.
# --port 8000 matches the exposed port.
CMD ["poetry", "run", "uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
