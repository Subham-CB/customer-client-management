from django.db import models
from clients.models import Client


class Contact(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    clients = models.ManyToManyField(Client, blank=True, related_name='contacts')

    class Meta:
        ordering = ['surname', 'name']
        indexes = [
            models.Index(fields=['surname', 'name']),
        ]

    def __str__(self):
        return f'{self.surname} {self.name}'

    @property
    def full_name(self):
        return f'{self.surname} {self.name}'