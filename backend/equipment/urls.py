from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('check-auth/', views.check_auth, name='check_auth'),
    
    # Dataset operations
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/', views.get_summary, name='get_summary'),
    path('history/', views.get_history, name='get_history'),
    path('dataset/<int:dataset_id>/', views.get_dataset, name='get_dataset'),
    
    # Reports
    path('report/', views.generate_report, name='generate_report_latest'),
    path('report/<int:dataset_id>/', views.generate_report, name='generate_report'),
]
