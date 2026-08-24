from fastapi import FastAPI
import joblib
import pandas as pd
import mysql.connector

#app = object and fast api - constructor    we usse this because without initialization we 
# cant access fastapi methods


app=FastAPI()  #initialization of fast api class

model=joblib.load("model.pkl")  #loading the model from the pickle file

# we write logic on fuction
#annotation-we giving instruction/rules(you have to work for this type of request and respnse)
#  to python function  @

@app.get("/")  #get method
def testing():
    return {"test":"all ok"}

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
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="9555805060",
            database="ml_project"
        )
        cursor = conn.cursor()
        
        sql = "INSERT INTO predictions (study_hours, prediction, result) VALUES (%s, %s, %s)"
        val = (hours, float(mynewdata[0]), result)
        cursor.execute(sql, val)
        conn.commit()
        print("Prediction saved to database successfully!")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    return {"prediction": float(mynewdata[0]), "status": result}