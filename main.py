from fastapi import FastAPI,Request
import pickle

app = FastAPI()

@app.on_event("startup")
def load_model():
    global model
    model =pickle.load(open("ml_model_regression.pkl","rb"))
    
@app.get("/api/author")
def index():
    return {
        
        "msg" :"Machine Learning",
        "author": "Ing. Danny Jaramillo"
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