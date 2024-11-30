import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import Volunteer, Contact, Cause,Donate, Person, work, Event, EventImage
from django.core.paginator import Paginator
from .forms import EventForm, PersonForm, CauseForm, WorkForm



def index(request):
    # Limit causes to 3 for the index page
    causes = Cause.objects.all()[:3]  # Fetch the first 3 causes
    return render(request, 'index.html', {'causes': causes})

def about(request):
    works = work.objects.all()
    return render(request, 'about.html', {'works': works})

def gallery(request):
    persons = Person.objects.all()
    return render(request, 'gallery.html', {'persons': persons})

def person_gallery(request):
    persons = Person.objects.all().order_by('-date_registered')
    return render(request, 'gallery.html', {'persons': persons})

def submit_valunteer(request):
    if request.method =="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        gender=request.POST['gender']
        dob=request.POST['dob']
        subject=request.POST['subject']
        message=request.POST.get('message')

        volunteer=Volunteer.objects.create(name=name,email=email,phone=phone, gender=gender, dob=dob, subject=subject,message=message)
        volunteer.save()

        web3forms_url = "https://api.web3forms.com/submit"
        api_key = "60e389c0-86f5-4080-9bbf-6660da85eabb"  # Replace with your actual Web3Forms API key

        data = {
            "access_key": api_key,
            "name": f"{name}",
            "email": email,
            "phone": phone,
            "gender:": gender,
            "Date of Birth": dob, 
            "message": message,
            "subject": f"{name} wants to contact regarding Voluteer for Pragati-foundation  ",
            "from_name": "Voluteer_Pragati-Foundation",
            "to_email": "admin@example.com",  # Admin email address
        }

        response = requests.post(web3forms_url, data=data)

        if response.status_code == 200:
            messages.success(request, 'Form submitted successfully! Our Team will contact you.')
        else:
            messages.error(request, 'There was an error submitting the form. Please try again later.')

        return redirect('/')
    
    return render(request, '/')  # Adjust to the correct template


def contact(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        message = request.POST.get('message')

        contact = Contact.objects.create(
            name=f"{f_name} {l_name}",
            email=email,
            message=message
        )
        contact.save()
        
        web3forms_url = "https://api.web3forms.com/submit"
        api_key = "60e389c0-86f5-4080-9bbf-6660da85eabb"  # Replace with your actual Web3Forms API key

        data = {
            "access_key": api_key,
            "name": f"{f_name} {l_name}",
            "email": email,
            "message": message,
            "subject": f"{f_name} {l_name} wants to contact regarding Pragati-foundation ",
            "from_name": "Pragati-Foundation",
            "to_email": "admin@example.com",  # Admin email address
        }

        response = requests.post(web3forms_url, data=data)
        
        # Add success message
        if response.status_code == 200:
            messages.success(request, 'Form submitted successfully! Our Team will contact you.')
        else:
            messages.error(request, 'There was an error submitting the form. Please try again later.')

        return redirect('/')  # Redirect to the home page to show the message

    return render(request, 'contactus.html')  # Adjust to the correct template



def donate(request,id):
    if request.method =="POST":
        name=request.POST['name']
        email=request.POST['email']
        amount=request.POST.get('amount')

        cause=Cause.objects.get(id=id)
        cause.raised=cause.raised+float(amount)
        cause.goal=cause.goal-float(amount)
        cause.save()
        donation=Donate.objects.create(name=name,email=email,amount=float(amount))
        donation.save()
        return redirect('/')
    else:
        cause=Cause.objects.get(id=id)
        return render(request,'donate.html',{"cause":cause})
    
def contactus(request):
    return render(request, 'contactus.html')

def donates(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        amount = request.POST.get('amount')
        photo = request.FILES.get('photo')
        cause_id = request.POST.get('cause')  # Get selected cause

        if not cause_id:
            return HttpResponse("Cause is required.", status=400)

        try:
            cause = Cause.objects.get(id=cause_id)  # Fetch the selected cause
        except Cause.DoesNotExist:
            return HttpResponse("Invalid Cause.", status=404)

        # Update the cause's raised and goal amounts
        cause.raised += float(amount)
        cause.goal -= float(amount)
        cause.save()

        # Create the donation entry
        Donate.objects.create(name=name, email=email, amount=float(amount), photo=photo, cause=cause)

        return redirect('donates')

    # Fetch all causes and donations to display
    causes = Cause.objects.all()
    donations = Donate.objects.all().order_by('-id')  # Order by latest first
    return render(request, 'donates.html', {"causes": causes, "donations": donations})


def history(request):
    events = Event.objects.prefetch_related('images').order_by('-date')  # Sort by latest date first
    paginator = Paginator(events, 4)  # 4 events per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'history.html', {'page_obj': page_obj})
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('add_event')  # Redirect to add_event page after login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})  # Correct error key
    return render(request, 'login.html')
    

@login_required
def add_event(request):
    success_message = None  # Initialize success message as None
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        
        if event_form.is_valid():
            event = event_form.save()  # Save the event

            # Handle image files
            for image in request.FILES.getlist('image'):  # Access multiple uploaded images
                EventImage.objects.create(event=event, image=image)

            success_message = "Data is added successfully."  # Set the success message
            event_form = EventForm()  # Re-initialize the form to be blank after submission

    else:
        event_form = EventForm()

    return render(request, 'add_event.html', {'event_form': event_form, 'success_message': success_message})

@login_required
def add_cause(request):
    success_message = None
    if request.method == 'POST':
        cause_form = CauseForm(request.POST, request.FILES)  # Include request.FILES to handle image uploads
        if cause_form.is_valid():
            cause_form.save()
            success_message = "Cause added successfully!"
            cause_form = CauseForm()  # Reset the form
    else:
        cause_form = CauseForm()

    return render(request, 'add_cause.html', {'cause_form': cause_form, 'success_message': success_message})


# views.py

def add_person(request):
    if request.method == "POST":
        person_form = PersonForm(request.POST, request.FILES)
        if person_form.is_valid():
            person = person_form.save()  # Save the form data to the database

            # Web3 Forms API endpoint and your API key
            url = "https://api.web3forms.com/submit"
            headers = {"Content-Type": "application/json"}

            # Prepare data for Web3 Forms API
            data = {
                "access_key": "60e389c0-86f5-4080-9bbf-6660da85eabb",  # Replace with your actual access key
                "subject": "New Beneficiary Registered",
                "from_name": "Your Pragati Foundation",
                "from_email": "your_email@example.com",
                "reply_to": person.email,
                "message": f"""
                    A new beneficiary has registered with the following details:

                    Name: {person.name}
                    Phone: {person.phone}
                    Email: {person.email}
                    Address: {person.address}
                    Disability Type: {person.disability_type}
                    Disability Percentage: {person.dis_percentage}
                    UDID Number: {person.udid_no}
                    Aadhaar Number: {person.aadhaar_no}
                    Age: {person.age}
                    Gender: {person.gender}
                    Dependent: {person.dependent}
                    Occupation: {person.occupation}
                    Salary: {person.salary}
                    IT Return: {person.it_return}
                """
            }

            # Send data to Web3 Forms
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                # Success response handling
                return render(request, 'add_person.html', {
                    'person_form': PersonForm(),
                    'success_message': "Person added successfully. Details have been sent to the admin."
                })
            else:
                # Error response handling
                return render(request, 'add_person.html', {
                    'person_form': PersonForm(),
                    'error_message': "There was an error sending the details to the admin. Please try again."
                })

        else:
            # Form is not valid, render form with error messages
            return render(request, 'add_person.html', {'person_form': person_form})

    else:
        person_form = PersonForm()
    
    return render(request, 'add_person.html', {'person_form': person_form})

@login_required
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'add_work.html', {'form': WorkForm(), 'success_message': 'Work added successfully!'})
    else:
        form = WorkForm()

    return render(request, 'add_work.html', {'form': form})
