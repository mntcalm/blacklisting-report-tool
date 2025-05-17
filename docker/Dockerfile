FROM python:3.11-slim

# Опционально: установка зависимостей, если нужно что-то системное
#RUN apt-get update && apt-get install -y --no-install-recommends \
#        build-essential \
#    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем само приложение
COPY cmp_report.py .

# Чистим кэш pip (если что-то осталось)
RUN rm -rf /root/.cache

# Указываем, как запускать (можно переопределить в docker-compose)
CMD ["python", "cmp_report.py"]
