from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref#OK
from datetime import datetime#OK


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


# TODO: connect to a local postgresql database
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


Show=db.Table('Show',
    db.Column('start_time',db.DateTime()),
    db.Column('artist_id',db.Integer, db.ForeignKey('Artist.id',primary_key=True)),
    db.Column('venue_id',db.Integer, db.ForeignKey('Venue.id',primary_key=True)))

GenreVenue=db.Table('GenreVenue',
    db.Column('genre_id',db.Integer, db.ForeignKey('Genre.id',primary_key=True)),
    db.Column('venue_id',db.Integer, db.ForeignKey('Venue.id',primary_key=True)))

GenreArtist=db.Table('GenreArtist',
    db.Column('genre_id',db.Integer, db.ForeignKey('Genre.id',primary_key=True)),
    db.Column('artist_id',db.Integer, db.ForeignKey('Artist.id',primary_key=True)))

class City(db.Model):
    __tablename__="City"
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venue=db.relationship('Venue',backref="city",lazy=True)
    artists=db.relationship('Artist',backref="city",lazy=True)
    
    def __init__(self,city,state):
        self.city=city
        self.state=state
        
    def __repr__(self):
        return "Todo : \n-ID: "+str(self.id)+"\n-city: "+self.city

class Genre(db.Model):   
    __tablename__='Genre'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    venues = db.relationship('Venue',secondary=GenreVenue,backref= backref('genres',lazy=True))
    artists = db.relationship('Artist',secondary=GenreArtist,backref= backref('genres',lazy=True))
     
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    city_id=db.Column(db.Integer,db.ForeignKey('City.id'),nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))#ADD
    seeking_talent = db.Column(db.Boolean,default = False,nullable=False)#ADD
    datecreate=db.Column(db.DateTime())#ADD Stand Out
    seeking_description = db.Column(db.String,default='')
    
    db.relationship('Genre',backref='venue',lazy=True)
    
    def __init__(self,name,address,phone,facebook_link,city_id,image_link='http://indonesiaexpat.biz/wp-content/uploads/2017/05/Wedding-venue-e1494816432851.jpg',website_link="",seeking_talent=False,seeking_description="",datecreate=datetime.now()):
        self.name=name
        self.address=address
        self.phone=phone
        self.image_link=image_link
        self.facebook_link=facebook_link
        self.website_link=website_link
        self.seeking_talent=seeking_talent
        self.seeking_description=seeking_description
        self.city_id=city_id
        self.datecreate=datecreate
        
    def __repr__(self):
        return "Venue : \n-ID: "+str(self.id)+"\n-name: "+self.name
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    city_id=db.Column(db.Integer,db.ForeignKey('City.id'),nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))#ADD
    seeking_venue = db.Column(db.Boolean,default = False,nullable=False)#ADD
    seeking_description = db.Column(db.String,default='')
    datecreate=db.Column(db.DateTime())#ADD Stand Out
    venues = db.relationship('Venue',secondary=Show,backref= backref('artists',lazy=True))
    
    def __init__(self,name,phone,facebook_link,city_id,image_link='https://www.babelio.com/users/AVT_inconnu_9527.jpg',website_link="",seeking_venue=False,seeking_description="",datecreate=datetime.now()):
        self.name=name
        self.phone=phone
        self.image_link=image_link
        self.facebook_link=facebook_link
        self.website_link=website_link
        self.seeking_venue=seeking_venue
        self.seeking_description=seeking_description
        self.city_id=city_id
        self.datecreate=datecreate
        
    def __repr__(self):
        return "Artist : \n-ID: "+str(self.id)+"\n-name: "+self.name

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
