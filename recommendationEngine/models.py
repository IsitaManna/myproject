from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    contact_no = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    vector = models.TextField(null=True)


class Question(models.Model):
    QUALITATIVE = 'Qualitative'
    QUANTITATIVE = 'Quantitative'
    QUESTION_TYPES = [
        (QUALITATIVE, 'Qualitative'),
        (QUANTITATIVE, 'Quantitative')
    ]
    question = models.CharField(max_length=255, unique=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default=QUANTITATIVE)
    image_path = models.FileField(upload_to='questions',null=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='question_response', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    image_path = models.FileField(upload_to='answers',null=True)

class UserResponse(models.Model):
    class Meta:
        unique_together = ['user', 'question']

    user = models.ForeignKey(User, related_name='user_response', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='+', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)


class OCRImage(models.Model):
    image_path = models.FileField(upload_to='floor_plans',null=True)
    data_dict = models.TextField(null=True)


class Rating(models.Model):
    class Meta:
        unique_together = ['user', 'image']

    user = models.ForeignKey(User, related_name='user_rating', on_delete=models.CASCADE)
    image = models.ForeignKey(OCRImage, related_name='user_image', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
