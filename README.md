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
## Pre deployments requirements:
```
cd app/
```
``` 
mkdir secrets
```
**Make sure you have your secrets folder in .gitignore file**

``` 
echo -n "dev" > secrets/postgres_user.txt

```
echo -n "my_secret_password" > secrets/postgres.txt

```
echo -n "dev_db" > secrets/postgres_db_name.txt
```

```
echo -n "pgadmin_password" > secrets/pgadmin.txt
```


**The project is set up to be deployed with one single command. To see more about project see dev branch**

```
docker compose up --build -d
```
**Note - Im still making changes in order to deploy project with one single command**


## API endpoint
### API allows next methods and endpoint:
 - ```GET /fishes/``` - lists all fishes
 - ```Get /fishes/{fish_id}``` - list fish with required number or ```404``` if fish doesn`t exist```
 - ```POST /fishes/``` - adding another fish to DB, if fish name not in DB already
 - ```PUT /fishes/{fish_id}``` - changes fish with ```fish_id``` credentials
 - ```DELETE /fishes/{fish_id}``` - deletes fish with ```fish_id```
## API documentation
 - **Swagger UI**: ```http://localhost:8000/docs```
 - **ReDOC**: ```http://localhost:8000/redoc```



