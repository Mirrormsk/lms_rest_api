# LMS REST API

RESTful API для LMS системы. 
Проект содержит модели уроков, курсов, пользователей, и информацию о платежах.


## Запуск через Docker
```bash
docker compose up --build  # сборка и запуск контейнеров

docker ps  # посмотреть список контейнеров

docker exec -it <hash контейнера api> bash  # войти в консоль контейнера с api

python3 manage.py migrate  # применить миграции
python3 manage.py collectstatic  # собрать статику
```

### Проект запускается на порту `0.0.0.0:80` (или `0.0.0.0`)


## Первичная настройка
Примените миграции:

```bash
python3 manage.py migrate
```

Создать записи об уроках и курсах из фикстуры:

```bash
python3 manage.py loaddata lessons_data.json
```

Создание тестовых пользователей командой `python3 manage.py fill_users <count>`, где `<count>` - количество необходимых записей (опциональный аргумент, по умолчанию - 10):

```bash
python3 manage.py fill_users 10
```

Создание тестовых записей о платежах командой `python3 manage.py fill_payments <count>`, где `<count>` - количество необходимых записей (опциональный аргумент, по умолчанию - 10):

```bash
python3 manage.py fill_payments 30
```


Создание группы "moderators" и тестового модератора:
```bash
python3 manage.py load_groups
```


Запуск celery и периодических задач:
```bash
make run-celery-and-beat
```
