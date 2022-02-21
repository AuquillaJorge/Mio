from fastapi import FastAPI,Request,HTTPException
import pickle

app = FastAPI()
posts = []

@app.on_event("startup")
def load_model():
    global model
    model =pickle.load(open("ml_model_GROCERY.pkl","rb"))
    
@app.get("/api/author")
def index():
    return {        
        "msg" :"Proyecto de Machine Learning : Analisis de Ventas",
        "author": "Jorge Luis Auquilla"
    }

@app.post("/api/predict")
async def get_home_price(request:Request):
       formdata = await request.form()
       hause_attr=[[
           formdata["anio"],
           formdata["mes"]    
       ]]
       price=model.predict(hause_attr).tolist()[0]
       return {'Anio':formdata["anio"],'Mes':formdata["mes"],"prediccion":price}


@app.post("/api/predict1")
async def get_home_price(request:Request):
       model1=pickle.load(open("ml_model_GROCERY1.pkl","rb"))
       formdata = await request.form()
       hause_attr=[[
           formdata["anio"],
           formdata["mes"]    
       ]]
       price=model1.predict(hause_attr).tolist()[0]
       return {'Anio':formdata["anio"],'Mes':formdata["mes"],'prediccion': "1010" }


@app.get('/posts')
def get_posts():
    return posts

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Item not found")