from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Max

class Client(models.Model):

    name = models.CharField(
        max_length=255,
        unique=False,
        help_text="Client name"
    )
    # description = models.TextField(
    #     blank=True,
    #     null=True,
    #     help_text="Additional client information"
    # )
    client_code = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        help_text="Auto-generated unique client code"
    )
    # client_type = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True,
    #     help_text="Type of client (e.g., Bank, Retail, etc.)"
    # )
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
            for _ in range(5):  # retry for race condition
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
    
            # Multi-word case → take first letters
            if len(words) >= 3:
                return ''.join(word[0] for word in words[:3])
    
            elif len(words) == 2:
                return words[0][0] + words[1][0] + words[1][1]
    
            elif len(words) == 1:
                word = ''.join(c for c in words[0] if c.isalpha())
                return (word + 'ABC')[:3]
    
            return "ABC"


    def _generate_client_code(self):
        
        name = self.name.upper().strip()
        alpha_chars = ''.join(c for c in name if c.isalpha())
       
        if len(alpha_chars) < 3:
            alpha_chars = (alpha_chars + 'A' * 3)[:3]
        else:
            alpha_chars = alpha_chars[:3]
        
       
        numeric_suffix = 1
        while numeric_suffix <= 999:
            potential_code = f"{alpha_chars}{numeric_suffix:03d}"
            if not Client.objects.filter(client_code=potential_code).exists():
                return potential_code
            numeric_suffix += 1
        
        raise ValidationError("Unable to generate unique client code")

    def get_linked_contacts_count(self):
        return self.contacts.count()