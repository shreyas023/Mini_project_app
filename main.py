import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.base")

from sklearn.preprocessing import OrdinalEncoder
le = OrdinalEncoder()

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    Item_Cost = float(request.form.get('Item_Cost'))
    Item_Count	= float(request.form.get('Item_Count'))
    Total_Cost	= Item_Cost * Item_Count
    Lead_Time	= float(request.form.get('Lead_Time'))
    Shelf_Life	= float(request.form.get('Shelf_Life'))
    EOQ	= float(request.form.get('EOQ'))
    encoding_ltv = {
        "low": 0.0,
        "medium": 1.0,
        "high": 2.0
    }
    Lead_Time_Variability = encoding_ltv[request.form.get('Lead_Time_Variability')]
    encoding_seasonality = {
        "none": 0.0,
        "seasonal": 1.0
    }
    Seasonality = encoding_seasonality[request.form.get('Seasonality')]
    location	= request.form.get('Warehouse_Location')
    possible_location = pd.DataFrame(['Mumbai','Delhi','Banglore','Pune','Chennai','Kolkata','Lucknow','Gujarat','Hyderabad'])
    encoded_Location = le.fit_transform(possible_location)
    if location in possible_location:
        Warehouse_Location = le.transform(location)
    else:
        Warehouse_Location = 0.0
    Customer_Reviews	= float(request.form.get('Customer_Reviews'))
    Historical_Sales_Data	= float(request.form.get('Historical_Sales_Data'))
    encoding_demand = {
        "decreasing": 0.0,
        "increasing": 1.0,
        "stable": 2.0
    }
    Demand_Fluctuation	= encoding_demand[request.form.get('Demand_Fluctuation')]

    input_data = [[Item_Cost, Item_Count, Total_Cost, Lead_Time, Shelf_Life, EOQ, Lead_Time_Variability, Seasonality, Warehouse_Location, Customer_Reviews, Historical_Sales_Data, Demand_Fluctuation]] 

    prediction = model.predict(input_data)
    output = prediction[0]

    if output == 'A':
        prediction_text = "This is the more perishable and more profitable inventory, it need to be managed at the highest priority. This belongs to class A."
    elif output == 'B':
        prediction_text = "This is the less perishable and profitable inventory, it need to be managed at the medium priority. This belongs to class B."
    elif output == 'C':
        prediction_text = "This is the non-perishable and less profitable inventory, it need to be managed at the lowest priority. This belongs to class C"

    # return jsonify({'prediction_text': prediction_text})
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)