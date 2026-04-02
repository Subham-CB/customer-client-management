from django.db import models
from clients.models import Client


class Contact(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Contact first name"
    )
    
    surname = models.CharField(
        max_length=255,
        help_text="Contact last name"
    )

    email = models.EmailField(
        unique=True,
        help_text="Contact email address"
        )
    
    clients = models.ManyToManyField(
        Client,
        related_name='contacts',
        blank=True,
        help_text="Clients linked to this contact"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contacts'
        ordering = ['surname', 'name']
        indexes = [
            models.Index(fields=['surname', 'name']),
        ]

    def __str__(self):
        return f'{self.surname} {self.name}'

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name}'
    
    def get_linked_clients_count(self):
        return self.clients.count()