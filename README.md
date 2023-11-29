# SPA-Comments-API

SPA-Comments-API is a web application that provides an API for managing comments.
The application is built using Django REST Framework (DRF) and a MySQL database.
It also provides both session-based and JWT token-based user authentication.

## Установка локально Linux

Команды вля вашей операционной системы могут немного отличаться
Если пакеты у вас есть этот шаг можно пропустить

1. **Установите необходимые инструменты:**
    ```bash
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip virtualenv mysql-server
   ```

   Если пакеты у вас есть этот шаг можно пропустить

2. **Создайте папку для проекта :**
    ```bash
   mkdir my_project
   ```
3. **Клонирование и настройка проекта:**
   ```bash
   git clone git@github.com:ShevaPython/SPA-Comments-API.git
   ```

У Вас появиться папка SPA-Comments-API это будет главная папка вашего проэкта

4. **Активируйте виртуальное окружение:**
   ```bash
   cd SPA-Comments-API
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Создайте базу данных:**
   Запустите MySQL и создайте базу данных, которую вы указали в `DATABASES['default']['NAME']`
   SPA-Comments-API/core/settings.py.
   Например, с использованием командной строки MySQL:Подробно как подключить Mysql можете ознакомиться
   здесь https://metanit.com/python/django/5.9.php

   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE DB_Comments;
   ```


7. **Применение миграций:**
    ```bash
    python manage.py migrate
    ```

8. **Создание суперпользователя:**

   ```bash
   python manage.py createsuperuser
   ```

9. **Запуск проекта**
   ```bash
   python manage.py runserver
   ```

Ваше приложение будет доступно по адресу: http://localhost:8000/swagger/ -это документация о API!
Теперь у вас должно быть локальное развернутое приложение с базой данных MySQL. Убедитесь, что вы предоставили
корректные
значения в вашем файле SPA-Comments-API/core/settings.py для подключения к базе данных.

## Запуск через докер Linux

Для локальной установки вам потребуется Docker и Docker Compose. Если у вас их еще нет, вы можете следовать инструкциям
по установке:

1. **Установите Docker:**
    - [Установка Docker на Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Установка Docker на macOS](https://docs.docker.com/desktop/install/mac-install/)
    - [Установка Docker на Linux](https://docs.docker.com/desktop/install/linux-install/)

2. **Установите Docker Compose:**
    - [Установка Docker Compose](https://docs.docker.com/compose/install/)

3. **Клонируйте репозиторий в заранее созданую папку с виртуальным окружением:**
   ```bash
   git clone git@github.com:ShevaPython/SPA-Comments-API.git
   ```

У Вас появиться папка SPA-Comments-API это будет главная папка вашего проэкта

4. **Активируйте виртуальное окружение:**
   ```bash
   cd SPA-Comments-API
   python3 -m venv venv
   source venv/bin/activate
   ``` 
4. **Збор докер контейнера**
   ```bash
   docker compose build
   ```
4. **Запуск докер контейнера**
   ```bash
   docker compose up
   ```
   Если с первого раза контейнер не запустился попробуйте остановить его и запустить заново
    ```bash
      docker compose stop
       docker compose up
      ```
5. **Эти команды выполнятся внутри контейнера, и вы сможете создать миграции и суперпользователя, как если бы вы
   выполняли эти команды локально в виртуальной среде Django.**

    ```bash
   # Создание миграций
   docker exec -it django-api-container python manage.py makemigrations
   
   # Применение миграций
   docker exec -it django-api-container python manage.py migrate
   
   # Создание суперпользователя
   docker exec -it django-api-container python manage.py createsuperuser
    
   ```
6. **Итоги Docker контейнера:**
После успешной сборки вы выполните команду docker-compose up, которая запустит контейнеры. Django-приложение будет
доступно на http://localhost:8000/, а MySQL будет доступен на localhost:3306.

## Автодокументация с Swagger

SPA-Comments-API предоставляет автодокументацию API с использованием Swagger. Swagger представляет собой инструмент для
создания, документирования и потребления веб-сервисов. С его помощью вы можете легко понять структуру API, опробовать
запросы и получить доступ к интерактивной документации.

### Как использовать Swagger  or Redoc
Доступ к документации
Swagger: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/

После успешного запуска Docker контейнеров, вы можете открыть Swagger UI, перейдя по следующему URL-адресу:

- [Swagger UI](http://localhost:8000/swagger/)

Здесь вы найдете подробное описание всех доступных эндпоинтов, схему запросов и ответов, а также возможность отправлять
запросы и тестировать функциональность API прямо из интерфейса Swagger.

### Преимущества использования Swagger

1. **Легкая навигация по API:** Swagger предоставляет понятную структуру API, что облегчает навигацию и понимание
   доступных эндпоинтов.

2. **Тестирование запросов:** Вы можете использовать Swagger UI для отправки запросов на эндпоинты и проверки ответов в
   удобном интерфейсе.


## Аутентификация и Регистрация

### Регистрация (/register/)

Чтобы зарегистрировать нового пользователя, отправьте POST-запрос на http://localhost:8000/api/v1/users/register/ с необходимыми данными пользователя.

### Аутентификация по токену (JWT)

Для аутентификации по токену используется JSON Web Token (JWT). После успешной аутентификации вы получите токен доступа. Этот токен следует включать в заголовок Authorization каждого последующего запроса, требующего аутентификации.

Пример запроса на получение токена с использованием cURL:http://localhost:8000/api/v1/users/api/token/
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "securepassword"}' http://localhost:8000/api/v1/users/api/token/

```
Пример заголовка Authorization для последующих запросов:
```bash
Authorization: Bearer your_access_token

```
Проверка токена
Чтобы проверить действительность токена доступа, отправьте POST-запрос на http://localhost:8000/api/v1/users/api/token/verify/ с токеном доступа.

Обновление токена доступа http://localhost:8000/api/v1/users/api/token/refresh/
это эндпоинт для обновления токена доступа в вашем API. Этот путь предоставляет возможность обновить токен доступа, если он истек или близок к истечению срока действия.

# Управление Комментариями
