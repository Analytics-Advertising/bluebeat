from django.conf import settings
from datetime import datetime
from django.template.loader import get_template
from django.core.mail import EmailMessage



def new_account(email, first_name, password, url):

    email_subject = 'BlueBeat - Welcome to Our Platform!'

    html_tpl_path = 'email_temps/new_user.html'

    context_data = {'first_name': first_name, 'email':email, 'password': password,
                    'url': url}

    email_html_template = get_template(html_tpl_path).render(context_data)

    receiver_email = email

    email_msg = EmailMessage(email_subject,
                             email_html_template,
                             settings.DEFAULT_FROM_EMAIL,
                             [receiver_email],
                             reply_to=[settings.DEFAULT_FROM_EMAIL])

    email_msg.content_subtype = 'html'

    email_msg.send(fail_silently=False)


def send_email(email_subject, email_message, student_email,student_name, student_lastname, url):


    email_subject = email_subject

    html_tpl_path = 'email_temps/send_applicant_email.html'

    context_data = {'first_name': student_name, 'last_name':student_lastname, 
                    'email_message': email_message, 'email_subject': email_subject,
                    'url': url}

    email_html_template = get_template(html_tpl_path).render(context_data)

    receiver_email = student_email

    email_msg = EmailMessage(email_subject,
                             email_html_template,
                             settings.DEFAULT_FROM_EMAIL,
                             [receiver_email],
                             reply_to=[settings.DEFAULT_FROM_EMAIL])

    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)


def send_status_email(email, first_name, status, url):
    # Set the subject based on the approval status
    email_subject = f'BlueBeat - Application {status}'

    # Define the path to the email template
    if status == 'Approved':
        html_tpl_path = 'email_temps/application_approved.html'
    else:
        html_tpl_path = 'email_temps/application_rejected.html'

    # Create the context for the email template
    context_data = {'first_name': first_name, 'status': status, 'url': url}

    # Render the email template with context data
    email_html_template = get_template(html_tpl_path).render(context_data)

    # Define the receiver email
    receiver_email = email

    # Create and send the email
    email_msg = EmailMessage(email_subject,
                             email_html_template,
                             settings.DEFAULT_FROM_EMAIL,
                             [receiver_email],
                             reply_to=[settings.DEFAULT_FROM_EMAIL])

    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)