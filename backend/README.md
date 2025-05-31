codebase root path> cd .\backend\
codebase root path\backend\> .\.venv\Scripts\activate
(.venv) codebase root path\backend\> uvicorn main:app --host=0.0.0.0 --port=8000 --reload

uvicorn main:app --host=0.0.0.0 --port=8000 --reload

pip freeze > requirements.txt

pip install -r requirements.txt
