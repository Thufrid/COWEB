from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('companies/', views.company_list, name='company_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.job_apply, name='job_apply'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), # <-- New URL pattern for logging out
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('register/', views.register, name='register'), # New URL for registration
    path('companies/<str:company_name>/', views.company_detail, name='company_detail'),
    path('about/', views.about_us, name='about_us'), # New URL for the About Us page
    path('post-job/', views.post_job, name='post_job'), # New URL for posting a job
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'), # New URL for editing a job
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'), # New URL for deleting a job
]