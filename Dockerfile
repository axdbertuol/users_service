# Use the official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry install --no-root

# Copy the application code into the container
COPY . /app
COPY .env /app/
# Expose port 3336 to the outside world
EXPOSE 3336

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3336"]
