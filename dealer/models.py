from django.db import models
from system_management.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    suburb = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_address}, {self.suburb}, {self.city}, {self.province}, {self.postal_code}"
    
# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now=True)

        # New field
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Pre-Approved', 'Pre-Approved'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        # Add more choices as needed
    ], default='Pending')

    # Personal Details
    alternative_phone_number = models.CharField(max_length=10, blank=True, null=True)
    id_number = models.CharField(max_length=13)
    direct_phone_number = models.CharField(max_length=13, blank=True, null=True)
    
    # Experience and Distribution
    has_experience = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    experience_details = models.TextField(blank=True, null=True)
    previous_companies = models.CharField(max_length=255, blank=True, null=True)
    distribution_method = models.TextField()
    other_method = models.CharField(max_length=45, blank=True, null=True)
    distribution_area = models.CharField(max_length=255)
    rica_access = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    required_networks = models.CharField(max_length=255)
    best_networks = models.CharField(max_length=255)
    vat_registered = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    vat_number = models.CharField(max_length=45, blank=True,null=True)
    average_activations = models.CharField(max_length=45)
    
    # Additional Information
    preferred_communication = models.CharField(max_length=45)
    airtime_solution = models.TextField(blank=True, null=True)
    hear_about_us = models.CharField(max_length=255, choices=[
        ('Friend referred me', 'Friend referred me'),
        ('Facebook', 'Facebook'),
        ('LinkedIn', 'LinkedIn'),
        ('Other', 'Other')
    ])

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Application"
    

class CommercialSchedule(models.Model):
    name = models.CharField(max_length=45)
    date_created = models.DateTimeField(auto_now=True)


class DealerCommercial(models.Model):
    dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    commercial_schedule = models.ForeignKey(CommercialSchedule, on_delete=models.CASCADE)
    date_signed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dealer.username} - {self.commercial_schedule.name}"
    

class SignedContract(models.Model):
    name = models.CharField(max_length=255)
    date_signed = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    pdf_url = models.TextField()
    dealer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class ContractAcknowledgement(models.Model):
    dealer = models.ForeignKey(User, on_delete=models.CASCADE)
    section_1 = models.BooleanField(default=False)
    section_2 = models.BooleanField(default=False)
    section_3 = models.BooleanField(default=False)
    section_4 = models.BooleanField(default=False)
    section_5 = models.BooleanField(default=False)
    date_acknowledged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dealer.username} - {self.date_acknowledged}"
    



class DocumentType(models.Model):

    DOC_TYPE = (
        ('id number/passport', 'ID Number/Passport'),
        ('proof of bank account', 'Proof of Bank Account'),
        ('proof of residence', 'Proof of Residence'),
        ('live photo', 'Live Photo'),


    )

    doc_type = models.CharField(max_length=250, choices=DOC_TYPE)

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)