from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from system_management.sendsms import send_status_sms
from system_management.models import User, UserType
from system_management.sendmail import send_status_email
from dealer.models import Address, Application, Document
from django.http import JsonResponse, HttpResponse

# Create your views here.
@login_required
def dashboard(request):

    applications = Application.objects.all()
    approved_applications = Application.objects.filter(status='approved')
    rejected_applications = Application.objects.filter(status='rejected') 

    context = {
        'applications':applications,
        'approved_applications':approved_applications,
        'rejected_applications':rejected_applications
        
    }
        
    return render(request, 'dashboard/dashboard.html', context)


def applications(request):

    applications = Application.objects.all() 

    context = {
        'applications':applications,

    }
        
    return render(request, 'application/applications.html', context)


def applicant_view(request, application_id):

    applicant = get_object_or_404(Application, pk=application_id)

    applicant_address = get_object_or_404(Address, user=applicant.user)
    documents = Document.objects.filter(user=applicant.user)

    context = {
        'applicant': applicant,
        'applicant_address':applicant_address,
        'documents': documents,
        'application_id': application_id 
    }
    return render(request, 'application/applicant/applicantview.html', context)


def user_management(request):
    
    all_users = User.objects.filter(user_type__in=[1,2])
    user_types = UserType.objects.all()

    context = {
        'users': all_users,
        'user_types': user_types
    }



    return render(request, 'dashboard/users/users.html', context)

import json
def send_status_email_view(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        application_id = data.get('application_id')
        status = data.get('status')
        
        # Fetch the application and user details
        application = get_object_or_404(Application, pk=application_id)
        user = application.user
        user_email = user.email
        user_first_name = user.first_name
        
        # URL can be provided if needed, or set to None
        url = 'https://bluebeat.digital/login'
        
        if status == 'approved':
            send_status_email(user_email, user_first_name, 'approved', url)
        elif status == 'rejected':
            send_status_email(user_email, user_first_name, 'rejected', url)
        else:
            return JsonResponse({'message': 'Invalid status'}, status=400)
        
        return JsonResponse({'message': 'Email sent successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    

def update_application_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        application_id = data.get('application_id')
        status = data.get('status')
        
        # Fetch the application
        application = get_object_or_404(Application, pk=application_id)

        # Update the status
        application.status = status
        application.save()

        # Optionally, send an email or perform other actions based on the status
        if status in ['Approved', 'Rejected']:
            user = application.user
            user_email = user.email
            user_first_name = user.first_name
            
            # URL can be provided if needed, or set to None
            url = 'https://bluebeat.digital/login'
            
            # send_status_email(user_email, user_first_name, status.lower(), url)
            send_status_sms(user_email, user_first_name, status.lower(), url)

        return JsonResponse({'message': 'Status updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)