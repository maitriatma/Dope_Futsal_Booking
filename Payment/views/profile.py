from django.shortcuts import render, redirect
from django.views import View
from Payment.models.customer import Customer
from Payment.forms import updateprofile, updatecustomer
from Payment.models.profile import Profile


class Userprofile(View):
    def get(self, request):
        customer = request.session.get('customer')
        all_customer = Customer.get_all_customers();
        return render(request, 'userprofile.html', {'all_customer': all_customer})



def update_profile(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        fm = updatecustomer(request.POST, request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('userprofile')
        else:
            pi = Customer.objects.get(pk=id)
            fm = updatecustomer(instance=pi)
    else:
        pi = Customer.objects.get(pk=id)
        fm = updatecustomer(instance=pi)
    return render(request, 'updateprofile.html', {'form': fm})








"""
class Userprofile(View):
    def get(self, request):
        customer = request.session.get('customer')
        profile = Profile.get_profile_by_customer(customer)
        all_customer = Customer.get_all_customers();
        print(profile)
        return render(request, 'userprofile.html', {'profile': profile, 'all_customer': all_customer})
"""








