from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from kubetask.models.model import TaskModel, TaskInstanceModel, async_sessionmaker
from .constants import JOB_FILE_CONTENT_TYPE
from .process_files import parse_files

from kubernetes import client, config
from fastapi.responses import JSONResponse

job_router = APIRouter(
    prefix="/job",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@job_router.post("/")
async def upload_job(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    async with async_sessionmaker() as session:
        async with session.begin():
            db_objects = []
            for file in files:
                if file.content_type not in JOB_FILE_CONTENT_TYPE:
                    raise HTTPException(400, detail="Invalid document type")
                obj = parse_files(file)
                db_objects.append(TaskModel(**obj.dict()))
        session.add_all(db_objects)
        session.commit()
    return {"status": "Successfully updated"}


@job_router.get("/{namespace}")
async def main(namespace):
    config.load_kube_config()
    v1 = client.BatchV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_job(namespace)
    print (len(ret.items))
    content = {"data": [{"ns": i.metadata.namespace, "name": i.metadata.name} 
            for i in ret.items]}
    return JSONResponse(content=content)


ns_router = APIRouter(
    prefix="/namespace",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@ns_router.get("/")
async def list_ns():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_namespace()
    return {"data": [i.metadata.name for i in ret.items]}

