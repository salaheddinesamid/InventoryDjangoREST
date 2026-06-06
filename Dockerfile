FROM python:3.12-slim

# Prevent Python from creating pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Force Python output to stdout
ENV PYTHONUNBUFFERED=1


# Set up the working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency files
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Copy the project in the workinf directory
COPY . .


# Expose the port 8000
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]