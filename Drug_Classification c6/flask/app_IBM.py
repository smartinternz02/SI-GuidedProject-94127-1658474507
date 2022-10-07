from flask import Flask, render_template, request
import requests
import pickle

API_KEY = "GIhuAqI-RYYM8pQWbVwXbNO0Zl_wwMdcaIWSkQc7zx-d"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

model = pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)


@app.route("/")
def about():
    return render_template('home.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/predict")
def home1():
    return render_template('predict.html')


@app.route("/submit")
def home2():
    return render_template('submit.html')


@app.route("/pred", methods=['POST'])
def predict():
    age = request.form['Age']
    print(age)
    sex = request.form['Sex']
    if sex == '1':
        sex = 1
    if sex == '0':
        sex = 0
    bp = request.form['BP']
    if bp == '0':
        bp = 0
    if bp == '1':
        bp = 1
    if bp == '2':
        bp = 2
    cholesterol = request.form['Cholesterol']
    if cholesterol == '0':
        cholesterol = 0
    if cholesterol == '1':
        cholesterol = 1
    na_to_k = request.form['Na_to_K']
    total = [[int(age), int(sex), int(bp), int(cholesterol), float(na_to_k)]]

    payload_scoring = {"input_data": [{"field": [['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']],
                                       "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/44031f77-b1c4-4966-b2fe-db25aee0486b/predictions?version=2022-10-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)

    pred = response_scoring.json()

    output = pred['predictions'][0]['values'][0][0]

    return render_template('submit.html', prediction_text=output)


if __name__ == "__main__":
    app.run(debug=False)