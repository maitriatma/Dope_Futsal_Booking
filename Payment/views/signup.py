from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from Payment.models.customer import Customer
from django.views import View


class Signup(View):
    def get(self, request):
        customer = Customer.get_all_customers();
        return render(request, 'signup.html', {'customer': customer})

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        # saving
        if not error_message:
            print(first_name, last_name, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
        return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required!"
        elif len(customer.first_name) < 4:
            error_message = "First Name must be 4 char long or more."
        elif not customer.last_name:
            error_message = "Last Name Required"
        elif len(customer.last_name) < 4:
            error_message = "Last Name must be 4 char long or more."
        elif len(customer.password) < 6:
            error_message = "Password must be 6 char long."
        elif len(customer.email) < 5:
            error_message = "Email must be 5 char long."
        elif customer.isExists():
            error_message = "Email address already registered."
        return error_message
