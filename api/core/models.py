from django.db import models

# Create your models here.
class CourseSales(models.Model):
    # id = models.IntegerField(primary_key=True)
    transId = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

class Transaction(models.Model):
    transId = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    status = models.CharField(("status"), max_length=50)
    medium = models.CharField(("Medium"), max_length=50) 
    serviceName = models.CharField(("serviceName"), max_length=50)
    transType = models.CharField(("Transaction Type"), max_length=50)
    amount = models.CharField(("Amount"), max_length=50)
    payerName = models.CharField(("Payer Name"), max_length=50)
    email = models.CharField(("Email"), max_length=50)
    financialTransId = models.CharField(("financialTransId"), max_length=50)
    dateInitiated = models.CharField(("dateInitiated"), max_length=50)
    dateConfirmed = models.CharField(("dateConfirmed"), max_length=50)
    