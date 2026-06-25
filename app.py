from flask import Flask,render_template,request,jsonify
import requests

app =Flask(__name__)


@app.route("/",methods=["GET","POST"])

def home():
    repo = ""
    if request.method == "POST":
        print("submitted")

        repo = request.form["repodata"] 
        
        

        repo = repo.rstrip("/")#removes any extra / at the end
        parts = repo.split("/")#splits the useriput to parts it cut at every /
       
        if not repo.startswith("https://github.com/"):#starts with match the provided text with iniatl text of userinp
            return render_template("index.html",repo=repo+" not valid")
        if len(parts) < 5:
            return render_template("index.html", repo="Repository name missing")
        # elif parts[4] == "":
        #     return render_template("index.html", repo="Repository name missing")
        #  checking repo really exsist
        api_url = f"https://api.github.com/repos/{parts[3]}/{parts[4]}"
        response = requests.get(api_url)
        if  response.status_code == 200:
             return render_template("index.html", repo="Repository found")
        
            
        else:
            return render_template("index.html", repo="Repository not found")
            

      
       
        print("you enterd: ",repo)

    return render_template("index.html",repo=repo)



app.run()
