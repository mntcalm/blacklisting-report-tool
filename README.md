# blacklisting-report-tool
multithread checking IPs on blacklists, HTML-report, 2 modes of script activity (builder and server)

> Многофункциональный инструмент для проверки IP-адресов и доменов на попадание в DNS-блэклисты и доступность HTTPS. Поддерживает работу как в виде скрипта, так и в Docker/Kubernetes.

---

## 🚀 Возможности

- ✅ Многопоточная проверка IP по DNS-блэклистам
- ✅ Генерация HTML-отчетов
- ✅ Проверка HTTPS-доступности и выполнения PHP-скриптов
- ✅ Работа в нескольких режимах (скрипт, Docker, Kubernetes)
- ⚙️ Планируется поддержка ingress

---

## 🧠 Архитектура

Проект состоит из одного скрипта `cmp_report.py`, который может работать в двух режимах:

- `builder` — многопоточный сборщик данных (IP, blacklist и пр.)
- `server` — простой веб-сервер для показа HTML-отчетов

 Структура:

├── static/ # стили, изображения, прочая статика вебсервера
├── templates/ # темплейты вебсервера
├── docker/ # Dockerfiles
├── k8s/ # Манифесты Kubernetes
├── env/ # requirements.txt для venv
├── cron/ # Скрипт для cron-запуска
├── docs/ # Скриншоты, архитектура, демо
├── cmp_report.py   # собственно скрипт
├── list.txt        # перечень серверов и ИП\хостнеймов
├── black_lists.txt # перечень ДНС-подобных блеклистов


## ⚙️ Установка и запуск

### 1. Простой запуск скриптов

```bash
# Установка окружения
cd /home/calltop/blacklisting-report-tool/
python3 -m venv venv
source venv/bin/activate
pip install -r env/requirements.txt

# Сбор данных, проверка в блеклистах - формирование отчета
python3 cmp_report.py build

# Запуск сервера
python3 cmp_report.py &

### 2. Запуск по cron с окружением (добавляем строку в /etc/crontab)
0 * * * * /bin/sh /home/calltop/blacklisting-report-tool/blacklisting-report-builder.sh >> /home/calltop/blacklisting-report-tool/cmp_report.log 2>&1



### 3. Docker

# Билд образов
docker build -f docker/Dockerfile -t cmp-report-cmp-server:latest .
docker build -f docker/Dockerfile -t cmp-report-cmp-server:latest .

# Пример запуска с docker-compose 
cd docker && docker compose up


### 4. Kubernetes

cd k8s
# Простой запуск пода с пробросом порта
kubectl apply -f k8s/pod.yaml
kubectl port-forward pod/server-report 8080:80

# Продвинутый вариант — deployment + service + ingress
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

### 5. ingress + TLS
# пока только в планах

### 6. Telegram-бот для уведомлений
# В планах.


### Лицензия ###
Этот проект распространяется под лицензией MIT (https://opensource.org/license/mit)

### Авторы ###

Автор - Mntcalm (https://github.com/mntcalm/blacklisting-report-tool.git)


