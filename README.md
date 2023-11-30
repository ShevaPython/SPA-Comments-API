# SPA-Comments-API

SPA-Comments-API is a web application that provides an API for managing comments.
The application is built using Django REST Framework (DRF) and a MySQL database.
It also provides both session-based and JWT token-based user authentication.

## Install Linux locally.

The commands for your operating system may be slightly different.
If you have packages you can skip this step. The project is initially configured to run via docker so see Chapter 6. and configure the database according to your data.
1. **Install the necessary tools:**
    ```bash
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip virtualenv mysql-server
   ```

   If you have the packages, you can skip this step

2. **Create a folder for the project:**
    ```bash
   mkdir my_project
   ```
3. **Cloning and customization of the project:**
   ```bash
   git clone git@github.com:ShevaPython/SPA-Comments-API.git
   ```

You will see the SPA-Comments-API folder, which will be the main folder of your project.
4. **Activate the virtual environment:**.
   ```bash
   cd SPA-Comments-API
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Set dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Create a database:**
   Start MySQL and create the database you specified in `DATABASES['default']['NAME']`
   SPA-Comments-API/core/settings.py.
   For example, using the MySQL command line:For details on how to connect Mysql, please see
   here https://metanit.com/python/django/5.9.php

   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE DB_Comments;
   ```


7. **Application of Migrations:**.
    ```bash
    python manage.py migrate
    ```

8. **Creating a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

9. **Project Launch**
   ```bash
   python manage.py runserver
   ```

Your application will be available at: http://localhost:8000/swagger/ -this is the documentation about the API!
You should now have a locally deployed application with a MySQL database. Make sure you have provided
correct
values in your SPA-Comments-API/core/settings.py file to connect to the database.

## Docker startup

You will need Docker and Docker Compose for installation. If you don't already have them, you can follow the instructions below
for installation:

1. **Установите Docker:**
    - [Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Install Docker on macOS](https://docs.docker.com/desktop/install/mac-install/)
    - [Install Docker on Linux](https://docs.docker.com/desktop/install/linux-install/)

2. **Install Docker Compose:**
    - [Install Docker Compose](https://docs.docker.com/compose/install/)

3. **Clone the repository into the previously created my_project:** folder.
   ```bash
   git clone git@github.com:ShevaPython/SPA-Comments-API.git
   ```

You will see the SPA-Comments-API folder, which will be the main folder of your project.

4. **Activate the virtual environment:**
   ```bash
   cd SPA-Comments-API
   python3 -m venv venv
   source venv/bin/activate
   ``` 
5. **Build containers from docker-compose.yaml**.
   ```bash
   docker compose build
   ```
6. **Docker container launch**
   ```bash
   docker compose up
   ```
7. **If the container does not start the first time, try stopping it and starting it again**
    ```bash
    docker compose stop
    docker compose up
    ```
8. **These commands will be executed inside the container, and you will be able to create migrations and superuser as if you are
   execute these commands locally in a virtual Django environment.**

    ```bash
   # Create migrations
   docker exec -it django-api-container python manage.py makemigrations
   
   # Application of migrations  
   docker exec -it django-api-container python manage.py migrate
   
   # Create superuser
   docker exec -it django-api-container python manage.py createsuperuser
    
   ```
9. **Docker container totals:**
After a successful build, you will run the docker-compose up command, which will start the containers. The Django application will be
available at http://localhost:8000/, and MySQL will be available at localhost:3306.

## Auto-documentation with Swagger

SPA-Comments-API provides API auto-documentation using Swagger. Swagger is a tool for
creating, documenting and consuming web services. With its help, you can easily understand the API structure, try out
requests, and access interactive documentation.

### How to use Swagger or Redoc
Access to documentation :
Swagger: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/

After successfully launching Docker containers, you can open the Swagger UI by going to the following URL:
- [Swagger UI](http://localhost:8000/swagger/)

Here you will find a detailed description of all available endpoints, a scheme of requests and responses, as well as the ability to send requests and test API functionality directly from the Swagger interface.

### Преимущества использования Swagger

### Benefits of using Swagger

1. **Easy API navigation:** Swagger provides a clear API structure that makes it easy to navigate and understand the
   the available endpoints.

2. **Query Testing:** Using the Swagger user interface, you can send queries to endpoints and test the responses in a
   user-friendly interface.


### Authentication and Registration

### Registration 

To register a new user, send a POST request to http://localhost:8000/api/v1/users/register/ with the required user data.

### ### Session-based authentication
Simply enter your account username and password.

### Token-based authentication (JWT)

JSON Web Token (JWT) is used for token authentication. After successful authentication, you will receive an access token. This token should be included in the Authorization header of each subsequent request that requires authentication.

Example of a token request using cURL:http://localhost:8000/api/v1/users/api/token/
```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "securepassword"}' http://localhost:8000/api/v1/users/api/token/

```
An example of an Authorization header for subsequent requests:
```bash
Authorization: Bearer your_access_token

```
Token Validation
To verify the validity of an access token, send a POST request to http://localhost:8000/api/v1/users/api/token/verify/ with the access token.

Updating the access token http://localhost:8000/api/v1/users/api/token/refresh/
is the endpoint for updating the access token in your API. This path provides a way to update your access token if it has expired or is close to expiration.
# Manage Comments
Creating a comment http://localhost:8000//api/v1/comments/create/
* Description: The path is used to create a new comment.
* Method: POST
* Example Usage:
```bash.
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <your_jwt_token>" -d '{"text": "New comment", "parent_comment": null, "image":"<your_image_data_data_as_base64>"}' http://localhost:8000/api/v1/comments/create/
```
List of all main comments and replies to them http://localhost:8000/api/v1/comments/list_all_info/

* Description: Path provides a complete list of all comments.
* Method: GET
* Example Usage:
```bash
curl http://localhost:8000/api/v1/comments/list_all_info/

```
Comment Details http://localhost:8000/api/v1/comments/1/

* Description: Path provides details of a specific comment by its identifier.
* Method: GET
* Example Usage:
```bash
curl http://localhost:8000/api/v1/comments/1/
 
```

List of root comments http://localhost:8000//api/v1/comments/

* Description: The path provides a list of root comments (without parent comments).
* Method: GET
* Example Usage:
```bash
curl http://localhost:8000/api/v1/comments/
```