from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymongo

# Create your views here.
con = pymongo.MongoClient("mongodb://localhost:27017")
mydb = con["Student"]
mycol = mydb["studentDetails"]
loginCol = mydb["login"]

{"name": ""}


def home(req):
    if (req.session.get("user") == None):
        return redirect("loginPage")
    myData = mycol.find()
    dataList = []
    for data in myData:
        dataList.append(data)
    # return HttpResponse("<h1>Hello welcome to home page</h1>")

    return render(req, 'home.html', {"data": dataList})


def about(req):
    return HttpResponse("<h1>Hello welcome to home page</h1>")


def form(req):
    message = ""
    if (req.method == "POST"):
        name = req.POST.get("username")
        rollno = req.POST.get("rollno")
        age = req.POST.get("age")
        mark = req.POST.get("mark")

        if (len(name) > 0 and len(rollno) > 0 and len(age) > 0 and len(mark) > 0):
            mydata = {"name": name, "rollno": rollno, "age": age, "mark": mark}
            result = mycol.insert_one(mydata)
            print(result.inserted_id)
            return redirect("homePage")
        else:
            message = "enter value"

    return render(req, "form.html", {"message": message})


def login(req):
    if (req.session.get("user") != None):
        return redirect("homePage")
    if (req.method == "POST"):
        name = req.POST.get("username")
        password = req.POST.get("password")
        result = loginCol.find({"name": name, "password": password})
        for each in result:
            print("person is in database")
            req.session["user"] = name
            return redirect("homePage")
        return redirect("signupPage")

    return render(req, "login.html")


def signup(req):
    message = ""
    if (req.session.get("user") != None):
        return redirect("homePage")
    if (req.method == "POST"):
        name = req.POST.get("username")
        password = req.POST.get("password")
        confirmPassword = req.POST.get("confirmPassword")
        if (confirmPassword == password):
            result = loginCol.find({"name": name, "password": password})
            for each in result:
                print("person is already in database")
                return redirect("homePage")
            loginCol.insert_one({"name": name, "password": password})
            return redirect("homePage")

        else:
            message = "passwordMismatch"

    return render(req, "signup.html", {"errMessage": message})


def logout(req):
    del req.session["user"]
    return redirect("loginPage")
