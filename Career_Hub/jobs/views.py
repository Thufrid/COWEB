from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout  # <-- Import the Django logout function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # Import Django's user creation form
from .models import Job
from .forms import JobForm

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')
    context = {
        'jobs': jobs
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id): # New view function
    job = get_object_or_404(Job, pk=job_id) # Fetches the job or returns a 404 error
    context = {
        'job': job
    }
    return render(request, 'jobs/job_detail.html', context)

def job_apply(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        # Here you would process the form data
        # For a full implementation, you would save this data to a new 'Application' model
        # and handle the uploaded resume file.
        
        name = request.POST.get('applicant_name')
        email = request.POST.get('applicant_email')
        # You'd also handle the resume upload (request.FILES.get('resume'))
        
        # After successful submission, redirect to a confirmation page or back to the job details page
        return redirect('job_detail', job_id=job.id)
        # return HttpResponse("Application submitted successfully!")
    
    # For a GET request, render the form
    context = {
        'job': job
    }
    return render(request, 'jobs/job_apply.html', context)


# ... other views (job_list, job_detail, job_apply)

@login_required
def dashboard(request):
    user = request.user
    # For a full implementation, you would query for the user's applications
    # or saved jobs here.
    context = {
        'user': user,
        # 'applied_jobs': applied_jobs,
        # 'saved_jobs': saved_jobs
    }
    return render(request, 'dashboard/dashboard.html', context)

def logout_view(request):
    auth_logout(request)
    return redirect('job_list') # Redirect to the homepage after logging out

@login_required
def employer_dashboard(request):
    # This assumes the user is an employer and has a way to post jobs.
    # In a real app, you would have a more complex user model.
    employer_jobs = Job.objects.filter(company=request.user.username)  # Filter jobs by the logged-in user's name
    context = {
        'employer_jobs': employer_jobs,
    }
    return render(request, 'employer/employer_dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You can log the user in here after registration if you want
            # login(request, user)
            return redirect('login') # Redirect to the login page
    else:
        form = UserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)

def company_detail(request, company_name):
    # Retrieve all jobs from the specified company
    company_jobs = Job.objects.filter(company=company_name).order_by('-posted_date')

    # If no jobs are found for this company, return a 404 error
    if not company_jobs:
        return HttpResponse('<h1>Company Not Found</h1><p>The company you are looking for does not exist or has no posted jobs.</p>', status=404)

    context = {
        'company_name': company_name,
        'company_jobs': company_jobs
    }
    return render(request, 'jobs/company_detail.html', context)



def company_list(request):
    companies = Job.objects.values_list('company', flat=True).distinct()
    context = {
        'companies': companies
    }
    return render(request, 'jobs/company_list.html', context)

def about_us(request):
    return render(request, 'jobs/about_us.html')

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.company = request.user.username
            new_job.save()
            return redirect('employer_dashboard') # Redirect to dashboard on success
    else:
        form = JobForm()
        
    context = {
        'form': form,
    }
    return render(request, 'jobs/post_job.html', context)

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security check: Ensure the logged-in user is the owner of the job
    if job.company != request.user.username:
        return HttpResponseForbidden("You are not authorized to edit this job.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'jobs/edit_job.html', context)

# ... import statements

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Security check: Ensure the logged-in user is the owner of the job
    if job.company != request.user.username:
        return HttpResponseForbidden("You are not authorized to delete this job.")

    if request.method == 'POST':
        job.delete()
        return redirect('employer_dashboard')

    context = {
        'job': job,
    }
    return render(request, 'jobs/delete_job.html', context)