from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=30)
    movie_image = models.ImageField(upload_to='movies/images', null=True)
    nation = models.CharField(max_length=20, null=True)
    genre = models.CharField(max_length=30, null=True)
    release_date = models.DateField()
    summary = models.TextField()

    def __str__(self):
        return self.title

# 유저 id, 영화 id 좀 받아와야 하는데..
# 해당 유저와 해당 코멘트는 1:1 관계여야 한다 -> ForeignKey 또는 OneToOne
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.review