from flask import Flask,request
from flask import render_template,redirect
from flask import current_app as app
from datetime import datetime
from .database import *
from .models import *

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html",error="")
    else:
        user=request.form.get("username")
        pwd=request.form.get("password")
        exist=user_info.query.filter_by(username=user).all()
        if exist==[]:
            return render_template("login.html",error="User Does Not Exist")
        else:
            for person in exist:
                if person.password==pwd:
                    return redirect("/dashboard/"+user)
            return render_template("login.html",error="Incorrect Password")
    
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="GET":
        return render_template("signup.html",error="")
    else:
        name=request.form.get("name")
        user=request.form.get("username")
        pwd=request.form.get("password")
        exist=user_info.query.filter_by(username=user).all()
        if exist!=[]:
            return render_template("signup.html",error="Existing User")
        if name!="" and user!="" and pwd!="":
            p=user_info(name=name,username=user,password=pwd)
            db.session.add(p)
            db.session.commit()
            return redirect("/")
        else:
            return redirect("/signup",error="Enter Valid Input")
        
@app.route("/dashboard/<string:user>",methods=["GET"])
def dash(user):
    decks=deck_info.query.filter_by(username=user).all()
    return render_template("dashboard.html",error="",name=user,decks=decks)

@app.route("/make_deck/<string:user>",methods=["GET","POST"])
def deck(user):
    if request.method=="GET":
        return render_template("add_deck.html",error="")
    else:
        name=request.form.get("deck_name")
        description=request.form.get("description")
        now=datetime.now()
        last= now.strftime("%d/%m/%Y %H:%M:%S")
        exist=deck_info.query.filter_by(username=user,deck_name=name).all()
        if exist!=[]:
            return render_template("add_deck.html",error="Existing Deck")
        if name!="":
            if description!="":
                p=deck_info(deck_name=name,username=user,description=description,score=0,last_reviewed=last)
                db.session.add(p)
                db.session.commit()
                return redirect("/dashboard/"+user)
            else:
                p=deck_info(deck_name=name,username=user,description="-",score=0,last_reviewed=last)
                db.session.add(p)
                db.session.commit()
                return redirect("/dashboard/"+user)
        else:
            return redirect("/make_deck/"+user,error="Enter Valid Input")

@app.route("/<string:user>/manage/<int:deck_id>",methods=["GET","POST"])
def deck_manage(user,deck_id):
    if request.method=="GET":
        cards=card_info.query.filter_by(deck_id=deck_id).all()
        return render_template("manage.html",name=user,cards=cards,deck_id=deck_id)
    
@app.route("/<string:user>/delete/<int:deck_id>")
def delete_deck(user,deck_id):
    deck=deck_info.query.filter_by(deck_id=deck_id,username=user).first()
    db.session.delete(deck)
    db.session.commit()
    return redirect("/dashboard/"+user)

@app.route("/<string:user>/add_card/<int:deck_id>",methods=["GET","POST"])
def add_card(user,deck_id):
    if request.method=="GET":
        return render_template("add_card.html")
    else:
        front=request.form.get("front")
        back=request.form.get("back")
        p=card_info(front=front,back=back,deck_id=deck_id)
        db.session.add(p)
        db.session.commit()
        return redirect("/"+user+"/manage/"+str(deck_id))
    
@app.route("/<string:user>/<int:deck_id>/delete/<int:card_id>")
def delete_card(user,deck_id,card_id):
    card=card_info.query.filter_by(deck_id=deck_id,card_id=card_id).first()
    db.session.delete(card)
    db.session.commit()
    return redirect("/"+user+"/manage/"+str(deck_id))

@app.route("/<string:user>/<int:deck_id>/update/<int:card_id>",methods=["GET","POST"])
def update_card(user,deck_id,card_id):
    card=card_info.query.filter_by(deck_id=deck_id,card_id=card_id).first()
    if request.method=="GET":
        return render_template("update_card.html",card=card)
    else:
        new_front=request.form.get("front")
        new_back=request.form.get("back")
        if new_front!="":
            card.front=new_front
        if new_back!="":
            card.back=new_back
        db.session.commit()
        return redirect("/"+user+"/manage/"+str(deck_id))
    
@app.route("/<string:user>/review/<int:deck_id>/<int:pos>",methods=["GET","POST"])
def review(user,deck_id,pos):
    cards=card_info.query.filter_by(deck_id=deck_id).all()
    deck=deck_info.query.filter_by(deck_id=deck_id,username=user).first()
    if request.method=="GET":
      if cards!=[]:
        return render_template("review.html",user=user,deck_id=deck_id,cards=cards,i=pos)
      else:
        return redirect("/dashboard/"+user)
    else:
        scoredata=request.form
        score=scoredata[list(scoredata.keys())[0]]
        cards[pos-1].score=score
        db.session.commit()
        total=0
        for card in cards:
            if card.score!=None:
                total+=card.score
        total=int((total/(3*len(cards)))*100)
        deck.score=total
        deck.last_reviewed=datetime.now()
        db.session.commit()
        return redirect("/"+user+"/review/"+str(deck_id)+"/"+str(pos))