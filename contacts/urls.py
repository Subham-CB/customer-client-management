from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # Contact list view
    path('', views.contact_list, name='list'),
    
    # Create new contact
    path('create/', views.contact_create, name='create'),
    
    # Contact detail (edit)
    path('<int:pk>/', views.contact_detail, name='detail'),
    
    # Delete contact
    path('<int:pk>/delete/', views.contact_delete, name='delete'),
    
    # AJAX endpoints for client linking
    path('<int:pk>/link-client/', views.contact_link_client, name='link_client'),
    path('<int:pk>/unlink-client/<int:client_id>/', views.contact_unlink_client, name='unlink_client'),
    
    # AJAX endpoint to get available clients
    path('<int:pk>/available-clients/', views.get_available_clients, name='available_clients'),
]