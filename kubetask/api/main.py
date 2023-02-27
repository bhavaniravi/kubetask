from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

from .constants import JOB_FILE_CONTENT_TYPE


router = APIRouter(
    prefix="/job",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def upload_job(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    for file in files:
        if file.content_type not in JOB_FILE_CONTENT_TYPE:
            raise HTTPException(400, detail="Invalid document type")
    return {"status": "Successfully updated"}


@router.get("/")
async def main():
    content = """
<body>
<form action="/job" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
