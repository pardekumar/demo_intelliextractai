from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import StreamingResponse
# from utils.csv_export import dict_to_csv_stream
from typing import Annotated, Union
from config import Paths
from glob import glob
from pydantic import BaseModel
import base64
import csv
import io
from typing import Dict, Any, Iterable

from dependencies import get_token_header
from llm.ingestion.ingestion import data_ingestion
from llm.qna.qna import data_ask, data_ask_history
from llm.summary.summary import data_summary
from llm.summary.stream_summary import stream_data_summary  # <-- Import the streaming generator
from sql_app.main import create_document_for_user
from sql_app.main import get_db
from sql_app.crud import get_document_by_name
from utils import object_print


class Question(BaseModel):
    prompt: str
    files: list[str]


class QuestionHistory(BaseModel):
    files: list[str]


class Summary(BaseModel):
    files: list[str]


class FileList(BaseModel):
    data: list[str]


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

async def save_file(file: UploadFile):
    try:
        contents = await file.read()
        type = 'pdf'
        filepath = str(Paths.pdf_upload / file.filename)
        with open(filepath, 'wb') as f:
            f.write(contents)
        document = create_document_for_user(user_id=1, document={
            "name": file.filename,
            "size": file.size,
            "path": filepath,
            "type": type,
            "vector_index": filepath,
            "status": "active",
        })
        await data_ingestion([filepath], [file.filename], document.id)
    except Exception:
        return {"status": "error", "message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"status": "success", "message": f"Successfully uploaded {file.filename}"}


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    try:
        for file in files:
            await save_file(file)
    except Exception:
        return {"status": "error", "message": "There was an error uploading the files"}

    return {"status": "success", "message": f"Successfully uploaded {len(files)} files"}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        document = get_document_by_name(db=get_db(), name=file.filename)
        # print("document", object_print(document))
        if (not document):
            await save_file(file)
        else:
            return {"status": "error", "message": f"File already uploaded {file.filename}"}
    except Exception:
        return {"status": "error", "message": "There was an error uploading the file"}

    return {"status": "success", "message": f"Successfully uploaded {file.filename}"}


@router.get("/getfiles/")
async def getfiles():
    try:
        ret_files = []
        pdf_files = glob(str(Paths.pdf_upload / "*.pdf"))
        for pdf_file in pdf_files:
            encoded_string = ""
            with open(pdf_file, "rb") as pdffile:
                encoded_string = base64.b64encode(pdffile.read())
            ret_files.append({
                "name": pdf_file.rsplit('\\', 1)[-1],
                # "result": "data:application/pdf;base64,{}".format(encoded_string),
                "result": encoded_string,
            })
        return {"files": ret_files}
    except Exception:
        return {"files": []}


# @router.post("/ingest_files/")
# async def ingest_files(files: FileList):
#     res = await data_ingestion(files.data, ["12876_2021_Article_1875.pdf"], 58)
#     return {"status": "success", "message": f"Successfully ingestion", "res": res}
#     # try:
#     # except Exception:
#     #     return {"status": "error", "message": "There was an error ingestion the files"}


@router.post("/ask/")
async def ask(question: Question):
    res = await data_ask(question)
    return {"status": "success", "message": res}
    try:
        res = await data_ask(question)
        return {"status": "success", "message": res}
    except Exception:
        return {"status": "error", "message": "There was an error Q&A response"}


@router.post("/ask-history/")
async def ask(question: QuestionHistory):
    try:
        res = await data_ask_history(question)
        return {"status": "success", "message": res}
    except Exception:
        return {"status": "error", "message": "There was an error Q&A response"}


@router.post("/summary/")
async def summary(params: Summary):
    res = await data_summary(params)
    try:
        return {"status": "success", "message": res}
    except Exception as e:
        print(e)
        return {"status": "error", "message": "There was an error Q&A response"}


@router.post("/stream-summary/")
async def stream_summary(params: Summary):
    try:
        return StreamingResponse(
            stream_data_summary(params),
            media_type="application/x-ndjson"
        )
    except Exception as e:
        print(e)
        return {"status": "error", "message": "There was an error streaming the summary"}


@router.post("/export-csv/")
async def export_csv(request: Request):
    """
    Exports the provided dictionary or list of dictionaries as a downloadable CSV file.
    Accepts any valid JSON body (list or dict).
    """
    data = await request.json()
    print("data", data)
    return StreamingResponse(
        dict_to_csv_stream(data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )


def dict_to_csv_stream(data: Union[Dict[str, Any], list]) -> Iterable[bytes]:
    output = io.StringIO()
    # If data is a list of dicts
    if isinstance(data, list) and data and isinstance(data[0], dict):
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    # If data is a single dict
    elif isinstance(data, dict):
        writer = csv.DictWriter(output, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    else:
        output.write("Unsupported data format for CSV export.\n")
    output.seek(0)
    for line in output:
        yield line.encode('utf-8')


# @router.get("/getchromadb/")
# async def getchromadb():
#     try:
#         res = await get_all_data()
#         return {"status": "success", "message": res}
#     except Exception:
#         return {"files": []}
