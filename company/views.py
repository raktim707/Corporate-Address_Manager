from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contact, Company
from .forms import CompanyForm
from django.contrib import messages
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet, ContactForm
from django.contrib.auth.decorators import login_required


def companyList(request):
    # retireve all companies from the database
    all_companies = Company.objects.all()

    # get the total number of companies on the database
    count = Company.objects.count()
    # create paginator with 12 companies per page
    paginator=Paginator(all_companies, 12)
    page = request.GET.get('page')
    try:
        companies=paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    return render(request, 'company/all_company_list.html', {'companies': companies, 'count': count})

@login_required
def add_company(request):
    #if a GET method we'll create a blank form
    if request.method == 'GET':
        form = CompanyForm(request.GET or None)
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            company_name = form.data['name']
            company_address = form.data['address']
            company_contract = form.data['contract']
            company_email = form.data['email']
            company_phone = form.data['phone']

            try:
                # Check if a company already exist in the database by the same name
                companyExist = Company.objects.get(name=company_name)
            except:
                companyExist = None
            # If it exists, do no create a new company instance. Only add the contact details to database for the company
            if companyExist:
                # if valid email and phone number has given as input create new contact for the company
                if company_email or company_phone:
                    companyExist.contact_set.create(email=company_email, phone=company_phone)
                    messages.info(request, 'Company already Exists in the database. Only the contact details has been added')
                else:
                    messages.error(request, 'Company already Exists in the database.')
            else:
                #else create a new company instance with the data from the form.
                company = Company.objects.create(name=company_name, address=company_address, contract=company_contract)
                # create the contact details of the company
                company.contact_set.create(email=company_email, phone=company_phone)
                messages.success(request, 'Company Information saved successfully')
            return redirect('/')
    return render(request, 'company/add_company.html', {'form': form})


def companyDetails(request, id):
    # retrieve the company associated with the requested id
    company = get_object_or_404( Company,id=id)
    # if company exist, retrieve the last added contact and pass it to context
    if company:
        contact = company.contact_set.last()
        return render(request, 'company/companyDetails.html', {'company': company, 'contact': contact})

# show all contacts of a company
def showAllContacts(request, company_id):
    # retrieve the company associated with the requested id
    company = get_object_or_404(Company, id=company_id)
    #if company exists, get all contact details of the company
    if company:
        contacts = company.contact_set.all()
        return render(request, 'company/all_contacts.html', {'company': company,'contacts':contacts})
    # else if company does not exist, redirect to home page
    else:
        return redirect('/')

# Company Information Edit view
class EditCompany(LoginRequiredMixin, UpdateView):
    # create the form using the model of Company
    model = Company
    # include all model fields of Company in the form
    fields = '__all__'
    template_name = 'company/editCompany.html'
    #if company information edited successfully,redirect to company list page
    success_url = reverse_lazy('company_list')

#edit contacts of a company
class EditContactView(LoginRequiredMixin,TemplateResponseMixin, View):
    template_name = 'company/formset.html'
    company = None
    login_url = 'login'
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.company, data=data)

    # get company id which will be required by the get and post request
    def dispatch(self, request, company_id):
        self.company = get_object_or_404(Company, id=company_id)
        return super().dispatch(request, company_id)

    def get(self, request, *args, **kwargs):
        #build an empty ModuleFormSetformset
        formset = self.get_formset()
        #and render it to the template together with the current Company object using the render_to_response() method provided by TemplateResponseMixin.
        return self.render_to_response({'company': self.company, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('show_all_contact', company_id=self.company.id)
        return self.render_to_response({'company':self.company, 'formset': formset})

class DeleteCompanyView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'company/delete_company.html'
    success_url = reverse_lazy('company_list')
    success_message = 'Company Deleted Successfully'
    login_url = 'login'

@login_required
def addContact(request, id):
    # get the company id
    company = get_object_or_404(Company, id=id)

    # if this is a post request and a company exist
    if request.method == 'POST':
        if company:
            #  create a form instance and populate it with data from the request
            form = ContactForm(request.POST)
            if form.is_valid():
                email = form.data['email']
                phone = form.data['phone']
                # if email or phone is provided, create a contact instance for the company
                if email or phone:
                    company.contact_set.create(email=email, phone=phone)
                    messages.success(request, 'Successfully addded new contact')
                # if no email or phone is provided, generate error message
                else:
                    messages.error(request, 'No contacts were provided')
                return redirect('show_all_contact', company_id=company.id)
    # if this is a get request, display the empty form
    else:
        form = ContactForm()
    return render(request, 'company/add_contact.html', {'form':form, 'company':company})

def searchCompany(request):
    # Retrieve the search keyword from user input
    query = request.GET.get('search')
    results = []
    count=0
    if query:
        # if query exists, convert it to lowercase
        # to check against company names to find a match
        query=query.lower()
        companies = Company.objects.all()
        for company in companies:
            # convert the company names to lowercase to check against the query
            name = company.name.lower()
            # if company name has multiple words,
            # split it word by word to check if the query matches with any of the word
            name=name.split()
            if query in name:
                # if query matches with a word containing in a company name
                # append the company to result
                results.append(company)
        count=len(results)

        # create pagination with 12 company names per page
        paginator=Paginator(results, 12)
        page = request.GET.get('page')
        try:
            companies=paginator.page(page)
        except PageNotAnInteger:
            companies = paginator.page(1)
        except EmptyPage:
            companies = paginator.page(paginator.num_pages)
    return render(request, 'company/search.html', {'query':query, 'companies':companies, 'count':count})
