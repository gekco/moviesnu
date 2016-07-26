from django.db import models
from movies.models import Movies
from django.contrib.auth.models import User
# Create your models here.


class Ratings(models.Model):
	UserId=models.ForeignKey(User)
	MovieId=models.ForeignKey(Movies)
	Rating=models.IntegerField(null=True)
	PredictedRating=models.IntegerField(null=True)
	Review=models.TextField(null=True)
	class Meta:
		unique_together=('UserId','MovieId')
	def __str__(self):
		return self.MovieId.MovieName