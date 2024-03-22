from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from pymongo.mongo_client import MongoClient
from prometheus_client import start_http_server,Summary


application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html') 

# Updated /predictdata route with Prometheus metrics
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            cycle = float(request.form.get('cycle')),
            op1=float(request.form.get('op1')),
            op2=float(request.form.get('op2')),
            sensor2=float(request.form.get('sensor2')),
            sensor3=float(request.form.get('sensor3')),
            sensor4=float(request.form.get('sensor4')),
            sensor5=float(request.form.get('sensor5')),
            sensor6=float(request.form.get('sensor6')),
            sensor7=float(request.form.get('sensor7')),
            sensor8=float(request.form.get('sensor8')),
            sensor9=float(request.form.get('sensor9')),
            sensor10=float(request.form.get('sensor10')),
            sensor11=float(request.form.get('sensor11')),
            sensor12=float(request.form.get('sensor12')),
            sensor13=float(request.form.get('sensor13')),
            sensor14=float(request.form.get('sensor14')),
            sensor15=float(request.form.get('sensor15')),
            sensor16=float(request.form.get('sensor16')),
            sensor17=float(request.form.get('sensor17')),
            sensor20=float(request.form.get('sensor20')),
            sensor21=float(request.form.get('sensor21'))
        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
            
        print("Storing new data in Monogo DB server")
        password = "Vishnu8748803252"
        uri = "mongodb+srv://vishnumurali835:{}@vishnumurali.gan12f1.mongodb.net/?retryWrites=true&w=majority".format(password)
        # Create a new client and connect to the server
        client = MongoClient(uri)
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
                
        database=client["PM_AERO"]
        collection = database['AERO_PM']
            
        data = {"cycle": data.cycle,"op1": data.op1,"op2": data.op2,"sensor2":data.sensor2,
                    "sensor3": data.sensor3,"sensor4":data.sensor4,"sensor5": data.sensor5,
                    "sensor6":data.sensor6,"sensor7": data.sensor7,"sensor8":data.sensor8,
                    "sensor9": data.sensor9,"sensor10":data.sensor10,"sensor11": data.sensor11,
                    "sensor12": data.sensor12,"sensor13":data.sensor13,"sensor14": data.sensor14,
                    "sensor15":data.sensor15,"sensor16": data.sensor16,"sensor17":data.sensor17,
                    "sensor20": data.sensor20,"sensor21":data.sensor21}
            
        record = collection.find()
        for i in record :
            print(i)
                    
        print("Database and collection is create in Mongodb")
        print("New values is sucessfully inserted into MONGODB")
            
            
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
     

# Start the Prometheus Http server
if __name__=="__main__":
    #start_http_server(5000)
    app.run(host="0.0.0.0")        