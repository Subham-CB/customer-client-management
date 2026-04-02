from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Client list view
    path('', views.client_list, name='list'),
    
    # Create new client
    path('create/', views.client_create, name='create'),
    
    # Client detail (edit)
    path('<int:pk>/', views.client_detail, name='detail'),
    
    # Delete client
    path('<int:pk>/delete/', views.client_delete, name='delete'),
    
    # AJAX endpoints for contact linking
    path('<int:pk>/link-contact/', views.client_link_contact, name='link_contact'),
    path('<int:pk>/unlink-contact/<int:contact_id>/', views.client_unlink_contact, name='unlink_contact'),
    
    # AJAX endpoint to get available contacts
    path('<int:pk>/available-contacts/', views.get_available_contacts, name='available_contacts'),
]