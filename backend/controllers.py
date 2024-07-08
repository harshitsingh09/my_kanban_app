
from flask import Flask,render_template,request
from flask import current_app as app #Alias for current running app
from .models import *

@app.route("/") #it refers base url 127.0.0.1:5000
def home():
    return "<h2>Welcome to Kanban app</h2>"

@app.route("/register",methods=["GET","POST"]) #it refers base url+/signup
def user_signup():
    if request.method=="POST":
        email=request.form.get("email")
        full_name=request.form.get("full_name")
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        usr=User_Info.query.filter_by(user_name=uname).first() #Get existig user matched
        if not usr:
            new_user=User_Info(email=email,full_name=full_name,user_name=uname,pwd=pwd)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="")
        else:
            return render_template("signup.html",msg="Sorry, User is already existed!!")
    
    return render_template("signup.html",msg="")


@app.route("/login",methods=["GET","POST"]) #it refers base url+/login
def user_login():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        usr=User_Info.query.filter_by(user_name=uname, pwd=pwd).first() #Get existig user matched
        if usr and usr.role==0:
            user_summary=fetch_users() #Calling
            return render_template("admin_dashboard.html",name=usr.user_name,users=user_summary)
        elif usr and usr.role==1:
            user_info=fetch_user_info(usr.id) #one user object
            return render_template("user_dashboard.html",id=user_info.id,name=usr.user_name,lists=user_info.lists)
        else:
            return render_template("login.html",msg="Invalid credentials!!")
    
    return render_template("login.html",msg="")


#UDF for reading all general users
def fetch_users():
    users=User_Info.query.filter_by(role=1).all()
    user_list={}
    for user in users:
        if user.id not in user_list.keys():
            user_list[user.id]=[user.user_name,len(user.lists)]
    return user_list

def fetch_user_info(id):
    user_info=User_Info.query.filter_by(id=id).first()
    return user_info


#more routes here
@app.route("/list/add/<int:user_id>",methods=["GET","POST"])
def new_list(user_id):
    if request.method=="POST":
        title=request.form.get("title")
        description=request.form.get("description")
        list_obj=Lists(title=title,description=description,user_id=user_id)
        db.session.add(list_obj)
        db.session.commit()
        user_info=fetch_user_info(user_id)
        return render_template("user_dashboard.html",id=user_info.id,name=user_info.user_name,lists=user_info.lists)


@app.route("/list/edit/<int:user_id>/<int:list_id>",methods=["GET","POST"])
def edit_list(user_id,list_id):
     if request.method=="POST":
        new_title=request.form.get("title")
        new_description=request.form.get("description")
        list_obj=Lists.query.filter_by(id=list_id).first()
        list_obj.title=new_title
        list_obj.description=new_description
        db.session.commit()
        user_info=fetch_user_info(user_id)
        return render_template("user_dashboard.html",id=user_info.id,name=user_info.user_name,lists=user_info.lists)
   


@app.route("/list/delete/<int:user_id>",methods=["GET","POST"])
def delete_list(user_id):
    pass


#lot of routes
