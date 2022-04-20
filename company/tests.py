from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import *

class CompanyTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )

        self.company = Company.objects.create(
        name = 'A test company',
        address = 'California',
        contract = 'bronze'
        )
    def test_string_representation(self):
        company = Company(name='A test company')
        self.assertEqual(str(company), company.name)

    def test_company_details(self):
        self.assertEqual(f'{self.company.name}', 'A test company'),
        self.assertEqual(f'{self.company.address}', 'California'),
        self.assertEqual(f'{self.company.contract}', 'bronze')

    def test_company_list_view(self):
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A test company')


    def test_company_create_view(self):
        self.client.login(email='test@email.com', password='secret')
        response = self.client.post(reverse('add_company'), {
            "name": "New title", "address": "California", "contract": "bronze"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
        self.assertContains(response, 'California')
