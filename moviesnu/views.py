from django.http import *
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.template import Template,Context
from django.template.loader import get_template
import datetime
from movies.models import *
from ratings.models import *
from django.contrib.auth.models import User
from operator import itemgetter
import datetime
import math


def home(request):
	if(request.user.is_authenticated()):
		try:
			request.session['skip']
		except KeyError:
			request.session['skip']=[]
	movie=get_next_movie(request)
	if(request.user.is_authenticated()):
		predicted_rating=predict_rating(User.objects.filter(id=request.user.id)[0],movie)
	else:
		predicted_rating=4;

	context=Context({
						'error_flag':0,
						'user':request.user,
						'movie':movie,
						'predicted_rating':round(predicted_rating,1),
						'verdict':get_verdict(predicted_rating*2)
					})
	
	
	a=get_template('home//home.html')
	return(HttpResponse(a.render(context)))
	
	
def logout_user(request):
    logout(request)
    return redirect('http://localhost:8000')

def rate_movie(request):
	movie_id=request.GET['movieid']
	user_id=request.user.id
	rating=request.GET['rating']
	review=request.GET['review']
	if(not request.user.is_authenticated()):
		return(JsonResponse({'error_flag':1,'error':'USER NOT LOGGED IN'}))
	try:
		movie=Movies.objects.filter(MovieId=movie_id)[0]
		movie.NoRating+=1
	except IndexError:
		return(JsonResponse({'error_flag':1,'error':'MOVIE DOES NOT EXIST'}))
		
	try:
		user=User.objects.filter(id=user_id)[0]
	except IndexError:
		return(JsonResponse({'error_flag':1,'error':'USER DOES NOT EXIST'}))
	
	try:
		r=Ratings(UserId=user,MovieId=movie,Rating=rating,Review=review)
		r.save()
	except IntegrityError:
		r=Ratings.objects.filter(UserId=user,MovieId=movie)[0]
	if(r.Rating):
		movie.AvgUsrRating-=int(r.Rating)/movie.NoRating
		
	r.Rating=int(rating)
	movie.AvgUsrRating+=r.Rating/movie.NoRating
	r.Review=review
	
	r.save()
	movie.save()
	m=get_next_movie(request)
	rspnse={
	'error_flag':0,
	'movieid':m.MovieId,
	'name':m.MovieName,
	'year':m.Year,
	'poster':m.Poster,
	}
	return(JsonResponse(rspnse))
	
def not_in(m,qs):
	for q in qs:
		if q.MovieId==m:
			return False
	return True
	
def get_next_movie(request):
	if(not request.user.is_authenticated()):
		return Movies.objects.all()[0]
	qryst=Ratings.objects.filter(UserId=request.user.id)
	movies=Movies.objects.all()
	movies= sorted(movies, key=lambda x: x.NoRating)
	for m in movies: 
		if not_in(m,qryst)  and str(m.MovieId) not in request.session['skip']:
			return m;
	return Movies.objects.filter(MovieId=7)[0] 
		
def skip_movie(request):
	movie_id=request.GET['movieid']
	if( not request.user.is_authenticated()):
		rspnse={
		'error_flag':1,
		'error':'USER NOT LOGGED IN',
		}
		return JsonResponse(rspnse)
	#print request.session['skip']
	movie_id=movie_id.encode('ascii','ignore')
	if(movie_id not in request.session['skip']):
		request.session['skip'].append(movie_id)
		request.session.modified = True
	m=get_next_movie(request)
	rspnse={
	'error_flag':0,
	'movieid':m.MovieId,
	"name":m.MovieName,
	"year":m.Year,
	"poster":m.Poster
	}
	return(JsonResponse(rspnse))
	
def search(key):
	return Movies.objects.filter(MovieName__icontains=key)
	
def search_movie(request):
	movie_key=request.GET['key']
	search_results=search(movie_key)
	rsponse={'result':[]}
	i=0
	for r in search_results:
		dict={
		"name":r.MovieName,
		"year":r.Year,
		}
		rsponse['result'].append(dict)
		i=i+1
		if(i>=5):
			break
	return JsonResponse(rsponse)

	
def difference(a,b):
	ans=0
	for i in a:
		if not i in b:
			ans+=1
	return ans
	
def get_difference(m1,m2):
	a=[]
	try:
		a.append(m1.Action-m2.Action)
	except TypeError:
		a.append(1)
	a.append(m1.Horror-m2.Horror)
	a.append(m1.Romantic-m2.Romantic)
	a.append(m1.Comedy-m2.Comedy)
	a.append(m1.Dark-m2.Dark)
	a.append(m1.Fantasy-m2.Fantasy)
	a.append(m1.SuperHero-m2.SuperHero)
	a.append(m1.ScienceFiction-m2.ScienceFiction)
	a.append(m1.Adventure-m2.Adventure)
	a.append(m1.Animation-m2.Animation)
	a.append(m1.Historic-m2.Historic)
	a.append(m1.Adult-m2.Adult)
	
	try:
		b=m1.Keywords.split(',')
	except AttributeError:
		b=[]
	try:
		c=m2.Keywords.split(',')
	except AttributeError:
		c=[]
	a.append(difference(b,c))
	b=m1.Stars.split(',')
	c=m2.Stars.split(',')
	a.append(difference(b,c))
	if(m1.Director==m2.Director):
		a.append(0)
	else:
		a.append(1)
	result=0	
	for i in a:
		result+=(i*i)
	return math.sqrt(result)
		
def classifier(r,k):
	training_data=Ratings.objects.filter(UserId=r.UserId)
	"""tr=[]
	#for a in training_data:
		if(a.Rating):
			tr.append(a)
	training_data2=sorted(tr,key=lambda x : x.Rating)[0:10]
	training_data1=sorted(tr,key=lambda x : x.Rating,reverse=True)[0:10]
	training_data=training_data1+training_data2"""
	a=[]
	for row in training_data:
		#b=[]
		#b.append(row)
		#b.append(get_similarity())
		#print get_difference(row.MovieId,r.MovieId)
		if(row.Rating):
			a.append([row,get_difference(row.MovieId,r.MovieId)])
	a=sorted(a,key=itemgetter(1))
	#print a
	ans=0
	for i in range(0,min(k,len(a))): 
		ans+=a[i][0].Rating**2
	#print ans
	return math.sqrt(ans/k)
	
def predict_rating(u,m):
	try:
		r=Ratings.objects.filter(UserId=u,MovieId=m)[0]
	except IndexError:
		r=Ratings(UserId=u,MovieId=m)
	
	if(r.Rating):
		return r.Rating
	else:
		rating1=classifier(r,5)
		if(m.IMDBRating!=0):
			rating1=math.sqrt((rating1**2+float(m.IMDBRating/2)**2)/2)
		#rating2=user_classifier(r)
		#rating3=movie_classifier(r)
		return rating1
		
		
def get_verdict(p):
	if(p<=1):
		return "Hell no! Don't go for this one,You 'll probably end up hating yourself for watching this Movie."
	elif(p<=2):
		return "Probably a waste of time and money both, You'll like advertisements better than the Movie"
	elif(p<=3):
		return "Go for this one if you really really really want to. just don't blame us if you hate it."
	elif(p<=4):
		return "umm...Not great enough to spent your money on.just Torrent it already"
	elif(p<=5):
		return "This one's alright, go out with friends,P S Don't get your hopes up."
	elif(p<=6):
		return "You might just like this one not highly recommended though"
	elif(p<=7):
		return "Yes,Now we are talking, You'll like this one. Go for it"
	elif(p<=8):
		return "Don't even think. Book the tickets already,You ll love this Movie"
	elif(p<=9):
		return "Its like This Movie is made for you"
	else:
		return "bingooo! DO NOT miss it at all"

def predict(request):
	if(not request.user.is_authenticated()):
		rspnse={
		'error_flag':1,
		'error':'USER NOT LOGGED IN',
		}
		return JsonResponse(rspnse)
	movie_name=request.GET['name']
	movie_year=request.GET['year']
	try:	
		Usr=User.objects.filter(id=request.user.id)[0]
	except IndexError:
		return(JsonResponse({'error_flag':1,'error':'USER DOES NOT EXIST'}))
		
	no=Ratings.objects.filter(UserId=Usr).count()
	if(no<10):
		return(JsonResponse({'error_flag':1,'error':'YOU HAVE RATED LESS THAN 10 MOVIES.'}))
	try:
		Movie=Movies.objects.filter(MovieName=movie_name,Year=movie_year)[0]
	except IndexError:
		return(JsonResponse({'error_flag':1,'error':'MOVIE DOES NOT EXIST'}))
	
	try:
		r=Ratings.objects.filter(UserId=Usr,MovieId=Movie)[0]
	except IndexError:
		Ratings(UserId=Usr,MovieId=Movie).save()
		r=Ratings.objects.filter(UserId=Usr,MovieId=Movie)[0]
	
	predicted_rating=predict_rating(Usr,Movie)
	r.PredictedRating=round(predicted_rating,1)
	r.save()
	rspnse={
	'error_flag':0,
	'movieid':Movie.MovieId,
	"name":Movie.MovieName,
	"year":Movie.Year,
	"poster":Movie.Poster,
	'description':Movie.Description,
	"predicted_rating":str(round(predicted_rating,1)),
	"verdict":get_verdict(predicted_rating*2)
	}
	return(JsonResponse(rspnse))