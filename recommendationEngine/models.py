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
    STYLE = "Style"
    QUESTION_TYPES = [
        (QUALITATIVE, 'Qualitative'),
        (QUANTITATIVE, 'Quantitative'),
        (STYLE, 'Style')
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
    user = models.ForeignKey(User,null=True,unique=True, related_name='user_ocr', on_delete=models.SET_NULL)


class Rating(models.Model):
    class Meta:
        unique_together = ['user', 'image']

    user = models.ForeignKey(User, related_name='user_rating', on_delete=models.CASCADE)
    image = models.ForeignKey(OCRImage, related_name='user_image', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )


class StyleImage(models.Model):
    image_path = models.FileField(upload_to='style_plans',null=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, default=None)
    bedroom = models.PositiveIntegerField(null=True)
    is_black = models.BooleanField(default=True)


class UserStyle(models.Model):
    user = models.ForeignKey(User, related_name='user_userstyle', on_delete=models.CASCADE)
    style = models.ForeignKey(StyleImage, related_name='user_style', on_delete=models.CASCADE)

class ColoredTextTestImage(models.Model):
    image_path = models.ImageField(upload_to='colored_text_test_plans',null=True)
    data_dict = models.TextField(null=True)

class GANPredictImage(models.Model):
    style_image = models.ForeignKey(StyleImage, null=True, on_delete=models.CASCADE, default=None)
    image_path = models.FileField(upload_to='gan_predict_img',null=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, default=None)
