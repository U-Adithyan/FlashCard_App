from .database import db

class user_info(db.Model):
    __tablename__="user_info"
    user_id=db.Column(db.Integer,autoincrement=True,unique=True,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,unique=True,nullable=False)
    decks=db.relationship("deck_info")
    
class deck_info(db.Model):
    __tablename__="deck_info"
    deck_id=db.Column(db.Integer,autoincrement=True,unique=True,primary_key=True)
    deck_name=db.Column(db.String,nullable=False)
    description=db.Column(db.String)
    score=db.Column(db.Integer)
    last_reviewed=db.Column(db.String)
    username=db.Column(db.String,db.ForeignKey("user_info.username"))
    decks=db.relationship("card_info",cascade="all, delete-orphan")
    
    
class card_info(db.Model):
    __tablename__="card_info"
    card_id=db.Column(db.Integer,autoincrement=True,unique=True,primary_key=True)
    front=db.Column(db.String,nullable=False)
    back=db.Column(db.String,nullable=False)
    score=db.Column(db.Integer)
    deck_id=db.Column(db.String,db.ForeignKey("deck_info.deck_id"))