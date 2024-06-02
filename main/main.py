from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import *
import numpy as np
import random
from ultralytics import YOLO
import cv2
model = YOLO("best.pt")
idintance ="ID: "+ str(int(random.random()*1000))
from fastapi.middleware.cors import CORSMiddleware
import json

from sqlkk import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,"inid":idintance})
@app.get("/home", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"inid":idintance})

@app.post("/detect")
async def ocr(data:ORC_Check):
    #rgb image pil image
    image_pil = decode_base64_to_numpy(data.image)
    image_np = np.array(image_pil,dtype=np.uint8)
    result = model(image_np,conf=0.35)
    if len(result):
        result = result[0]
        for box in result.boxes:
            
            x1,y1,x2,y2 = list(map(int,box.xyxy[0]))
            image_np = cv2.rectangle(image_np,(x1,y1),(int(x2),int(y2)),(0,255,0))
            
    image_str = encode_numpy_array_to_base64(image_np)
    return Response(json.dumps({"data":image_str}))

@app.post("/check_login")
async def check_login(data:Login):
    tk = data.tk
    mk = data.mk
    if check_login_sql(tk,mk):
        print("oke")
        return Response(json.dumps({"data":"ok"}))
        
    else:
        return Response(json.dumps({"data":"cut"}))
@app.post("/signup")
async def check_login(data:Login):
    tk = data.tk
    mk = data.mk
    if not insert_new_person(tk,mk)[0]:
        
        return Response(json.dumps({"data":"ok"}))
        
    else:
        return Response(json.dumps({"data":"cut"}))