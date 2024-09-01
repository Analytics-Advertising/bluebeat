import json
import os
from django.shortcuts import render
from system_management.sendsms import new_account_sms
from system_management.sendmail import new_account
from system_management.models import User
from .models import Address, Application, ContractAcknowledgement, DealerCommercial, CommercialSchedule
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings
import base64
from django.core.files.base import ContentFile
from .models import DocumentType, Document
from django.db import IntegrityError
from urllib.parse import urlparse

# Create your views here.


def dashboard(request):
    return render(request, 'dealer/dashboard.html')


def commercials(request):
    has_commercial = DealerCommercial.objects.select_related('dealer', 'commercial_schedule').all()
    
    print(has_commercial)
    context = {
        'has_commercial': has_commercial
    }
    return render(request, 'dealer/commercials.html', context)

def submit_application(request):

    url = request.build_absolute_uri()
    parsed_url = urlparse(url)
    url = parsed_url.scheme + "://" + parsed_url.netloc

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Generate a random password
                password = get_random_string(length=8)

                # Extract user data
                user_data = {
                    'email': request.POST.get('app-email'),
                    'phone_number': request.POST.get('app-phone-number'),
                    'first_name': request.POST.get('app-first-name'),
                    'last_name': request.POST.get('app-last-name'),
                    'password': password,
                }

                # Check if user exists
                try:
                    user = User.objects.get(email=user_data['email'])
                    # User already exists, handle error
                    return JsonResponse({'error': 'User with this email already exists.'}, status=400)
                except User.DoesNotExist:
                    # Create user if not exists
                    user = User.objects._create_user(
                        email=user_data['email'],
                        phone_number=user_data['phone_number'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        password=user_data['password']
                    )

                # Extract address data
                address_data = {
                    'user': user,
                    'street_address': request.POST.get('app-street-address'),
                    'city': request.POST.get('app-city'),
                    'suburb': request.POST.get('app-suburb'),
                    'province': request.POST.get('app-province'),
                    'postal_code': request.POST.get('app-postal-code'),
                }

                # Create Address instance
                address_instance = Address.objects.create(**address_data)

                # Extract application data
                application_data = {
                    'user': user,
                    'alternative_phone_number': request.POST.get('app-alternative-phone-number'),
                    'id_number': request.POST.get('app-id-number'),
                    'direct_phone_number': request.POST.get('app-direct-phone-number'),
                    'has_experience': request.POST.get('app-experience'),
                    'experience_details': request.POST.get('app-experience-details'),
                    'previous_companies': request.POST.get('app-previous-companies'),
                    'distribution_method': request.POST.get('app-distribution-method'),
                    'other_method': request.POST.get('app-other-method'),
                    'distribution_area': request.POST.get('app-distribution-area'),
                    'rica_access': request.POST.get('app-rica-access'),
                    'required_networks': request.POST.get('app-required-networks'),
                    'best_networks': request.POST.get('app-best-networks'),
                    'vat_registered': request.POST.get('app-vat-registration'),
                    'average_activations': request.POST.get('app-average-activations'),
                    'preferred_communication': request.POST.get('app-preferred-communication'),
                    'airtime_solution': request.POST.get('app-airtime-solution'),
                    'hear_about_us': request.POST.get('app-hear-about-us'),
                }

                # Create Application instance
                application_instance = Application.objects.create(**application_data)
                # new_account( user.email, user.first_name, password, url )
                message_body = f"Dear {user.first_name}, \n\nThank you for submitting your application to BlueBeat Digital. \n\nYour password is {password} and your login email is {user.email}. \n\nPlease login to {url} to complete your application."
                new_account_sms(user.phone_number, message_body)


                # Return success response
                return JsonResponse({'message': 'Application submitted successfully.'}, status=200)

        except ValidationError as ve:
            return JsonResponse({'error': ve.message_dict}, status=400)
        except Exception as e:
            # Rollback user and address creation if application creation fails
            if 'user' in locals() and 'address_instance' in locals():
                address_instance.delete()
                user.delete()
            elif 'user' in locals():
                user.delete()
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def choose_schedule(request):

    if request.method == "POST":
        schedule_name = request.POST.get('schedule')
        schedule = get_object_or_404(CommercialSchedule, name=schedule_name)
        
        # Assuming the dealer is identified by the logged-in user
        dealer = request.user
        
        # Create or update the dealer's commercial schedule
        DealerCommercial.objects.update_or_create(
            dealer=dealer,
            defaults={'commercial_schedule': schedule}
        )
        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'})



def agreements(request):
    try:
        acknowledgment = ContractAcknowledgement.objects.get(dealer=request.user)
        all_signed = (
            acknowledgment.section_1 and
            acknowledgment.section_2 and
            acknowledgment.section_3 and
            acknowledgment.section_4 and
            acknowledgment.section_5
        )
    except ContractAcknowledgement.DoesNotExist:
        all_signed = False
    
    context = {
        'all_signed': all_signed,
        'date_signed': acknowledgment.date_acknowledged if all_signed else None
    }
    
    return render(request, 'dealer/agreements/agreements.html', context)


def choose_contract(request):
    return render(request, 'dealer/agreements/agreements.html')


def acknowledgment_section(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        dealer = request.user

        try:
            acknowledgment = ContractAcknowledgement.objects.get(dealer=dealer)
        except ContractAcknowledgement.DoesNotExist:
            acknowledgment = ContractAcknowledgement(dealer=dealer)

        acknowledgment.section_1 = data.get('section_1', False)
        acknowledgment.section_2 = data.get('section_2', False)
        acknowledgment.section_3 = data.get('section_3', False)
        acknowledgment.section_4 = data.get('section_4', False)
        acknowledgment.section_5 = data.get('section_5', False)
        acknowledgment.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def acknowledgment_state(request):
    try:
        acknowledgment = ContractAcknowledgement.objects.get(dealer=request.user)
        all_signed = (
            acknowledgment.section_1 and
            acknowledgment.section_2 and
            acknowledgment.section_3 and
            acknowledgment.section_4 and
            acknowledgment.section_5
        )
        state = {
            'section_1': acknowledgment.section_1,
            'section_2': acknowledgment.section_2,
            'section_3': acknowledgment.section_3,
            'section_4': acknowledgment.section_4,
            'section_5': acknowledgment.section_5,
            'all_signed': all_signed,
        }
    except ContractAcknowledgement.DoesNotExist:
        state = {
            'section_1': False,
            'section_2': False,
            'section_3': False,
            'section_4': False,
            'section_5': False,
            'all_signed': False,
        }
    return JsonResponse(state)

def view_contract(request):
    return render(request, 'dealer/agreements/contract.html')

def verification_documents(request):
    return render(request, 'dealer/verification_documents/verification_documents.html')

def upload_documents(request):
    print("hahaha")

    if request.method == 'POST':
        try:
            # Decode base64 data and save documents
            id_number_base64 = request.POST.get('idNumber')
            proof_of_bank_account_base64 = request.POST.get('proofOfBankAccount')
            proof_of_residence_base64 = request.POST.get('proofOfResidence')
            nok_id_number_base64 = request.POST.get('nokIdNumber')
            proof_of_funding_base64 = request.POST.get('proofOfFunding')

            # Create and save documents
            save_document(request.user, id_number_base64, 'ID Number/Passport')
            save_document(request.user, proof_of_bank_account_base64, 'Proof of Bank Account')
            save_document(request.user, proof_of_residence_base64, 'Proof of Residence')
            save_document(request.user, nok_id_number_base64, 'Next of Kins ID Document')
            save_document(request.user, proof_of_funding_base64, 'Proof of Funding')


            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def save_document(user, base64_data, doc_type):
    print(doc_type)
    if base64_data:
        # Get or create document
        document_type = DocumentType.objects.get(doc_type=doc_type)
        try:
            document = Document.objects.get(user=user, document_type=document_type)
            document.document = base64_data  # Update existing document
        except Document.DoesNotExist:
            document = Document(user=user, document_type=document_type, document=base64_data)

        # Save document to database
        try:
            document.save()
        except IntegrityError:
            # Handle integrity error (e.g., unique constraint violation)
            # This could happen if there's an attempt to create a new document for the same user and type
            pass


def sign_contract_online(request):
    pass
def get_documents(request):
    user = request.user  # Assuming the user is authenticated
    documents = Document.objects.filter(user=user)

    data = []
    for document in documents:
        data.append({
            'doc_type': document.document_type.doc_type,
            'document': document.document
        })

    return JsonResponse(data, safe=False)

def download_document(request, document_id):
    user = request.user  # Assuming the user is authenticated
    document = Document.objects.get(id=document_id, user=user)

    response = HttpResponse(document.document, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(document.id)
    return response
