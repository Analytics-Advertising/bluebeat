from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser


# Create your views here.


def home_application(request):
        
    return render(request, 'application/application_form.html')


def redirect_user(request):

    user = request.user
    if isinstance(request.user, AnonymousUser):
        return redirect('login')
    else:
        if user.user_type_id == 1: 
            print(user.user_type_id)
            return redirect('admin-dashboard')
        elif user.user_type_id == 2: 
            print(user.user_type_id)
            return redirect('dealer-dashboard')
        else:
            return redirect('login')
            
