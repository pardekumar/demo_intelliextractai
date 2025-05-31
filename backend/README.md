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

> To update dependencies, use:
>
> ```sh
> pip freeze > requirements.txt
> ```
