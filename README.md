api_yamdb
===============

Описание:
----
Проект YaMDb собирает отзывы пользователей на различные произведения.

Как запустить проект:  
----
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:Ruzal-Z/api_yamdb.git
```
```bash
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:  
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python manage.py migrate
```
Запустить проект:  
```bash
python manage.py runserver
```
Примеры запросов к API:  
----
Регистрация нового пользователя(POST):
    http://127.0.0.1:8000/api/v1/auth/signup/ 

Получение JWT-токена:    
    http://127.0.0.1:8000/api/v1/auth/token/ 

Получение списка всех категорий (GET):
    http://127.0.0.1:8000/api/v1/categories/

Добавление новой категории (POST):
    http://127.0.0.1:8000/api/v1/categories/    

Получение списка всех жанров(GET):
    http://127.0.0.1:8000/api/v1/genres/

Получение списка всех произведений(GET):
    http://127.0.0.1:8000/api/v1/titles/

Получение списка всех отзывов(GET):
    http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

Получение списка всех комментариев к отзыву(GET):
    http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Получение списка всех пользователей(GET):
    http://127.0.0.1:8000/api/v1/users/
    

Стек технологий:
----

Python 3.9
Django 3.2
DRF
JWT


## Авторы: 

Рузал Закиров(Ruzal-Z) - Auth/Users
Андрей Габриэлис(Jeinter) - Categories/Genres/Titles
Шамиль Эбзеев(Em5ty) - Review/Comments