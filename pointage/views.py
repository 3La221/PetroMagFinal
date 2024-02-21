import calendar
from datetime import timedelta
import locale
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from pointage.forms import *
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time
from django.contrib.auth import logout
from django.core.paginator import Paginator , EmptyPage
from .models import *

def pointage2(request,ID):
    station = Station.objects.get(id=ID)
    instances=Employe.objects.filter(station=station)
    date=datetime.now().date()
    date_range = [date + timedelta(days=i) for i in range(15)]
    paginator = Paginator(instances, 5)  # Change 10 to the number of items per page
    page_number = request.GET.get('page', 1)
    try:
        instances_paginated = paginator.page(page_number)
    except EmptyPage:
        instances_paginated = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        credentials = service_account.Credentials.from_service_account_file(
        './petropointage-b1093416d578.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
        )

        # Specify the ID of your Google Sheet
        spreadsheet_id = '15BSWan9Olz9WisDThGlGESdcZPw4GGIvnLyayFIP74I'
        service = build('sheets', 'v4', credentials=credentials)
        
        for i in instances:
            for date in date_range:
                cell=find_cell(date)
                choice=request.POST.get(f'{i.ID}_{date}')
                print(choice)
                sheet_range = f"{i.ID}!{cell}"
                code=Code_Employe.objects.filter(employe=i,Date=date)
                if not choice :
                    if code.exists():
                        values=[['']]
                        code.delete()
                    else:
                        continue
                else:
                    if code.exists():
                        code.delete()
                    code_emp=Code_Employe()
                    code_emp.employe=i
                    code_emp.Date=date 
                    code_emp.code=Code.objects.get(pk=choice)
                    code_emp.save()
                    values = [[f"{choice}"]]
                body = {'values': values}
                service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=sheet_range,
                valueInputOption='RAW', body=body
                ).execute()
        return redirect(main_view,i.ID)
    else:
        codes_emp=Code_Employe.objects.filter(employe__station=station)
        codes=Code.objects.all()
        context={'date':date,'instances':instances_paginated,'date_range':date_range,'codes':codes,'codes_emp':codes_emp}
        return render(request,'pointage.html',context)    

def logout_view(request):
    logout(request)
    return redirect("/")

def find_cell(date):
    if (date.day <=25):
        alphabet=chr(ord('B') + (date.day)%26 -1)
    else:
        alphabet="A"+chr(ord('A') + (date.day)%26)
    return (f"{alphabet}{date.month+13}")


def pointage(request,ID):
    if request.user.profile.station.id != ID  and (request.user.profile.da != 1) :
        return redirect("menu_view")
    instances=Employe.objects.filter(station=ID)
    date=datetime.now().date()
    date_range = [date + timedelta(days=i) for i in range(15)]

    if request.method == 'POST':
        credentials = service_account.Credentials.from_service_account_file(
        './petropointage-b1093416d578.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
        )

        # Specify the ID of your Google Sheet
        spreadsheet_id = '15BSWan9Olz9WisDThGlGESdcZPw4GGIvnLyayFIP74I'
        service = build('sheets', 'v4', credentials=credentials)
        
        for i in instances:
            for date in date_range:
                cell=find_cell(date)
                choice=request.POST.get(f'{i.ID}_{date}')
                sheet_range = f"{i.ID}!{cell}"
                values = [[f"{choice}"]]
                body = {'values': values}
                service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=sheet_range,
                valueInputOption='RAW', body=body
                ).execute()
        return redirect("main_view",i.ID)
    else:
        context={'date':date,'instances':instances,'date_range':date_range}
        return render(request,'pointage.html',context)       

def main_view(request,ID):
    i=Employe.objects.get(ID=ID)
    return render(request,'main.html',{'result':i})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("menu_view")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')  # Redirect to home page after successful login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def menu_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    id = request.user.profile.station.id
    
    return render(request, 'menu.html',{'id':id})

# def menu_view(request,ID):
#     if request.user.profile.station.id != ID:
#         return redirect("menu_view",request.user.profile.station.id)
    
#     station = Station.objects.get(id=ID)
#     i=Employe.objects.filter(station=station)
#     print(i)
#     return render(request, 'menu.html',{'id':ID,"i":i})

# def add_chef_station(request):
#     '''Last_Update.objects.all().delete()
#     with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM sqlite_sequence WHERE name='pointage_last_update';")

# # Step 3: Vacuum the database to reclaim storage space
#     with connection.cursor() as cursor:
#             cursor.execute("VACUUM;")'''
#     if request.method == 'POST':
#         form = Chef_StationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             now=datetime.now().date()
#             # Redirect to a success page or homepage
#             return redirect('login')
#     else:
#         form = Chef_StationForm()

#     return render(request, 'add_chef_station.html', {'form': form})



def add_employe(request,ID):
    #the first part is a script that takes information from a sheet and create instances for each employe in that sheet If you want to use it you should modify model so that it won't check for pk
    if request.user.profile.station.id != ID and (request.user.profile.da != 1) :
        return redirect("menu_view")
    if request.user.profile.da == 1:
        if request.method == 'POST':
            form = EmployeFormForDg(request.POST)
            if form.is_valid():
                user=form.save()
                return redirect('table_employe',ID)
        else :
            form = EmployeFormForDg()
    else:
        if request.method == 'POST':
            form = EmployeForm(request.POST)
            if form.is_valid():
                user=form.save()
                user.station=ID
                user.save()
                return redirect('table_employe',ID)
        else:
            form = EmployeForm()
            
    return render (request, 'add_employe.html', {'form': form,'id':ID})

def table_employe(request,ID):
    if request.user.profile.station.id != ID  and (request.user.profile.da != 1) :
        return redirect("menu_view")
    instances=Employe.objects.filter(station=ID)
    return render(request,'table_employe.html',{'id':ID,'instances':instances,'da':request.user.profile.da})

# def employee_search(request,ID):
#     searched=request.GET.get('query','')
#     action=request.GET.get('action')
#     if searched.isdigit():
#         i=Employe.objects.filter(pk=searched , ID_Station_id=ID)
#         i=i.first()
#         if i :
#             if action=='update':
#                 return redirect (update_employe,i.ID)
#             elif action=='sheet_pointage':
#                 return redirect(main_view,i.ID)
#             else:
#                 return redirect(pointage_mois,i.ID)
            
#     message ='ID incorrect '
#     instances=Employe.objects.filter(ID_Station_id=ID)
#     return render(request,'table_employe.html',{'id':ID,'instances':instances,'message':message})
        
def pointage_mois(request,ID):
    if request.user.profile.station.id != ID or (request.user.profile.da == 1) :
        return redirect("menu_view")
    instance=Employe.objects.get(pk=ID)
    return render(request,'mois_form.html',{'instance':instance})

def affichage_mois(request,ID):
    
    i=Employe.objects.get(pk=ID)
    mois=request.POST.get('month')
    credentials = service_account.Credentials.from_service_account_file(
    './petropointage-b1093416d578.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )

    # Create a service using the credentials
    service = build('sheets', 'v4', credentials=credentials)
    source_spreadsheet_id = '15BSWan9Olz9WisDThGlGESdcZPw4GGIvnLyayFIP74I'
    dest_spreadsheet_id = '1mcaMIJmwYZV-TytMXaRlrNQwZHjEp2yCP7W1GSyjaSk'

# Specify the sheet name and range to copy
    ranges = [f"{ID}!AO4:AT4",f'{ID}!B{int(mois) + 13}:AF{int(mois) + 13}']
    values={}
# Iterate through each range and retrieve values
    for range_name in ranges:
        result = service.spreadsheets().values().get(spreadsheetId=source_spreadsheet_id, range=range_name).execute()
        values[range_name]=result.get('values',[])

    values_to_write = {
        'template!AO4:AT4': values[f"{ID}!AO4:AT4"],
        'template!B15:AF15': values[f'{ID}!B{int(mois) + 13}:AF{int(mois) + 13}'],
        "template!AG6:AJ6": [[f'{i.Date_Recrutement}']],
        "template!B8:N8": [[f"{i.Fonction}"]],
        "template!U6:X6": [[f"{i.ID}"]],
        "template!B6:N6": [[f"{i.Nom}"]],  # Update B2:N6 with "Value1"
        "template!B7:N7": [[f"{i.Prenom}"]],  # Update B7:N7 with "Value2"
        "template!AG8:AJ8": [["" if f"{i.Date_Detach}" == 'None' else f"{i.Date_Detach}"]],
        "template!B10:X10": [["" if f"{i.Adresse}" == 'None' else f"{i.Adresse}"]],
        "template!AG9:AM9": [["" if f"{i.Affect_Origin}" == 'None' else f"{i.Affect_Origin}"]],
        "template!AG10:AJ10": [["" if f"{i.Situation_Familliale}" == 'None' else f"{i.Situation_Familliale}"]],
        "template!AG11:AH11": [["" if f"{i.Nbr_Enfants}" == 'None' else f"{i.Nbr_Enfants}"]],
        "template!A15":[[calendar.month_name[int(mois)]]]
        # Add more ranges and values as needed
    }

    for sheet_range, data in values_to_write.items():
        body = {'values': data}
        service.spreadsheets().values().update(
            spreadsheetId=dest_spreadsheet_id, range=sheet_range,
            valueInputOption='RAW', body=body
        ).execute() 
    return render(request,'mois.html',{'ID':i.ID_Station_id})

def update_employe(request,ID):
    employe=Employe.objects.get(ID=ID)
    if request.method == 'POST':
        form=EmployeForm(request.POST,instance=employe)
        if form.is_valid():
            form.save()
            return redirect(table_employe,employe.station.id)
    else:
        form=EmployeForm(instance=employe)
        return render(request,'update_employe.html',{'i':employe,'form':form})
# Create your views here.
