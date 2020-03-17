from django.db import models

# Create your models here.
class Customer(models.Model):
    custID = models.AutoField(primary_key = True)
    email = models.CharField(unique=True,null = False, max_length = 50)
    fName = models.CharField(max_length = 50)
    lName = models.CharField(max_length = 50)
    password = models.CharField(max_length = 30)
    contactNo = models.CharField(max_length = 15)
    city = models.CharField(max_length = 30)
    country = models.CharField(max_length = 30)
    createdDate = models.DateTimeField(null = True)

class Questions(models.Model):
    questionID = models.AutoField(primary_key = True)
    Question = models.CharField(max_length = 255)

class Ratings(models.Model):
    email = models.ForeignKey(Customer, related_name='+', on_delete=models.CASCADE, db_column='email')
    imageID = models.IntegerField(5)
    rating = models.IntegerField(1)

class Responses(models.Model):
    responseID = models.AutoField(primary_key = True)
    questionID = models.ForeignKey(Questions, related_name='+', on_delete=models.CASCADE, db_column='questionID')
    response = models.CharField(max_length = 100)

class CustomerResponse(models.Model):
    custRespID = models.AutoField(primary_key = True)
    custID = models.ForeignKey(Customer, related_name='+', on_delete=models.CASCADE, db_column='custID')
    questionID = models.ForeignKey(Questions, related_name='+', on_delete=models.CASCADE, db_column='questionID')
    responseID = models.ForeignKey(Responses, related_name='+', on_delete=models.CASCADE, db_column='responseID')
    timestamp = models.DateTimeField(null = True)