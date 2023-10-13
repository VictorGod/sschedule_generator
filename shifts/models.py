from django.db import models

class Shift(models.Model):
    start_time = models.TimeField(verbose_name='Начало работы')
    end_time = models.TimeField(verbose_name='Окончание работы')

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

