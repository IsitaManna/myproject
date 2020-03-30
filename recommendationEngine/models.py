from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contact_no = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)


# class Customer(models.Model):
#     custID = models.AutoField(primary_key = True)
#     email = models.CharField(unique=True,null = False, max_length = 50)
#     fName = models.CharField(max_length = 50)
#     lName = models.CharField(max_length = 50)
#     password = models.CharField(max_length = 30)
#     contactNo = models.CharField(max_length = 15)
#     city = models.CharField(max_length = 30)
#     country = models.CharField(max_length = 30)
#     createdDate = models.DateTimeField(null = True)

class Question(models.Model):
    QUALITATIVE = 'Qualitative'
    QUANTITATIVE = 'Quantitative'
    QUESTION_TYPES = [
        (QUALITATIVE, 'Qualitative'),
        (QUANTITATIVE, 'Quantitative')
    ]
    question = models.CharField(max_length=255, unique=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default=QUANTITATIVE)

class Rating(models.Model):
    user = models.ForeignKey(User, related_name='user_rating', on_delete=models.CASCADE)
    image_id = models.IntegerField(5)
    rating = models.IntegerField(1)

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='question_response', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

class UserResponse(models.Model):
    user = models.ForeignKey(User, related_name='user_response', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
