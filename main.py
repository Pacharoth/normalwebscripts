from typing import List, Union
from fastapi import Depends, FastAPI,Request,BackgroundTasks,File,UploadFile,Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import config
import os
import subprocess

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")
settings =config.Settings()

@app.get('/')
async def import_page(request:Request,response_class=HTMLResponse):
    return templates.TemplateResponse("index.html",{"request":request,"url":settings.app_url})
def write_log(path_execution:str,filename:str):
    message=subprocess.check_output(["python3",path_execution])
    with open("logs/"+filename+".txt",mode="wb") as log:
        log.write(message)
        log.close()
@app.post("/upload_file")
async def submit(background_tasks:BackgroundTasks,files:List[UploadFile]=File(description="Multiple files as UploadFile"),):
    files_name = []
    for file in files:
        contents=await file.read()
        try:
            with open("static/"+file.filename,"wb") as buffer:
                buffer.write(contents)
        except Exception:
            return {"message":"There was error uploading the file"}
        finally:
            file.file.close()
        files_name.append(file.filename)
        path_execution=f'static/{file.filename}'
        background_tasks.add_task(write_log,path_execution,file.filename)
    return {"content":files_name}
class FileName(BaseModel):
    file_name:List[str]

@app.post("/logs")
async def get_logs(file_name:dict=Body(...)):
    list_data =file_name["file_name"]
    contents=""
    for data in list_data:
        for dat in data:
            print(dat)
            file= open("logs/"+dat+".txt","r")
            contents=file.read()
            file.close()
    return {"q":contents}

