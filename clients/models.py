from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Max

class Client(models.Model):

    name = models.CharField(
        max_length=255,
        unique=False,
        help_text="Client name"
    )

    client_code = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        blank=True,
        null=True,
        help_text="Auto-generated unique client code"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        indexes = [
            models.Index(fields=['client_code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.client_code})" if self.client_code else self.name

    def save(self, *args, **kwargs):


        if not self.client_code:
            for _ in range(5):  
                try:
                    with transaction.atomic():
                        self.client_code = self._generate_client_code()
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    continue
            raise ValidationError("Unable to generate unique client code")

        super().save(*args, **kwargs)

    def _get_prefix(self):
        words = self.name.upper().split()
        
        if len(words) >= 3:
            return ''.join(word[0] for word in words[:3])

        elif len(words) == 2:
            return words[0][0] + words[1][0] + words[1][1]

        elif len(words) == 1:
            word = ''.join(c for c in words[0] if c.isalpha())
            return (word + 'ABC')[:3]

        return "ABC"


    def _generate_client_code(self):
        
        prefix = self._get_prefix()

        max_code = Client.objects.filter(
            client_code__startswith=prefix
        ).aggregate(max_code=Max('client_code'))['max_code']

        if max_code:
            next_number = int(max_code[-3:]) + 1
        else:
            next_number = 1

        if next_number > 999:
            raise ValidationError("Client code limit reached")

        return f"{prefix}{next_number:03d}"
   
    def get_linked_contacts_count(self):
        return self.contacts.count()