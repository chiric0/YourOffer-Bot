# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директорию для документов
RUN mkdir -p Documents

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Запускаем бота
CMD ["python", "main_bot.py"] 