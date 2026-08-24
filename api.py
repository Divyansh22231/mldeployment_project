from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import joblib
import pandas as pd
import psycopg2
import os

#app = object and fast api - constructor    we usse this because without initialization we 
# cant access fastapi methods


app=FastAPI()  #initialization of fast api class

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

model=joblib.load("model.pkl")  #loading the model from the pickle file

# we write logic on fuction
#annotation-we giving instruction/rules(you have to work for this type of request and respnse)
#  to python function  @

@app.get("/")  #get method
def testing():
    return FileResponse("static/index.html")

@app.post("/prediction")
def myprediction(hours:float):

    newdata=pd.DataFrame({
    "StudyHours":[hours]
    })

    mynewdata=model.predict(newdata)
    print(mynewdata[0])

    if mynewdata[0]==1:
        result = "Pass"
        print("Pass")
    else:
        result = "Fail"
        print("Fail")

    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', '127.0.0.1'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', '9555805060'),
            dbname=os.environ.get('DB_NAME', 'ml_project')
        )
        cursor = conn.cursor()
        
        sql = "INSERT INTO predictions (study_hours, prediction, result) VALUES (%s, %s, %s)"
        val = (hours, float(mynewdata[0]), result)
        cursor.execute(sql, val)
        conn.commit()
        print("Prediction saved to database successfully!")
        
    except psycopg2.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals() and not cursor.closed:
            cursor.close()
        if 'conn' in locals() and not conn.closed:
            conn.close()

    return {"prediction": float(mynewdata[0]), "status": result}