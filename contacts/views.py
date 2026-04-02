from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.contrib import messages
import json

from .models import Contact
from .forms import ContactForm
from clients.models import Client


@require_http_methods(["GET"])
def contact_list(request):
    """
    Display list of all contacts ordered by surname, name ascending
    """
    contacts = Contact.objects.all().order_by('surname', 'name').annotate(
        client_count=Count('clients', distinct=True)
    )
    
    context = {
        'contacts': contacts,
        'total_contacts': contacts.count()
    }
    
    return render(request, 'contacts/contact_list.html', context)


@require_http_methods(["GET", "POST"])
def contact_create(request):
    """
    Create a new contact
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'Contact "{contact.get_full_name}" created successfully')
            return redirect('contacts:detail', pk=contact.pk)
        else:
            # Return form errors as JSON for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Contact'
    }
    
    return render(request, 'contacts/contact_form.html', context)


@require_http_methods(["GET", "POST"])
def contact_detail(request, pk):
    """
    Display contact details and manage linked clients
    Includes tabbed interface: General and Clients
    """
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Contact "{contact.get_full_name}" updated successfully')
            return redirect('contacts:detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    
    # Get linked clients ordered by name
    linked_clients = contact.clients.all().order_by('name')
    
    context = {
        'contact': contact,
        'form': form,
        'linked_clients': linked_clients,
        'page_title': f'Contact: {contact.get_full_name}'
    }
    
    return render(request, 'contacts/contact_detail.html', context)


@require_http_methods(["POST"])
def contact_link_client(request, pk):
    """
    AJAX endpoint to link a client to a contact
    """
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
        
        if not client_id:
            return JsonResponse({'success': False, 'error': 'Client ID is required'}, status=400)
        
        client = get_object_or_404(Client, pk=client_id)
        
        # Check if already linked
        if contact.clients.filter(id=client.id).exists():
            return JsonResponse({
                'success': False,
                'error': 'This client is already linked to this contact'
            }, status=400)
        
        # Link client to contact
        contact.clients.add(client)
        
        return JsonResponse({
            'success': True,
            'message': f'Client "{client.name}" linked successfully',
            'client': {
                'id': client.id,
                'name': client.name,
                'client_code': client.client_code
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def contact_unlink_client(request, pk, client_id):
    """
    AJAX endpoint to unlink a client from a contact
    """
    contact = get_object_or_404(Contact, pk=pk)
    client = get_object_or_404(Client, pk=client_id)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        # Check if client is linked
        if not contact.clients.filter(id=client.id).exists():
            return JsonResponse({
                'success': False,
                'error': 'This client is not linked to this contact'
            }, status=400)
        
        # Unlink client from contact
        contact.clients.remove(client)
        
        return JsonResponse({
            'success': True,
            'message': f'Client "{client.name}" unlinked successfully'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
def contact_delete(request, pk):
    """
    Delete a contact
    """
    contact = get_object_or_404(Contact, pk=pk)
    contact_name = contact.get_full_name
    
    try:
        contact.delete()
        messages.success(request, f'Contact "{contact_name}" deleted successfully')
        return redirect('contacts:list')
    except Exception as e:
        messages.error(request, f'Error deleting contact: {str(e)}')
        return redirect('contacts:detail', pk=pk)


@require_http_methods(["GET"])
def get_available_clients(request, pk):
    """
    AJAX endpoint to get list of clients not yet linked to a contact
    """
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    
    try:
        # Get clients not linked to this contact
        linked_client_ids = contact.clients.values_list('id', flat=True)
        available_clients = Client.objects.exclude(
            id__in=linked_client_ids
        ).order_by('name').values('id', 'name', 'client_code')
        
        clients_list = [
            {
                'id': client['id'],
                'name': client['name'],
                'client_code': client['client_code']
            }
            for client in available_clients
        ]
        
        return JsonResponse({
            'success': True,
            'clients': clients_list
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)