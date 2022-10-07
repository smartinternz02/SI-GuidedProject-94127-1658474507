from flask import Flask, render_template, request
import numpy as np
import pickle


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
    print(total)
    prediction = model.predict(total)
    print(prediction)

    return render_template('submit.html', prediction_text=prediction)



"""i = [x for x in request.form.values()]
    f = [np.array(i)]
    print(f)
    output = model.predict(f)"""


"""@app.route('/predicts',methods =['GET','POST'])
def predicts():
    
    return render_template('index.html', prediction_text = 'Suitable drug type is {}'.format(prediction))"""



if __name__ == "__main__":
    app.run(debug=False)