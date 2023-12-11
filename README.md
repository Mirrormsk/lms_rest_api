# LMS REST API

RESTful API для LMS системы. 
Проект содержит модели уроков, курсов, пользователей, и информацию о платежах.


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
