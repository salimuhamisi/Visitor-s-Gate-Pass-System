from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Entry
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import logout
from.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
import logging
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentUpdateForm
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import ExtractMonth
import json
import calendar
from .models import Group, GroupMember
from django.db.models import Sum



# Create a logger instance
logger = logging.getLogger(__name__)





def home(request):
    return render(request, 'home.html')

@login_required
def get_visitees(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        destination = request.GET.get('destination')
        region = request.GET.get('region')

        # Fetch visitees based on destination and region
        visitees = CustomUser.objects.filter(department=destination, region=region).values_list('username', flat=True)

        # Convert queryset to dictionary for JSON response
        visitees_dict = {visitee: visitee for visitee in visitees}

        return JsonResponse({'visitees': visitees_dict})

    # Return empty response if not an AJAX GET request
    return JsonResponse({})


@login_required
def contact(request):
    return render(request, 'contact.html')

def index(request):
    return render(request, 'index.html')

@login_required
@allowed_users(allowed_usernames=['Receptionis HQ', 'Receptionist KSM', 'hamisi','Receptionist MSA','Receptionist RFT', 'New'])
def eform(request):
    if request.method == 'POST' and 'submit1' in request.POST:
        receptionist = request.user
        id_number = request.POST.get('idNo')
        nature_of_visit = request.POST.get('nature_of_visit')
        fname = request.POST.get('fname')
        destination = request.POST.get('destination')
        plate_number = request.POST.get('plate_number')
        contact = request.POST.get('contact')
        purpose = request.POST.get('purpose')
        visitee = request.POST.get('visitee')
        
        # Do something with the form data, such as saving it to the database
        new_entry = Entry(
            receptionist=receptionist,
            id_number=id_number,
            nature_of_visit=nature_of_visit,
            fname=fname,
            destination=destination,
            plate_number=plate_number,
            contact=contact,
            purpose=purpose,
            visitee=visitee,
            comments=''  # Set the comments field to an empty string by default
        )
        new_entry.save()
        messages.success(request, 'Entry posted Successfully!')
        return redirect('eform')  # Redirect to success page

    if request.method == 'POST' and 'submit2' in request.POST:
        receptionist = request.user
        group_name = request.POST.get('group_name')
        contact = request.POST.get('contact2')
        plate_number2 = request.POST.get('plate_number2')
        purpose = request.POST.get('purpose2')
        department = request.POST.get('department')
        
        group = Group.objects.create(group_name=group_name, contact=contact, plate_number2=plate_number2, purpose=purpose, department=department)
        
        names = request.POST.getlist('name2[]')
        id_numbers = request.POST.getlist('id_number2[]')
        receptionist = receptionist
        
        for name, id_number, receptionist in zip(names, id_numbers, receptionist):
            group_member = GroupMember.objects.create(group=group, name=name, id_number=id_number, receptionist = receptionist)
        
        return redirect('eform')  # Redirect to success page
        

    return render(request, 'eform.html')



@login_required
@allowed_users(allowed_usernames=['hamisi'])
def administrator(request):
    # Retrieve all entries
    entries = Entry.objects.all()

    # Pass the entries and user to the template
    user = request.user
    return render(request, 'administrator.html', {'entries': entries, 'user': user})



@login_required
@allowed_users(allowed_usernames=['visitee1', 'visitee2','visitee3','visitee4', 'visitee5','visitee6','visitee7','visitee8','visitee9','visitee10','salimu'])
def staff_page(request):
    # Get the logged-in user's username
    current_user_username = request.user.username

    # Filter visitors based on the visitee field matching the current user's username
    entries = Entry.objects.filter(visitee=current_user_username)

    user = request.user
    return render(request, 'staff_page.html', {'entries': entries, 'user': user})

@login_required
@allowed_users(allowed_usernames=['Receptionis HQ', 'Receptionist KSM', 'salimu','Receptionist MSA','Receptionist RFT','New'])
def list(request):
    # Retrieve entries for the logged-in receptionist
    entries = Entry.objects.filter(receptionist=request.user)

    # Pass the entries and user to the template
    user = request.user
    return render(request, 'list.html', {'entries': entries, 'user': user})



def signup(request):
    error_message = None
    if request.method == 'POST':
        names = request.POST['names']
        empNo = request.POST['empNo']
        username = request.POST['username']
        password = request.POST['password']
        region = request.POST['region']
        department = request.POST['department']
       

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            error_message = 'Username is already taken'
        else:
            # Create a new user object with the submitted data
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                full_name=names,
                employee_number=empNo,
                region=region,
                department=department
            )

            messages.success(request, 'Account created successfully')

            # Redirect to home page or any other page
            return redirect('signup')
    return render(request, 'signup.html', {'error_message': error_message})
def check_username(request):
    username = request.POST.get('username', None)
    data = {'exists': User.objects.filter(username=username).exists()}
    return JsonResponse(data)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if request.user.username in ['Receptionis HQ', 'Receptionist KSM','Receptionist MSA','Receptionist RFT', 'New']:
                return redirect('eform')
            elif request.user.username == 'hamisi':  # Check username or role
                return redirect('administrator')
            else:
                return redirect("staff_page")
        
        else:
            messages.error(request, "invalid credentials")
            return redirect('login_view')
    return render(request, 'login_view.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logging out


def save_comment(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=entry_id)
        comment = request.POST.get('comment')  # Get the comment from the request

        if comment:  # Ensure comment is not empty
            entry.comments = comment
            entry.save()
            return JsonResponse({'success': True, 'comment': comment})
        else:
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@allowed_users(allowed_usernames=['visitee3', 'visitee2', 'visitee5','visitee6'])
def test(request):
     # Retrieve specific fields from all entries
    entries = Entry.objects.all().values('fname', 'id_number','contact', 'nature_of_visit', 'purpose', 'is_released')

    # Pass the entries and user to the template
    user = request.user
    return render(request, 'test.html', {'entries': entries, 'user': user})


def signedout(request, id):
    entry=Entry.objects.get(id=id)
    entry.is_signedout=True if request.GET.get('is_signedout')=='true' else False
    entry.save()
    
    messages.success(request, 'Updated Successfully!')
    return redirect('staff_page')

def release(request, id):
    entry=Entry.objects.get(id=id)
    entry.is_released=True if request.GET.get('is_released')=='true' else False
    entry.save()
    
    messages.success(request, 'Updated Successfully!')
    return redirect('list')


def dashboard(request):
    # Count entries by month
    entry_counts = (
        Entry.objects.filter(created_at__year=datetime.now().year)  
        .annotate(month=ExtractMonth('created_at'))  
        .values('month')  
        .annotate(count=Count('id'))  
        .order_by('month')  
    )

    # Count group members by month
    group_member_counts = (
        GroupMember.objects.filter(group__created_at__year=datetime.now().year)  
        .annotate(month=ExtractMonth('group__created_at'))  
        .values('month')  
        .annotate(count=Count('id'))  
        .order_by('month')  
    )

    # Combine counts for entries and group members
    total_counts = {}
    for entry_count in entry_counts:
        month = entry_count['month']
        total_counts.setdefault(month, 0)
        total_counts[month] += entry_count['count']
    for member_count in group_member_counts:
        month = member_count['month']
        total_counts.setdefault(month, 0)
        total_counts[month] += member_count['count']

    # Prepare dynamic data for the chart
    chart_data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'datasets': [{
            'label': 'Total Visitors',
            'data': [total_counts.get(month, None) for month in range(1, 13)],
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.1
        }]
    }

    # Calculate true and false counts
    true_count = Entry.objects.filter(status=True).count()
    false_count = Entry.objects.filter(status=False).count()

    # Query to get the top 3 receptionists with the highest number of entries
    top_receptionists = (
        CustomUser.objects.annotate(num_entries=Count('entry')).order_by('-num_entries')[:3]
    )
    top_departments = (
        Entry.objects.values('destination').annotate(num_entries=Count('id')).order_by('-num_entries')[:3]
    )
    
    # Convert chart data to JSON string
    chart_config = json.dumps(chart_data)
    
    return render(request, 'dashboard.html', {'top_receptionists': top_receptionists,'top_departments': top_departments, 'true_count':true_count, 'false_count':false_count, 'chart_config': chart_config})

def grouplist(request):
    # Retrieve all groups
    groups = Group.objects.all()

    return render(request, 'grouplist.html', {'groups': groups})

def agroup(request):
    # Retrieve all groups
    groups = Group.objects.all()

    return render(request, 'agroup.html', {'groups': groups})

def checked(request, id):
    entry=Group.objects.get(id=id)
    entry.is_checked=True if request.GET.get('is_checked')=='true' else False
    entry.save()
    
    return redirect('grouplist')

