from django.db import models

# Create your models here.
class Movies(models.Model):
    MovieId=models.AutoField(primary_key=True)
    MovieName=models.CharField(max_length=100)
    Year=models.CharField(max_length=4)
    ReleaseDate=models.DateField()
    Horror=models.DecimalField(max_digits=3, decimal_places=2)
    Romantic=models.DecimalField(max_digits=3, decimal_places=2)
    Comedy=models.DecimalField(max_digits=3, decimal_places=2)
    Fantasy=models.DecimalField(max_digits=3, decimal_places=2)
    Dark=models.DecimalField(max_digits=3, decimal_places=2)
    Historic=models.DecimalField(max_digits=3, decimal_places=2)
    ScienceFiction=models.DecimalField(max_digits=3, decimal_places=2)
    SuperHero=models.DecimalField(max_digits=3, decimal_places=2)
    Drama=models.DecimalField(max_digits=3, decimal_places=2)
    Adult=models.DecimalField(max_digits=3, decimal_places=2)
    Animation=models.DecimalField(max_digits=3, decimal_places=2)
    Adventure=models.DecimalField(max_digits=3,decimal_places=2)
    Action=models.DecimalField(max_digits=3,decimal_places=2)
    Stars=models.CharField(max_length=200)
    Director=models.CharField(max_length=200)
    IMDBRating=models.DecimalField(max_digits=3,decimal_places=1,)
    AvgUsrRating=models.DecimalField(max_digits=3,decimal_places=1)
    NoRating=models.IntegerField(default=0)
    NoPredictions=models.IntegerField(default=0)
    Keywords=models.CharField(max_length=1000,null=True)
    Description=models.TextField()
    Poster=models.URLField(null=True)
    ImdbURL=models.URLField(unique=True)
    Language=models.CharField(max_length=20)
    class Meta:
        unique_together=('MovieName','Year')
    def __str__(self):
        return self.MovieName+'('+self.Year+')'