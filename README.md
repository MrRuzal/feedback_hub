FeedbackHub
===============

Описание:
----
Проект FeedbackHub собирает отзывы пользователей на различные произведения.

Как запустить проект:  
----
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:MrRuzal/feedback_hub.git
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
Заполнить базу данных:
```bash
python manage.py runscript import_data
```
Запустить проект:  
```bash
python manage.py runserver
```
Примеры запросов к API:  
----
Регистрация нового пользователя(POST):
```bash
    http://127.0.0.1:8000/api/v1/auth/signup/ 
```
Получение JWT-токена:  
```bash
    http://127.0.0.1:8000/api/v1/auth/token/ 
```
Получение списка всех категорий (GET):
```bash
    http://127.0.0.1:8000/api/v1/categories/
```
Добавление новой категории (POST):
```bash
    http://127.0.0.1:8000/api/v1/categories/    
```
Получение списка всех жанров(GET):
```bash
    http://127.0.0.1:8000/api/v1/genres/
```
Получение списка всех произведений(GET):
```bash
    http://127.0.0.1:8000/api/v1/titles/
```
Получение списка всех отзывов(GET):
```bash
    http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Получение списка всех комментариев к отзыву(GET):
```bash
    http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Получение списка всех пользователей(GET):
```bash
    http://127.0.0.1:8000/api/v1/users/
```    

Стек технологий:
----

Python 3.9  
Django 3.2  
DRF  
JWT  


## Авторы: 

Рузал Закиров [devbkd](https://github.com/MrRuzal) - Auth/Users  
Андрей Габриэлис [Jeinter](https://github.com/Jeinter) - Categories/Genres/Titles/Импорт данных из csv файлов  
Шамиль Эбзеев [Em5ty](https://github.com/Em5ty) - Review/Comments  
