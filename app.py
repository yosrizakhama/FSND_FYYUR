#-----------------------------------------------------------------------------#
    #------------------------- Start Word ------------------------------------#
#-----------------------------------------------------------------------------#
"""
I have with pleasure realized this project, all the functions of my web application
are locally "functional" and I hope that it will be it with you too, I am sorry
because I have not commented on my work but I will do for the next project;)
My database model contains 2 main tables (VENUE, ARTIST,) and 5 other tables
(SHOW, GENRE, CITY, GENREVENUE and GENREARTIST) to manage the 1-n and n-n relationships
between the tables

"""

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import db,app,Artist,Venue,Show,City,Genre,GenreArtist,GenreVenue
import dateutil.parser
import babel
from flask import  render_template, request, Response, flash, redirect, url_for,jsonify,json
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate #OK
from datetime import datetime#OK
from sqlalchemy.orm import aliased#OK
import sys
from Demos.win32gui_dialog import WM_SEARCH_RESULT
import operator
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
connection=db.engine.connect()
migrate=Migrate(app,db)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  
  if format == 'full':
      format="dd.MM.YYYY hh:mm"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    artists=db.session.query(Artist).order_by(Artist.datecreate.desc()).limit(10)
    venues=db.session.query(Venue).order_by(Venue.datecreate.desc()).limit(10)
    
    return render_template('pages/home.html',artists=artists,venues=venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data_b=City.query.all()
 
  data1=[]
  for city in data_b:
    data_add={}
    data_add['city']=city.city
    data_add['state']=city.state
    data_add['venues']=[]
    venue_add={}
    for venue in city.venue:
        venue_add={}
        venue_add['id']=venue.id
        venue_add['name']=venue.name
        n,up=search_up(venue)
        venue_add['num_upcoming_shows']=n
        data_add['venues'].append(venue_add)
        
    data1.append(data_add)
    city=sorted(City.query.all(),key=operator.attrgetter("state"))
  return render_template('pages/venues.html', areas=data1,city=city);

def search_up(v,t=1):
    today=datetime.now()
    show=db.session.query(Show).all()
    n=0
    up=[]
    for sh in show:
        if t==1:
            id=sh.venue_id
        else:
            id=sh.artist_id
        if id==v.id and sh.start_time>today:
            n+=1
            up.append(sh)
    return n,up

def search_past(v,t=1):
    today=datetime.now()
    show=db.session.query(Show).all()
    n=0
    past=[]
    for sh in show:
        if t==1:
            id=sh.venue_id
        else:
            id=sh.artist_id
        if id==v.id and sh.start_time<=today:
            n+=1
            past.append(sh)
    return n,past

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={}
  search_term=request.form.get('search_term', '')
  venues_result=Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  response["count"]=len(venues_result)
  response["data"]=[]
  for venue in venues_result:
      data_item={}
      data_item["id"]=venue.id
      data_item["name"]=venue.name
      data_item["num_upcoming_shows"],up=search_up(venue)
      response["data"].append(data_item)
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
#ADD
@app.route('/venues/searchcity/<int:id>')
def search_venues_city(id):
    response={}
    #data_str=request.data
    #print(data_str)
    #data_json=json.loads(data_str)
    #id=int(data_json["id"])
    city=City.query.get(id)
    venues_result=Venue.query.filter(Venue.city_id==(id)).all()
    response["count"]=len(venues_result)
    response["data"]=[]
    for venue in venues_result:
        data_item={}
        data_item["id"]=venue.id
        data_item["name"]=venue.name
        data_item["num_upcoming_shows"],up=search_up(venue)
        response["data"].append(data_item)
    
    return render_template('pages/search_venues.html', results=response, search_term="Venue for City : "+city.city+" "+city.state)
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data_list=showdata(1)
  data = list(filter(lambda d: d['id'] == venue_id, data_list))[0]
  return render_template('pages/show_venue.html', venue=data)

def showdata(t):
  if t==1:
      all_data=Venue.query.all()
  else:
      all_data=Artist.query.all()
  
  data_list=[]
  for data in all_data:
    data_add={}
    data_add['id']=data.id
    data_add['name']=data.name
    data_add['city']=data.city.city
    data_add['state']=data.city.state
    data_add['phone']=data.phone
    data_add['website']=data.website_link
    data_add['facebook_link']=data.facebook_link
    if t==1:
        data_add['seeking_talent']=data.seeking_talent
        data_add['address']=data.address
    else:
        data_add['seeking_venue']=data.seeking_venue
    data_add['seeking_description']=data.seeking_description
    data_add['image_link']=data.image_link  
    data_add['genres']=[el.name for el in data.genres]
    data_add['past_shows_count'],past=search_past(data,t)
    data_add['upcoming_shows_count'],up=search_up(data,t)
    data_add['past_shows']=[]
    for p in past:
        s_add={}
        if t==1:
            s_add['artist_id']=p.artist_id
            s_add['artist_name']=Artist.query.get(p.artist_id).name
            s_add['artist_image_link']=Artist.query.get(p.artist_id).image_link
        else:
            s_add['venue_id']=p.venue_id 
            s_add['venue_name']=Venue.query.get(p.venue_id).name
            s_add['venue_image_link']=Venue.query.get(p.venue_id).image_link
            
        s_add['start_time']=p.start_time.strftime("%d/%m/%Y %H:%M:%S")
        data_add['past_shows'].append(s_add)
    data_add['upcoming_shows']=[]
    for p in up:
        s_add={}
        if t==1:
            s_add['artist_id']=p.artist_id
            s_add['artist_name']=Artist.query.get(p.artist_id).name
            s_add['artist_image_link']=Artist.query.get(p.artist_id).image_link
        else:
            s_add['venue_id']=p.venue_id 
            s_add['venue_name']=Venue.query.get(p.venue_id).name
            s_add['venue_image_link']=Venue.query.get(p.venue_id).image_link
            
        s_add['start_time']=p.start_time.strftime("%d/%m/%Y %H:%M:%S")
        data_add['upcoming_shows'].append(s_add)
        
    data_list.append(data_add)
  return data_list

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
    cities=City.query.all()
    exist=False
    city_id=0
    for city in cities:
        if request.form.get('state')==city.state and request.form.get('city')==city.city:
            city_id=city.id
            print("1-City ID is : ",city_id)
            exist=True
            break
       
    if not exist:
        try:
            city=City(city=request.form.get('city'),state=request.form.get('state'))
            db.session.add(city)
            db.session.commit()
            
            
        except:
            db.session.rollback()
            flash('An error 1 occurred. Venue ' + data.name + ' could not be listed.')
        finally:
            
            db.session.close()
    city_id=city_id=City.query.filter(City.city.ilike(request.form.get('city'))).filter(City.state.ilike(request.form.get('state'))).first().id
    print("2-City ID is : ",city_id)
    venue_id=0
    try:
    
        venue=Venue(
        name=request.form.get('name'),
        address=request.form.get('address'),
        phone=request.form.get('phone'),
        facebook_link=request.form.get('facebook_link'),
        city_id=city_id
        )
        db.session.add(venue)  
        
            #db.session.add(venue_genre)    
        db.session.commit()
        venue_id=venue.id
    except:
        db.session.rollback()
        flash('An error 2 occurred. Venue ' + data.name + ' could not be listed.')
    finally:
        db.session.close()
    
    try:
        for genre in request.form.getlist('genres'):
            req=Genre.query.filter(Genre.name==genre)
            if len(req.all())==0:
                gen=Genre(name=genre)
                db.session.add(gen)
                db.session.commit()
                
            genre_id=Genre.query.filter(Genre.name==genre).first().id
            venue_genre = GenreVenue.insert().values(genre_id=genre_id, venue_id=venue_id)
            db.engine.execute(venue_genre)
    except:
        flash('An error 3 occurred. Venue ' + data.name + ' could not be listed.')
        
    
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    artists=db.session.query(Artist).order_by(Artist.datecreate.desc()).limit(10)
    venues=db.session.query(Venue).order_by(Venue.datecreate.desc()).limit(10)
    
    return render_template('pages/home.html',artists=artists,venues=venues)

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    print("demande delete recue")
    try:
        
        venue_genre = GenreVenue.delete().where(venue_id==venue_id)
        db.engine.execute(venue_genre)
    
        show = Show.delete().where('Show.venue_id'==venue_id)
        db.engine.execute(show)
        db.session.delete(Venue.query.get(venue_id))
        db.session.commit()
        print("deleted")
        flash('Venue with ID= ' +venue_id + ' is deleted.')
    except:
        print("not deleted")
        flash('An error 1 occurred. Venue with ID= ' +venue_id + ' could not be deleted.')
        db.session.rollback()
    finally:
        db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    #return render_template('pages/home.html')
    
    return redirect(url_for('index'))
    
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()
  city=sorted(City.query.all(),key=operator.attrgetter("state"))
  return render_template('pages/artists.html', artists=data,city=city)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={}
  search_term=request.form.get('search_term', '')
  resp=Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  response['count']=len(resp)
  response['data']=[]
  for artist in resp:
      add_data={}
      add_data['id']=artist.id
      add_data['name']=artist.name
      add_data['num_upcoming_shows'],up=search_up(artist, 2)
      response['data'].append(add_data)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#ADD
@app.route('/artists/searchcity/<int:id>')
def search_artists_city(id):
    response={}
    #data_str=request.data
    #print(data_str)
    #data_json=json.loads(data_str)
    #id=int(data_json["id"])
    city=City.query.get(id)
    artists_result=Artist.query.filter(Artist.city_id==(id)).all()
    response["count"]=len(artists_result)
    response["data"]=[]
    for artist in artists_result:
        data_item={}
        data_item["id"]=artist.id
        data_item["name"]=artist.name
        data_item["num_upcoming_shows"],up=search_up(artist,2)
        response["data"].append(data_item)
    
    return render_template('pages/search_artists.html', results=response, search_term="Artist for City : "+city.city+" "+city.state)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  data_list=showdata(2)
  data = list(filter(lambda d: d['id'] == artist_id, data_list))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist_base=Artist.query.get(artist_id)
  artist={
    "id": artist_base.id,
    "name": artist_base.name,
    "genres": [g.name for g in artist_base.genres],
    "city": artist_base.city,
    "state": artist_base.state,
    "phone": artist_base.phone,
    "website": artist_base.website_link,
    "facebook_link": artist_base.facebook_link,
    "seeking_venue": artist_base.seeking_venue,
    "seeking_description":artist_base.seeking_description ,
    "image_link": artist_base.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist=Artist.query.get(artist_id)
  data_form=request.form 
  artist.name=data_form.get("name")
  artist.phone=data_form.get("phone")
  artist.facebook_link=data_form.get("facebook_link")
  db.session.commit()
  db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue_base=Venue.query.get(venue_id)
  venue={
    "id": venue_base.id,
    "name": venue_base.name,
    "genres": [g.name for g in venue_base.genres],
    "city": venue_base.city,
    "state": venue_base.state,
    "phone": venue_base.phone,
    "website": venue_base.website_link,
    "facebook_link": venue_base.facebook_link,
    "seeking_venue": venue_base.seeking_talents,
    "seeking_description":venue_base.seeking_description ,
    "image_link": venue_base.image_link
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue=Venue.query.get(venue_id)
  data_form=request.form 
  venue.name=data_form.get("name")
  venue.phone=data_form.get("phone")
  venue.facebook_link=data_form.get("facebook_link")
  db.session.commit()
  db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    cities=City.query.all()
    exist=False
    city_id=0
    for city in cities:
        if request.form.get('state')==city.state and request.form.get('city')==city.city:
            city_id=city.id
            print("1-City ID is : ",city_id)
            exist=True
            break
       
    if not exist:
        try:
            city=City(city=request.form.get('city'),state=request.form.get('state'))
            db.session.add(city)
            db.session.commit()
            
            
        except:
            db.session.rollback()
            flash('An error 1 occurred. Artist ' + request.form.get('name') + ' could not be listed.')
        finally:
            db.session.close()
    
    city_id=city_id=City.query.filter(City.city.like(request.form.get('city'))).filter(City.state.like(request.form.get('state'))).first().id
    print("2-City ID is : ",city_id)
    venue_id=0
    try:
        artist=Artist(name=request.form.get('name'),phone=request.form.get('phone'),facebook_link=request.form.get('facebook_link'),city_id=city_id)
        db.session.add(artist)  
        db.session.commit()
        artist_id=artist.id
    except:
        db.session.rollback()
        flash('An error 2 occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    
    try:
        for genre in request.form.getlist('genres'):
            req=Genre.query.filter(Genre.name==genre)
            if len(req.all())==0:
                gen=Genre(name=genre)
                db.session.add(gen)
                db.session.commit()
                
            genre_id=Genre.query.filter(Genre.name==genre).first().id
            artist_genre = GenreArtist.insert().values(genre_id=genre_id, artist_id=artist_id)
            db.engine.execute(artist_genre)
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error 3 occurred. Artist ' + request.form['name'] + ' could not be listed.')
        
    
  # on successful db insert, flash success
    
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    artists=db.session.query(Artist).order_by(Artist.datecreate.desc()).limit(10)
    venues=db.session.query(Venue).order_by(Venue.datecreate.desc()).limit(10)
    
    return render_template('pages/home.html',artists=artists,venues=venues)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data=[]
  data_show=db.session.query(Show).all()
  for data_s in data_show:
      data_add={}
      data_add['venue_id']=data_s.venue_id
      data_add['artist_id']=data_s.artist_id
      data_add['start_time']=data_s.start_time.strftime("%d/%m/%Y %H:%M:%S") 
      data_add['venue_name']=Venue.query.get(data_s.venue_id).name
      data_add['artist_name']=Artist.query.get(data_s.artist_id).name
      data_add['artist_image_link']=Artist.query.get(data_s.artist_id).image_link
      data.append(data_add)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    try:
        data_in=request.form      
        show_sql = Show.insert().values(artist_id=data_in['artist_id'],venue_id=data_in['venue_id'],start_time=data_in['start_time'])
        db.engine.execute(show_sql)
        flash('Show was successfully listed!')
    except:
        flash('An error occurred. Show could not be listed.')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    artists=db.session.query(Artist).order_by(Artist.datecreate.desc()).limit(10)
    venues=db.session.query(Venue).order_by(Venue.datecreate.desc()).limit(10)
    
    return render_template('pages/home.html',artists=artists,venues=venues)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
