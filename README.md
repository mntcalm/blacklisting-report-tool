# blacklisting-report-tool
multithread checking IPs on blacklists, HTML-report, 2 modes of script activity (builder and server)

URL: https://github.com/mntcalm/blacklisting-report-tool.git
docs: https://mntcalm.github.io/blacklisting-report-tool/index.html
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

# Билд образов (обратите внимание: два образа, builder и server) один Dockerfile с разными таргетами
docker build -f docker/Dockerfile -t cmp-report-cmp-server:latest .
docker build -f docker/Dockerfile -t cmp-report-cmp-builder:latest .

# Пример запуска с docker-compose 
docker compose -f docker/docker-compose.yml up --build -d

# для чтения логов 
##docker compose -f docker/docker-compose.yml logs -f

# для остановки
##docker compose -f docker/docker-compose.yml down

### 4. Kubernetes
# монтируем рабочую папку. ИЛИ - размещаем проект монтированном вольюме (с корректировкой путей)
# minikube start --memory=4096 --cpus=2 --mount --mount-string=~/blacklisting-report-tool:/mnt/cmp_report

# docker внурти миникуб /// вернуть к обычному docker
# eval $(minikube docker-env -u) /// eval $(minikube docker-env -u) 

cd k8s
# Простой запуск пода с пробросом порта
kubectl apply -f k8s/pod_cmp_report.yaml
kubectl port-forward pod/server-report 8002:8002 --address 0.0.0.0

# Продвинутый вариант — deployment + service + ingress
kubectl apply -f k8s/deployment_cmp_report.yaml
kubectl apply -f k8s/service_cmp_report.yaml
# этот вариант требует проброса порта ИЛИ проксирования через вебсервер на порт 30082

#### kubectl apply -f k8s/ingress.yaml  - пока не реализовано



### 5. ingress + TLS
# пока только в планах

### 6. Telegram-бот для уведомлений
# В планах.


### Лицензия ###
Этот проект распространяется под лицензией MIT (https://opensource.org/license/mit)

### Авторы ###

Автор - Mntcalm (Aleksandr Dotsenko)
(https://github.com/mntcalm/blacklisting-report-tool.git)


