from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    contract_choices = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )
    contract = models.CharField(max_length=10, choices=contract_choices)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('edit_company', kwargs={'pk':self.pk})

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    
    def __str__(self):
        return self.company.name

    
