from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from system_management.sendsms import new_account_sms
from system_management.models import User, UserType
from django.http import JsonResponse
from urllib.parse import urlparse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
            

def register_user(request):
    url = request.build_absolute_uri()
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        phone_number = request.POST.get('PhoneNumber')
        password = request.POST.get('password')
        user_type_id = request.POST.get('user-type')

        try:
            user_type = UserType.objects.get(id=user_type_id)
        except UserType.DoesNotExist:
            return JsonResponse({'error': 'Invalid user type'}, status=400)

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Validate form data
        if not all([first_name, last_name, email, phone_number, password, user_type]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Create a new user
        user = User.objects._create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
        
        user.save()
        
        # new_account(user.email, user.first_name, password, base_url)
        new_account_sms(user.phone_number, password)

        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def deactivate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.is_active = False
            user.save()
            return JsonResponse({'success': True, 'message': 'User deactivated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)




def get_user_details(request, user_id):
 
    user = get_object_or_404(User, id=user_id)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return JsonResponse(data)


def sign_out(request):
    logout(request)  # Log out the user
    return redirect('login') 
