

from django.db import models

class SmartFix(models.Model):
    
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    
    landmark = models.CharField(max_length=100, blank=True, null=True)
    
    village = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    designated_at=models.CharField(max_length=200,default=None,null=True,blank=True)
    department=models.CharField(max_length=100,blank=True, null=True)
    position=models.CharField(max_length=100,blank=True, null=True,default='User')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"
    
    


class Complaint(models.Model):
    # User Info
    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile=models.CharField(max_length=15)
    complaint_date = models.DateTimeField(auto_now_add=True)


    # Recipient Info
    recipient_name = models.CharField(max_length=100, default='FixSmart')
    recipient_position = models.CharField(max_length=100, default='Co-ordinator')
    recipient_department = models.CharField(max_length=100)

    # Address
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    mandal = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    assigned_to=models.CharField(max_length=100, blank=True,null=True)
    suggestion = models.TextField(blank=True, null=True)

    # Complaint Content
    message = models.TextField()
    signature = models.CharField(max_length=150)
    
    # Captured Image from camera (stored as base64 or image, here using ImageField)
    captured_image = models.ImageField(upload_to='complaint_images/', blank=True)

    # Resolution Details
    status = models.CharField(max_length=20, default='Pending')  # Pending / Solved
    solved_image = models.ImageField(upload_to='solved_images/', blank=True, null=True)
    solved_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.recipient_department} - {self.status}"
    
    
    
    
class Departments(models.Model):
    name = models.CharField(max_length=100, unique=True)


