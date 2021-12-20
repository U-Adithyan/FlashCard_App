from flask_restful import Resource,reqparse
from .database import db
from .models import *

create_parser=reqparse.RequestParser()
create_parser.add_argument('name')
create_parser.add_argument('username')
create_parser.add_argument('password')

class UserAPI(Resource):
  def get(self,username):
    user=user_info.query.filter_by(username=username).first()
    if user is not None:
      return {"name":user.name,"username":user.username}
    else:
      return {},404

  def put(self):
    args=create_parser.parse_args()
    name=args.get("name",None)
    username=args.get("username",None)
    password=args.get("password",None)

    if name is None or username is None or password is None:
      return {},406
    else:
      user=user_info.query.filter_by(username=username).first()
      if user is not None:
        return {},409
      else:
        p=user_info(name=name,username=username,password=password)
        db.session.add(p)
        db.session.commit()
        return {},201


class DeckAPI(Resource):
  def get(self,deck_id):
    deck=deck_info.query.filter_by(deck_id=deck_id).first()
    if deck is not None:
      return {"name":deck.deck_name,"description":deck.description,"score":deck.score,"username":deck.username}
    else:
      return {},404
  def delete(self,deck_id):
    deck=deck_info.query.filter_by(deck_id=deck_id).first()
    if deck is None:
      return {},404
    else:
      db.session.delete(deck)
      db.session.commit()
      return {},200
      

class CardAPI(Resource):
  def get(self,card_id):
    card=card_info.query.filter_by(card_id=card_id).first()
    if card is not None:
      return {"front":card.front,"back":card.back,"deck_id":card.deck_id}
    else:
      return {},404
  def delete(self,card_id):
    card=card_info.query.filter_by(card_id=card_id).first()
    if card is not None:
      db.session.delete(card)
      db.session.commit()
      return {},200
    else:
      return {},404