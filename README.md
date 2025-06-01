# Prerequisites

- Install **Node.js**
- Install **Python**
- Install **Postgres**
- Create a database named `intelliextractai`
- Set the DB username and password as `postgres`

# Backend Setup

1. **Clone the repo**
2. Open a terminal in the root directory where you cloned the repo.
3. Change to the backend directory:
   ```sh
   cd .\backend\
   ```
4. Set up a virtual environment:
   ```sh
   python -m venv .venv
   ```
5. Activate the virtual environment:
   ```sh
   .\.venv\Scripts\activate
   ```
6. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
7. Run the backend server:
   ```sh
   uvicorn main:app --host=0.0.0.0 --port=8000 --reload
   ```

> To update dependencies, use:
>
> ```sh
> pip freeze > requirements.txt
> ```

# Frontend Setup

1. **Clone the repo**
2. Open a terminal in the root directory where you cloned the repo.
3. Change to the frontend directory:
   ```sh
   cd .\frontend\
   ```
4. Install dependencies:
   ```sh
   npm i
   ```
5. Run frontend:
   ```sh
   npm start
   ```

# Steps to setup PostgreSQL

1. **Install stable version of PostgreSQL - from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads**
2. After installation run the following commands to setup the service

3. Create a data directory for Postgres DB say, u created in C directory - "C:\PostgresData"

4. Open a command prompt at bin directory of your postgres installation

5. Run the following commands

   ```
   initdb -D "C:\PostgresData" -U postgres
   pg_ctl start -D "C:\PostgresData"
   ```

6. Open a command prompt with adminstrator and change to bin directory and run the following commands

   ```
   pg_ctl register -N PostgreSql-14 -D "C:\Users\pardekumar\Documents\ProjectWork\Postgres14Data"
   net start PostgreSql-14
   ```

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.
