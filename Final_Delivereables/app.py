import requests
from  flask import *
import pandas as pd
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "McA0cABIxbmWF-itHuc3Tat6XJ0FtvRJHwgQjLDcZI5R"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app = Flask(_name_,template_folder="template")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict', methods=['POST'])

def y_predict():
    data = pd.read_csv('Temp_file.csv')
    cB = request.form["car name"]
    cB=cB.split(' ')[0]
    for i in range(len(data["Brand"])):
        if cB == data["Brand"].iloc[i]:
            cB=data["Encoded"].iloc[i]
    cy = request.form["cylinder"]
    disp = request.form["disp"]
    hP = request.form["hP"]
    weight = request.form["w"]
    Acc = request.form["Acc"]
    mY = request.form["Model"]
    origin = request.form["orgin"]
    
    t = [[int(cy),int(disp),int(hP),int(weight),int(Acc),int(mY),int(origin),int(cB)]]
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": ["cylinders" , "displacement" ,"horsepower","weight" , "acceleration" ,"model year" ,"orgin","make"], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/17716fa2-6c0e-4dd3-b8f3-6dbfd44a61df/predictions?version=2022-11-18', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction = response_scoring.json()

    print(prediction)
    out = prediction['predictions'][0]['values'][0][0]

    op = "Your car mileage is " + str(round(out,2)) 
    if out>30:
        op = op + "! It is astoundingly healthy!"
    elif out>20:
        op = op + "! It seems healthy!"
    elif out>15:
        op =  op + "! Not bad!"
    else:
        op = op + "! It needs proper maintenance"


    return render_template('index.html' , prediction_text=op)


if( _name_ == "_main_"):
    app.run()


