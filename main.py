from flask import Flask, render_template,request,session
import pyrebase
from werkzeug import secure_filename
import pyqrcode  as qr
import png 
import json
import os


local_server = True
app = Flask(__name__)
app.secret_key = "lifeisverycomplicated"

with open("config.json","r") as c:
    config_params = json.load(c)["params"]

app.config["UPLOAD_FOLDER"] = config_params['path']

config = {
    "apiKey": "AIzaSyC8JGX3tvNDH9pkTVQiXHhcXB35xIV29tk",
    "authDomain": "superman-a1a14.firebaseapp.com",
    "databaseURL": "https://superman-a1a14.firebaseio.com",
    "projectId": "superman-a1a14",
    "storageBucket": "superman-a1a14.appspot.com",
    "messagingSenderId": "954864727176",
    "appId": "1:954864727176:web:63e981126c974f76995b3d"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
services = firebase.storage()
# auth = firebase.auth()

# @app.route("/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     unsuccessful = 'Please check your credentials'
#     # successful = "Login Successful"
#     if ('user' in session and session['user'] == params["admin_user"]):
#         return render_template("dashboard.html")
         
#     elif (request.method == 'POST'):
#         email = request.form.get('email')
#         password = request.form.get('pass')
#         if (email == params["admin_user"] and password == params["admin_pass"]): 
#             try:
#                 user = auth.sign_in_with_email_and_password(email, password)
#                 # user = auth.refresh(user['refreshToken'])
#                 # user_id = user['idToken']
#                 session['user'] =  email
                
#                 return render_template("dashboard.html")
#             except:
#                 return render_template('signin.html', us=unsuccessful)
#     return render_template('signin.html')




@app.route("/edit/<string:sno>",methods = ['GET','POST'])
def edit(sno):
    if('user' in session and session['user'] == config_params['admin_user']):
        if request.method == "POST":
            cnic = request.form.get("CNIC")
            # dataqr = qr.create(cnic)
            # dataqr.png("Patient1.png", scale = 15)
            data = {
            "name" : request.form.get("name"),
            "phone" : request.form.get("Phone"),
            "age" : request.form.get("age"),
            "date" : request.form.get("Date_Of_Joining"),
            "days" : request.form.get("working_days"),
            "hours" : request.form.get("working_hours"),
            "qualifications" : request.form.get("qualifications"),
            "type" : request.form.get("type"),
            "fees" : request.form.get("fees"),
            "address" : request.form.get("address")
            }
            db.child("doctors").child(cnic).set(data)
    return render_template("edit.html",sno = sno)




@app.route("/", methods=['GET', 'POST'])
def signin():
    unsuccessful = 'Please check your credentials'
    successful = "Login Successful"

    data = db.child("employee").get()
    user_names = []
    user_passwords = []
    for employ in data.each():
        user_names.append(employ.val()["user_name"])
        user_passwords.append(employ.val()["user_password"])    
    if('user' in session and session['user'] == config_params['admin_user']):
        return render_template('dashboard.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        if (email == config_params['admin_user'] and password == config_params['admin_pass']):
            session['user'] = email
            return render_template('dashboard.html')
        elif (email in user_names and password in user_passwords):
            session['user'] = email
            return render_template('index.html')
        else:
            return render_template('signin.html',unsuccessful)
    
    return render_template('signin.html')




@app.route("/logout")
def logout():
    return render_template("index.html")
    session.pop['user']
    return redirect('signin.html')

    
            


@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/team.html", methods=['GET', 'POST'])
def doctors():
    data = db.child("users").get()
    posts = []   
    for doctor in data.each():
        if doctor.val()["role"] == 1 :
            name = doctor.val()["name"]
            doctortype = doctor.val()["type"]
            hours = doctor.val()["hours"]
            days = doctor.val()["days"]
            post = [name,doctortype,hours,days]
            posts.append(post) 
    return render_template("team.html", posts = posts)
    
@app.route("/records.html")
def view_records():
    data = db.child("patients").get()
    posts = []   
    for patient in data.each():
        name = patient.val()["name"]
        age = patient.val()["age"]
        date = patient.val()["date"]
        disorder = patient.val()["disorder"]
        doctor = patient.val()["doctor"]
        phone = patient.val()["phone"]
        room = patient.val()["room"]
        status = patient.val()["status"]
        
        post = [name,age,date,disorder,doctor,phone,room,status]
        posts.append(post) 

    return render_template("records.html", posts = posts)

@app.route("/emergency.html")
def emergency():
    return render_template("emergency.html")

@app.route("/opd.html")
def opd():
    return render_template("opd.html")

@app.route("/doctor.html")
def doctor():
    data = db.child("users").get()
    posts = []   
    for doctor in data.each():
        if doctor.val()['role'] == 1 :
            name = doctor.val()["name"]
            age = doctor.val()["age"]
            qualifications = doctor.val()["qualifications"]
            address = doctor.val()["address"]
            fees = doctor.val()["fees"]
            joining_date = doctor.val()["date"]
            working_days = doctor.val()["days"]
            working_hours = doctor.val()["hours"]
            post = [name,age,qualifications,address,fees,joining_date,working_days,working_hours]
            posts.append(post) 
    return render_template("doctor.html",posts = posts)

@app.route("/nurses.html")
def nurses():
    data = db.child("nurses").get()
    posts = []   
    for nurses in data.each():
        did = nurses.val()["id"]
        name = nurses.val()["name"]
        age = nurses.val()["age"]
        qualifications = nurses.val()["qualifications"]
        address = nurses.val()["address"]
        joining_date = nurses.val()["joining_date"]
        working_days = nurses.val()["working_days"]
        working_hours = nurses.val()["working_hours"]
        
        post = [did,name,age,qualifications,address,joining_date,working_days,working_hours]
        posts.append(post) 
    return render_template("nurses.html",posts = posts)

@app.route("/employees.html")
def employees():
    return render_template("employees.html")

@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@app.route("/print.html")
def print():
    return render_template("print.html")


@app.route("/fileuploader", methods=['GET', 'POST'])
def upload():
    if('user' in session and session['user'] == config_params['admin_user']):
        if (request.method == "POST"):
            # f = request.files['file1']

@app.route("/ipd.html", methods = ["GET","POST"])
def ipd():
    data = db.child("users").get()
    posts = []   
    for doctor in data.each():
        if doctor.val()["role"] == 1 :
            posts.append(doctor.val()["name"])
    if (request.method == "POST"):
        cnic = request.form.get("CNIC")
        dataqr = qr.create(cnic)
        dataqr.png("Patient"+cnic+".png", scale = 15)
        # services.put(dataqr)
        # dataqr.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename("Patient"+cnic+".png")))
        data = {
        "name" : request.form.get("Name"),
        "phone" : request.form.get("Phone"),
        "room" : request.form.get("Rooms"),
        "date" : request.form.get("Date"),
        "doctor" : request.form.get("Doctor"),
        "disorder" : request.form.get("any_disorder"),
        "age" : request.form.get("age"),
        "status" : "active"
        }
        db.child("patients").child(cnic).set(data)
        db.child("patients").child(cnic).child("comments").push({"condition" : "Stable","UID" : "zWl3ppjcH8S5eMCidAI9zYwgdpg2"})
        db.child("patients").child(cnic).child("checkup").push({"blood_pressure" : "Stable","fever" : "90","UID" : "zWl3ppjcH8S5eMCidAI9zYwgdpg2"})
        db.child("patients").child(cnic).child("medicines").push({"medicines" : "Done","UID" : "zWl3ppjcH8S5eMCidAI9zYwgdpg2"})
        return render_template("print.html", post = [data["name"],data["age"],data["doctor"],data["room"]],cnic = cnic)
    return render_template("ipd.html",posts = posts)

app.run(debug=True)




