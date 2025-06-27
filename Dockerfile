# In aegis-code/Dockerfile

# 1. Base Image
FROM python:3.11-slim-bullseye

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set Working Directory
WORKDIR /app

# 4. Install Dependencies
# Copy all necessary files for dependency installation.
COPY pyproject.toml poetry.lock* LICENSE* ./

# Install poetry and then the project dependencies.
# The --no-dev flag is corrected to the modern --without dev.
RUN pip install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --without dev

# 5. Copy Application Code
# This path is corrected to look inside the 'src' directory.
COPY ./src/api /app/api

# 6. Expose Port
EXPOSE 8000

# 7. Define Run Command
# The command to run when the container starts.
CMD ["poetry", "run", "uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
