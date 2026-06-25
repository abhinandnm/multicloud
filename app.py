from flask import Flask,render_template,request,jsonify

app =Flask(__name__)

users=[{"jhon":"Devops"}]
@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        print("submitted")

        repo = request.form["repo"]
        print("you enterd: ",repo)
    return render_template("index.html")
@app.route("/users",methods =["GET"])

def listusers():
    return users.jsonify
 


# def userdata ():
#     data = request.json
app.run()
