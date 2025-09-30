# That`s a dev branch for my Async CRUD backend aplication

## Project description and main idea
**That`s a  RESTful API for Fish&Location Management**

It`s a fully functional RESTful API, created to manage data about fishes and their location.Originnally created as a part of future social project for fishermans. It show`s modern techniques to backend developing, usign asycn technologies and conterization

API release full CRUD(Create, Read, Update, Delete) fucntional

##Key technologies

 - **FastAPI** - highly productive Python web framework
 - **PosgreSQL** safe database to store a lot of data in future
 - **SQLAlchemy ORM** library for database operation, used in async way with *asyncpg*
 - **Docker and Docker compose** - Allows to konterize all of tech stack in different runnig environments
 - **Pydantic** - Autovalidation library used with FastAPI

## Project structure

*Project setteld in a way to optimize developing of a project, so that user(or me) can add additional functional in a short term*

##How to run locally
 -  First thing first - make sure you have *Docker and Docker compose* installed
 -  Make sure you have Python 3.8+ installed

### 1.Clone the project
```
git clone https://github.com/thatwhocode/fastapi_crud_opreations.git
cd fast_api_crud_operations
```

### 2. In order to run project you need to create several files
 - **.env**
Used for local connection to database
```
POSTGRES_USER=dev
POSTGRES_PASSWORD=my_secret_password
POSTGRES_DB=dev_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

**Make sure you have #exactly#  same in your docker-compose file**

### 3.Docker compose deploying
``` docker compose up --build```
```--build``` you`ll only need at first


## API endpoint
### API allows next methods and endpoint:
 - ``` GET /fishes/``` - lists all fishes
 - ```Get /fishes/{fish_id}``` - list fish with required number or ```404``` if fish doesn`t exist```
 - ```POST /fishes/``` - adding another fish to DB, if fish name not in DB already
 - ```PUT /fishes/{fish_id}``` - changes fish with ```fish_id``` credentials
 - ```DELETE /fishes/{fish_id}``` - deletes fish with ```fish_id```
## API documentation
 - *Swagger UI*: ```http://localhost:8000/docs```
 - *ReDOC*: ``http://localhost:8000/redoc





