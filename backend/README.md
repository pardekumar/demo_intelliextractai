PS C:\Code\POC\poc-ask-file\v1> cd .\server\
PS C:\Code\POC\poc-ask-file\v1\server> .\.venv\Scripts\activate
(.venv) PS C:\Code\POC\poc-ask-file\v1\server> uvicorn main:app --host=0.0.0.0 --port=8000 --reload

uvicorn main:app --host=0.0.0.0 --port=8000 --reload

pip freeze > requirements.txt

pip install -r requirements.txt
