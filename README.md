# RESTful API for Fish & Location Management

## Project description and main idea
This is a fully functional RESTful API, created to manage data about fishes and their locations. Originally created as part of a future social project for fishermen, it demonstrates modern backend development techniques, using asynchronous technologies and containerization.

The API implements full **CRUD** (Create, Read, Update, Delete) functionality.

---

## Key technologies

- **FastAPI**: A highly productive Python web framework.
- **PostgreSQL**: A safe database for storing data.
- **SQLAlchemy ORM**: A library for database operations, used in an async way with **asyncpg**.
- **Docker and Docker Compose**: Tools for containerizing the entire tech stack for different running environments.
- **Pydantic**: An autovalidation library used with FastAPI.

---

## Project structure

The project is set up to optimize development, so that a user (or me) can add additional functionality in a short term.

---

## How to run locally

### 1. Prerequisites
- **Docker** and **Docker Compose** installed.
- **Python 3.8+** installed.

### 2. Clone the project
Clone the repository from GitHub:
```bash
git clone [https://github.com/thatwhocode/fastapi_crud_opreations.git](https://github.com/thatwhocode/fastapi_crud_opreations.git)
cd fastapi_crud_opreations
```

### 3. Docker secrets
#### This project uses Docker Secrets for secure credentials. You will need to create the secrets directory and the necessary files if they don't already exist :
```
mkdir secrets
touch secrets/postgres_user.txt
touch secrets/postgres.txt
touch secrets/postgres_db_name.txt
touch secrets/pgadmin.txt
```
### Note: Fill these files with your credentials. For example, postgres_user.txt should contain your PostgreSQL username.

### 4. Docker Compose deployment
```
docker compose up --build -d

```
### **Note:** the ```--build``` falg is only needed for the first run or after code changes. The ```-d``` flags runs container in the background

## API endpoint
### API allows next methods and endpoint:
 - ```GET /fishes/``` - lists all fishes
 - ```Get /fishes/{fish_id}``` - list fish with required number or ```404``` if fish doesn`t exist```
 - ```POST /fishes/``` - adding another fish to DB, if fish name not in DB already
 - ```PUT /fishes/{fish_id}``` - changes fish with ```fish_id``` credentials
 - ```DELETE /fishes/{fish_id}``` - deletes fish with ```fish_id```
## API documentation
 - * Swagger UI *: ```http://localhost:8000/docs```
 - * ReDOC *: ```http://localhost:8000/redoc```





