# Базовый образ Python (легковесная версия)
FROM python:3.13.3

# Создаём рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код в контейнер
COPY . .

# Указываем порт
EXPOSE 8080

# Команда, которая будет выполняться при старте контейнера

CMD ["python", "main.py"]
