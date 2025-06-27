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
RUN pip install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root

# 5. Copy Application Code
# This path is corrected to look inside the 'src' directory.
COPY ./src/api /app/api

# 6. Expose Port
# This is just metadata. The actual port is set in the CMD line.
EXPOSE 8080

# 7. Define Run Command
# This now uses the "shell form" of CMD to correctly expand the $PORT variable.
CMD poetry run uvicorn api.server:app --host 0.0.0.0 --port $PORT
