"""
URL configuration for fixsmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . views import *


urlpatterns = [
    path('',home,name='home'),
    path('register',register,name='register'),
    path('login',login,name='login'),
    path('base',base,name='base'),
    path('dashboard',dashboard,name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('postcomplaint',postcomplaint,name='postcomplaint'),
    path('addemp',addemployee,name='addemp'),
    path('complaints',complaintlist,name='complaints'),
   path('deny/<int:complaint_id>/', deny_complaint, name='deny_complaint'),
   path('offcomplaints',officer_complaints,name='offcomplaints'),
   path('detailed/<int:complaint_id>/', detailed_complaint, name='detailed'),
   path('completed_complaints',completed_complaints,name='completed_complaints'),
   path('detailed_view/<int:complaint_id>/', detailed_view, name='detailed_view'),
   path('track_complaint',track_complaint,name='track_complaint'),
   path("changepass",changepassword,name="changepass"),
      path("allcomplaints",all_complaints,name="allcomplaints"),
      path("update_delete",update_delete,name="update_delete"),
       path('update/<int:officer_id>/', update_officer, name='update'),  # USE officer_id
    path('delete/<int:officer_id>/', delete_officer, name='delete'),
    path('users',user,name='users'),
    path('depts',add_delete,name='depts'),
    path('add_department/', add_department, name='add_department'),
path('delete_department/<int:id>/', delete_department, name='delete_department'),


   
     
]

