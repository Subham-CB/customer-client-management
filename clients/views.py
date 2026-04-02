from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from django.contrib import messages
import json

from .models import Client
from .forms import ClientForm
from contacts.models import Contact


@require_http_methods(["GET"])
def client_list(request):
    """
    Display list of all clients ordered by name ascending
    """
    clients = Client.objects.all().order_by('name').annotate(
        contact_count=Count('contacts', distinct=True)
    )
    
    context = {
        'clients': clients,
        'total_clients': clients.count()
    }
    
    return render(request, 'clients/client_list.html', context)


@require_http_methods(["GET", "POST"])
def client_create(request):
    """
    Create a new client
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client "{client.name}" created successfully with code: {client.client_code}')
            return redirect('clients:detail', pk=client.pk)
        else:
            # Return form errors as JSON for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = ClientForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Client'
    }
    
    return render(request, 'clients/client_form.html', context)


@require_http_methods(["GET", "POST"])
def client_detail(request, pk):
    """
    Display client details and manage linked contacts
    Includes tabbed interface: General and Contacts
    """
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Client "{client.name}" updated successfully')
            return redirect('clients:detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    # Get linked contacts ordered by surname, name
    linked_contacts = client.contacts.all().order_by('surname', 'name')
    
    context = {
        'client': client,
        'form': form,
        'linked_contacts': linked_contacts,
        'page_title': f'Client: {client.name}'
    }
    
    return render(request, 'clients/client_detail.html', context)


@require_http_methods(["POST"])
def client_link_contact(request, pk):
    """
    AJAX endpoint to link a contact to a client
    """
    client = get_object_or_404(Client, pk=pk)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        data = json.loads(request.body)
        contact_id = data.get('contact_id')
        
        if not contact_id:
            return JsonResponse({'success': False, 'error': 'Contact ID is required'}, status=400)
        
        contact = get_object_or_404(Contact, pk=contact_id)
        
        # Check if already linked
        if client.contacts.filter(id=contact.id).exists():
            return JsonResponse({
                'success': False,
                'error': 'This contact is already linked to this client'
            }, status=400)
        
        # Link contact to client
        client.contacts.add(contact)
        
        return JsonResponse({
            'success': True,
            'message': f'Contact "{contact.get_full_name()}" linked successfully',
            'contact': {
                'id': contact.id,
                'full_name': contact.get_full_name(),
                'email': contact.email
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def client_unlink_contact(request, pk, contact_id):
    """
    AJAX endpoint to unlink a contact from a client
    """
    client = get_object_or_404(Client, pk=pk)
    contact = get_object_or_404(Contact, pk=contact_id)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        # Check if contact is linked
        if not client.contacts.filter(id=contact.id).exists():
            return JsonResponse({
                'success': False,
                'error': 'This contact is not linked to this client'
            }, status=400)
        
        # Unlink contact from client
        client.contacts.remove(contact)
        
        return JsonResponse({
            'success': True,
            'message': f'Contact "{contact.get_full_name()}" unlinked successfully'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def client_delete(request, pk):
    """
    Delete a client
    """
    client = get_object_or_404(Client, pk=pk)
    client_name = client.name
    
    try:
        client.delete()
        messages.success(request, f'Client "{client_name}" deleted successfully')
        return redirect('clients:list')
    except Exception as e:
        messages.error(request, f'Error deleting client: {str(e)}')
        return redirect('clients:detail', pk=pk)


@require_http_methods(["GET"])
def get_available_contacts(request, pk):
    """
    AJAX endpoint to get list of contacts not yet linked to a client
    """
    client = get_object_or_404(Client, pk=pk)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        # Get contacts not linked to this client
        linked_contact_ids = client.contacts.values_list('id', flat=True)
        available_contacts = Contact.objects.exclude(
            id__in=linked_contact_ids
        ).order_by('surname', 'name').values('id', 'surname', 'name', 'email')
        
        contacts_list = [
            {
                'id': contact['id'],
                'full_name': f"({contact['surname']}) {contact['name']}",
                'email': contact['email']
            }
            for contact in available_contacts
        ]
        
        return JsonResponse({
            'success': True,
            'contacts': contacts_list
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500) 