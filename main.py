from os import environ
from flask import Flask, render_template, request
app = Flask(__name__)
import requests

form = environ['mainform']

def getData(id):
    row = requests.get('https://sheetdb.io/api/v1/'+form+'/search?ID='+id).json()
    if len(row)<1: return "Not Found"
    else: row = row[0]
    data={"name":row["Name"],
            "id":row["ID"],
            "email":row["Email"],
            "gsuite":row["G-suite"],
            "desig":row["Designation"],
            "promoted":row["Promoted Semester"],
            "joined":row["Joined"],
            "prcount":len(row["PR"].split(",")),
            "pr":row["PR"][:-1],
            "meetings":meetings(id),
            "blogs":row["Blogs"],
            "mag":row["Magazines"]
        }
    return data


def meetings(id):
    rows = requests.get('https://sheetdb.io/api/v1/'+form+'?sheet=Sheet2').json()
    lst=[]
    total = 0
    attend = 0
    for i in rows:
        link = i["Link"]
        name = requests.get(link+'/name').json()["name"]
        att = requests.get(link+'/search?BRACU ID='+id).json()
        if len(att)==1:
            lst.append([name,"✅"])
            attend+=1
        else:
            lst.append([name,"❌"])
        total+=1
    
    return [lst,(attend/total)*100]

        
@app.route('/',methods=['POST','GET'])
def index():
    result=None
    if request.method=='POST':
        result=getData(request.form['id'])
    return render_template("index.html", result=result)

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port="8080")