from django.contrib import admin
from django.urls import path
from .views import companyList, add_company, EditCompany, companyDetails, showAllContacts, EditContactView, DeleteCompanyView, addContact, searchCompany

urlpatterns = [
    path('', companyList, name='company_list'),
    path('add-company/', add_company, name='add_company'),
    path('<int:pk>/edit-company', EditCompany.as_view(), name='edit_company'),
    path('<int:id>/detail', companyDetails, name='detail_company'),
    path('<int:company_id>/all-contacts', showAllContacts, name='show_all_contact'),
    path('<int:company_id>/edit-contacts', EditContactView.as_view(), name='edit_contact'),
    path('<int:pk>/delete-company', DeleteCompanyView.as_view(), name='delete_company'),
    path('<int:id>/add-contact', addContact, name='add_contact'),
    path('search/', searchCompany, name='search_company'),
]