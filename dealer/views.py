import json
import os
from django.shortcuts import render
from system_management.sendsms import new_account_sms
from system_management.sendmail import new_account
from system_management.models import User
from .models import Address, Application, ContractAcknowledgement, DealerCommercial, CommercialSchedule, SignedContract
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
from django.utils import timezone
from PyPDF2 import PdfReader, PdfWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.contrib.auth.decorators import login_required



# Create your views here.


def dashboard(request):
    return render(request, 'dealer/dashboard.html')


def commercials(request):
    try:
        has_commercial = DealerCommercial.objects.get(dealer=request.user)
    except DealerCommercial.DoesNotExist:
        has_commercial = None

    # check if vat registered is true in application model
    is_vat_registered = Application.objects.get(user=request.user).vat_registered

    
    print(has_commercial)

    context = {
        'has_commercial': has_commercial,
        'is_vat_registered': is_vat_registered
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
                    'vat_registered': request.POST.get('vat-number"'),
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

    signed_documents = SignedContract.objects.filter(dealer=request.user)

    is_contract_signed = SignedContract.objects.filter(dealer=request.user, is_signed=True).exists()
    
    context = {
        'all_signed': all_signed,
        'date_signed': acknowledgment.date_acknowledged if all_signed else None,
        'signed_documents': signed_documents,
        'is_contract_signed': is_contract_signed
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
            live_photo_base64 = request.POST.get('livePhoto')
            # Create and save documents
            save_document(request.user, id_number_base64, 'ID Number/Passport')
            save_document(request.user, proof_of_bank_account_base64, 'Proof of Bank Account')
            save_document(request.user, proof_of_residence_base64, 'Proof of Residence')
            save_document(request.user, nok_id_number_base64, 'Next of Kins ID Document')
            save_document(request.user, proof_of_funding_base64, 'Proof of Funding')
            save_document(request.user, live_photo_base64, 'Live Photo')


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

@login_required
def sign_document(request):
    if request.method == "POST":
        data = json.loads(request.body)
        document_path = data.get("document_path")
        if not document_path:
            return JsonResponse({"success": False, "error": "Document path is missing."})
        
        # check if user has read terms and conditions
        try:
            acknowledgment = ContractAcknowledgement.objects.get(dealer=request.user)
            all_signed = (
                acknowledgment.section_1 and
                acknowledgment.section_2 and
                acknowledgment.section_3 and
                acknowledgment.section_4 and
                acknowledgment.section_5
            )
            if not all_signed:
                return JsonResponse({"success": False, "error": "Please read and accept the terms and conditions."})
        except ContractAcknowledgement.DoesNotExist:
            all_signed = False
            return JsonResponse({"success": False, "error": "Please read and accept the terms and conditions."})
        
            
        print(all_signed)
        try:
            # Extract user details
            first_name = request.user.first_name
            last_name = request.user.last_name
            user_id_number = Application.objects.filter(user=request.user).first().id_number

            reader = PdfReader(document_path)
            writer = PdfWriter()

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]

                # Create a new PDF for annotations
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)

                if page_num == 0:  # Only add name and ID on the first page
                    # Add first and last name on the first line in the middle
                    name_text = f"{first_name} {last_name}"
                    can.drawCentredString(330, 330, name_text)  # Adjust Y position as needed

                    # Add the ID number below the name
                    can.drawCentredString(350, 295, user_id_number)  # Adjust Y position as needed

                # Add initials on every page (as before)
                user_initials = ''.join([name[0].upper() for name in request.user.get_full_name().split()])
                can.drawString(80, 20, user_initials)  # Adjust position as needed

                can.save()

                # Move to the beginning of the StringIO buffer
                packet.seek(0)
                new_pdf = PdfReader(packet)
                new_page = new_pdf.pages[0]

                # Merge the new PDF with the existing page
                page.merge_page(new_page)
                writer.add_page(page)

            # Save the signed PDF to a buffer
            buffer = BytesIO()
            writer.write(buffer)
            buffer.seek(0)

            # Encode the signed PDF as base64
            signed_pdf_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            # Save the signed document to the database
            SignedContract.objects.create(
                name=document_path.split('/')[-1],
                date_signed=timezone.now(),
                description="Agreement",
                dealer=request.user,
                pdf_url=signed_pdf_base64,
                is_signed=True
            )

            return JsonResponse({"success": True, "message": "Document signed successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)



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


def view_signed_document(request, document_id):
    try:
        signed_document = SignedContract.objects.get(pk=document_id)
        if signed_document.is_signed:
            pdf_data = base64.b64decode(signed_document.pdf_url)
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{signed_document.name}"'
            return response
        else:
            return HttpResponse("Document not found or not signed.", status=404)
    except SignedContract.DoesNotExist:
        return HttpResponse("Document not found.", status=404)