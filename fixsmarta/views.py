from django.shortcuts import render,redirect
from django.contrib import messages
from . serializers import *
from django.contrib.auth import logout

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        serializer=Register(data=request.POST)
        if serializer.is_valid():
             serializer.save()
             messages.success(request, "Registration successful!")
             return redirect('login')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('register')
            
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        if SmartFix.objects.filter(email=email,password=password).exists():
            request.session['email']=email
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
      
    return render(request,'login.html')

from django.contrib.auth import logout as django_logout

def logout_view(request):
    request.session.pop('email', None)
    django_logout(request)
    return redirect('login')



def base(request):
    
    email=request.session.get('email')
    if email is None:
        messages.error(request, "Please login")
        
        return redirect('login')
    else:
        user=SmartFix.objects.filter(email=email).first()
    return render(request,'base.html',{'user':user})

def dashboard(request):
    email=request.session.get('email')
    if email is None:
        messages.error(request, "Please login")
        
        return redirect('login')
    else:
        user=SmartFix.objects.filter(email=email).first()
    return render(request,'dashboard.html',{'user':user})

import base64
import uuid
from django.core.files.base import ContentFile


def postcomplaint(request):
    email = request.session.get('email')
    depts=Departments.objects.all()

    if email is None:
        messages.error(request, "Please login")
        return redirect('login')

    user = SmartFix.objects.filter(email=email).first()

    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        date = request.POST.get('date')

        recipient_name = request.POST.get('recipientName')
        recipient_position = request.POST.get('recipientPosition')
        recipient_department = request.POST.get('recipient_department')

        address = request.POST.get('address')
        message = request.POST.get('message')
        signature = request.POST.get('signature')
        pincode = request.POST.get('pincode')

        landmark = request.POST.get('landmark')
        area = request.POST.get('area')
        village = request.POST.get('village')
        mandal = request.POST.get('mandal')
        district = request.POST.get('district')

        captured_image_data = request.POST.get('captured_image')

        # Process captured base64 image
        image_file = None
        if captured_image_data and "base64," in captured_image_data:
            format, imgstr = captured_image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"{uuid.uuid4()}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

        # Save complaint
        Complaint.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            complaint_date=date,

            recipient_name=recipient_name,
            recipient_position=recipient_position,
            recipient_department=recipient_department,

            address=address,
            message=message,
            signature=signature,
            pincode=pincode,

            landmark=landmark,
            area=area,
            village=village,
            mandal=mandal,
            district=district,

            captured_image=image_file,
        )

        messages.success(request, "Complaint submitted successfully!")
        return redirect('postcomplaint')

    return render(request, 'postcomplaint.html', {'user': user,"depts":depts})

from .froms import *

def addemployee(request):
    depts=Departments.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)  # ✅ This works for file upload
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('addemp')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    
    return render(request, 'addemp.html', {'form': form,"depts":depts})


def complaintlist(request):
    email = request.session.get('email')
    print("User email is: ", email)

    if not email:
        return redirect('login')
    
    if request.method == 'POST':
        id=request.POST['id']
        assigned_to=request.POST['assigned_to']
        Complaint.objects.filter(id=id).update(assigned_to=assigned_to,status="Ongoing")
        messages.success(request, f"{assigned_to} assigned to this complaint successfully!")

    user = SmartFix.objects.get(email=email)
    print('User Details: ', user)

    complaints = Complaint.objects.filter(mandal=user.mandal,status="Pending")
    print('Complaints: ', complaints)

    user_complaints = Complaint.objects.all()
    officers = SmartFix.objects.filter(position="Officer")
    

    context = {
        'complaints': complaints,
        'error': '',
        'officers': officers,
        
    }

    return render(request, 'complaintlist.html', context)

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Complaint

def deny_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = "Denied Complaint"
    complaint.save()
    return redirect ('complaints')  # Or wherever you want to go after

def officer_complaints(request):
    email = request.session.get('email')
    complaint=Complaint.objects.filter(assigned_to=email,status="Ongoing")
    for c in complaint:
        print("yes" if c.assigned_to == email else "no")

    return render(request, 'officercomplaints.html', {'complaint': complaint})

def detailed_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, status="Ongoing")

    if request.method == "POST":
        base64_image = request.POST.get('solved_image')

        if base64_image and base64_image.startswith("data:image"):
            # Split the base64 string and decode
            format, imgstr = base64_image.split(';base64,')  
            ext = format.split('/')[-1]  # Get image extension (e.g., png)
            file_name = f"solved_{complaint.id}.{ext}"

            # Create a Django ContentFile
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            # Save to the model
            complaint.solved_image = image_file
            complaint.status = "Solved"
            from django.utils.timezone import now
            complaint.solved_date = now()
            complaint.save()
            messages.success(request, 'Complaint marked as solved and image uploaded successfully.')

    return render(request, 'detailedcomplaint.html', {'complaint': complaint})


def completed_complaints(request):
    email=request.session.get('email')
    user=SmartFix.objects.get(email=email)
    if user.position=="User":
        completed_complaints = Complaint.objects.filter(email=email,status="Solved")
    elif user.position=="Officer":
        completed_complaints = Complaint.objects.filter(assigned_to=email,status="Solved")
        
    elif user.position=="Co-ordinator":
        completed_complaints = Complaint.objects.filter(mandal=user.mandal,status="Solved")
    
        
        
    return render(request, 'Complaints.html', {'completed_complaints': completed_complaints})

def detailed_view(request, complaint_id):
    complaint = get_object_or_404(Complaint,id=complaint_id,status="Solved")
    return render(request, 'detailedview.html', {'complaint': complaint})

from django.db.models import Q

def track_complaint(request):
    email=request.session.get('email')
    user=SmartFix.objects.get(email=email)
    if user.position=="User":
        complaints = Complaint.objects.filter(Q(status="Pending") | Q(status="Ongoing") | Q (status="Denied Complaint"),email=email)
    if user.position=="Officer":
        complaints = Complaint.objects.filter(Q(status="Pending") | Q(status="Ongoing") | Q (status="Denied Complaint"),assigned_to=email)
    elif user.position=="Co-ordinator":
        complaints = Complaint.objects.filter(Q(status="Pending") | Q(status="Ongoing") | Q (status="Denied Complaint"),mandal=user.mandal)
    
    return render(request, 'trackcomplaint.html', {'complaints': complaints})

def changepassword(request):
    email=request.session.get('email')
    if request.method == 'POST':
        old_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = SmartFix.objects.get(email=email)
        if user.password == old_password:
            if new_password == confirm_password:
                user.password = new_password
                user.save()
                messages.success(request, 'Password changed successfully')
    return render(request, 'changepassword.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SmartFix, Complaint

def all_complaints(request):
    email = request.session.get('email')
    try:
        user = SmartFix.objects.get(email=email)
    except SmartFix.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    complaints = Complaint.objects.all()

    if user.position == "Admin":
        filter_by = request.GET.get('filter_by')
        search = request.GET.get('search')

        if filter_by and search:
            if filter_by in ["Solved", "Ongoing", "Pending"]:
                complaints = complaints.filter(status__iexact=filter_by, mandal__icontains=search)
            elif filter_by == "Mandal":
                complaints = complaints.filter(mandal__icontains=search)
            elif filter_by == "Pincode":
                complaints = complaints.filter(pincode__icontains=search)
            elif filter_by == "District":
                complaints = complaints.filter(district__icontains=search)
            elif filter_by == "State":
                complaints = complaints.filter(state__icontains=search)

        return render(request, 'allcomplaints.html', {
            'complaints': complaints,
            'filter_by': filter_by,
            'search': search,
            
            
        })
    else:
        messages.error(request, "You are not authorized to view this page")
        return redirect('home')
    
    
def update_delete(request):
    query = request.GET.get('q', '')
    officers = SmartFix.objects.filter(Q(position="Officer") | Q(position="Co-ordinator"))

    if query:
        officers = officers.filter(
            Q(fname__icontains=query) |
            Q(mname__icontains=query) |
            Q(lname__icontains=query) |
            Q(email__icontains=query) |
            Q(mobile__icontains=query) |
            Q(village__icontains=query) |
            Q(mandal__icontains=query) |
            Q(pincode__icontains=query) |
            Q(district__icontains=query) |
            Q(state__icontains=query) |
            Q(department__icontains=query) |
            Q(landmark__icontains=query) |
            Q(designated_at__icontains=query)
        )

    return render(request, 'update_delete.html', {'officers': officers, 'query': query})


def delete_officer(request, officer_id):
    officer = get_object_or_404(SmartFix, id=officer_id)
    officer.delete()
    return redirect('update_delete')

def update_officer(request, officer_id):
    officer = get_object_or_404(SmartFix, id=officer_id)

    if request.method == 'POST':
        serializer = Register(officer, data=request.POST, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Updated Successfully")
        else:
            messages.error(request, "Error updating officer")

       
        return redirect('update_delete')  

    
    return redirect('update_delete')


def user(request):
    user=SmartFix.objects.filter(position='User')
    return render(request, 'user.html', {'user':user})


def add_delete(request):
    depts=Departments.objects.all().order_by('id')
    return render(request, 'add_delete.html', {'depts':depts})

def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Departments.objects.create(name=name)
    return redirect('depts')

def delete_department(request, id):
    Departments.objects.filter(id=id).delete()
    return redirect('depts')










