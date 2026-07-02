from flask import Flask,render_template,request#this request just recives data to backend from frontend
import requests # EXTERNSL PYTHON LIBRSRY WE USE IT TO CALL API and stuffs
import subprocess #let program execute terminal commands
import os#lets theprogram interact with the operating system, such as files, folders, and environment variables
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
             return render_template("index.html", repo=repo,message="Repository found",found=True)
        
            
        else:
            return render_template("index.html", repo=repo,message="Repository not found",found=False)
            

      
       
        print("you enterd: ",repo)

    return render_template("index.html",repo=repo)


@app.route("/deploy",methods=["POST"])
def clone():

    repo=request.form["repo"]
    parts= repo.rstrip("/").split("/")
    destination= f"repos/{parts[4]}"
    if os.path.exists(destination):
        return loadprojecthelper(destination,repo,clonestatus="Repository already exists, using existing copy")#calling helper function

    os.makedirs("repos", exist_ok=True)
    result = subprocess.run(
        ["git","clone",repo,destination],
        capture_output=True,
        text=True
    )
    if result.returncode==0:
        project = checktypeofwork(destination)
        details=projectdetails(get_repo_info(repo))
        dependencystatus=installdependencies(project,destination)
        # serverstatus=startproject(project,destination)
        if dependencystatus=="Dependencies installed successfully":
            serverstatus=startproject(project,destination)
        else:
            serverstatus="Dependencies not installed, so server not started"
        
        return render_template( "index.html",
                               clonestatus="Cloned successfully",
                               projecttype=project,
                               name=details[0],
                               language=details[1],
                               stars=details[2],
                               description=details[3],
                               dependencystatus=dependencystatus,
                               serverstatus=serverstatus)
    
    else:
        return  render_template( "index.html",clonestatus= f"something went wrong {result.stderr}")
    
def checktypeofwork(destination):
        
        files=os.listdir(destination)
        
        if  "requirements.txt" in files:
            return "python"
        if "package.json" in files:
            return "nodejs"
        if "pom.xml" in files:
            return "java"
        else:
            return "unknown"  
def get_repo_info(repo): #helper function to get repo info
    parts =repo.rstrip("/").split("/")
    api_url = f"https://api.github.com/repos/{parts[3]}/{parts[4]}"

    response = requests.get(api_url)

    data = response.json()
    return data
    
def projectdetails(data):
    name = data["name"]
    language = data["language"]
    stars = data["stargazers_count"]
    description = data["description"]
    return(name,language,stars,description)

def installdependencies(projecttype,destination):
    if projecttype=="python":
        result=subprocess.run(["pip","install","-r","requirements.txt"],cwd=destination,capture_output=True,text=True)
    elif projecttype=="nodejs":
        result=subprocess.run(["npm","install"],cwd=destination,capture_output=True,text=True)
    elif projecttype=="java":
        result=subprocess.run(["mvn","install"],cwd=destination,capture_output=True,text=True)
    else:
        return("unknown project type")
    if result.returncode==0:
        return "Dependencies installed successfully"
    else:
        return f"something went wrong {result.stderr}"

def pythonproject(destination):
    
    files=os.listdir(destination)
    if "app.py" in files:
        subprocess.Popen(["python","app.py"],cwd=destination)
        return "Server started successfully"
    elif "main.py" in files:
        subprocess.Popen(["python","main.py"],cwd=destination)
        return "Server started successfully"
    elif "manage.py" in files:
        subprocess.Popen(["python","manage.py"],cwd=destination)
        return "Server started successfully"
    else:
        return "no entry point found"

# def nodejsproject(destination):


def startproject(projecttype,destination):

    if projecttype=="python":
       return pythonproject(destination)
    else:
        return "unknown project type"
        
def loadprojecthelper(destination,repo,clonestatus):#helper function to load project if repo already exsist
    print("running helper function cause repo already exsist")
    project=checktypeofwork(destination)
    details=projectdetails(get_repo_info(repo))
    dependencystatus=installdependencies(project,destination)
    if dependencystatus=="Dependencies installed successfully":
            serverstatus=startproject(project,destination)
    else:
        serverstatus="Dependencies not installed, so server not started"
        
    return render_template( "index.html",
                           clonestatus=clonestatus,
                            projecttype=project,
                            name=details[0],
                            language=details[1],
                            stars=details[2],
                            description=details[3],
                            dependencystatus=dependencystatus,
                            serverstatus=serverstatus)
    
  #incomplete need to fix stuff near clone function

app.run(debug=True,use_reloader=False)
