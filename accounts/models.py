from django.db import models

# Create your models here.


class Account(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.balance}"
