from django.db import models

class Employee(models.Model):
    name = models.CharField(verbose_name='Работник',max_length=100)

    def __str__(self):
        return self.name
