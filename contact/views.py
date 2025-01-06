from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactEnquiryForm
from django.core.mail import send_mail
from django.conf import settings

import logging 
logger = logging.getLogger(__name__)

def contact_enquiry_view(request):
    """
    This view allows the user to submit
    an enquiry through the contact form.
    If the form is valid, it saves the enquiry
    and displays a success message.
    If the form is not valid, it shows an error
    message and prompts the user to try again.
    """
    # Clear the flag at the start of the
    # view to prevent unwanted flag persistence
    request.session['IsBagUpdated'] = False

    if request.method == 'POST':
        form = ContactEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()

            #send_contact_confirmation_email(enquiry)

            messages.success(request, 'Thank you for contacting us!'
                             'We have received your Enquiry.')
            return redirect('contact')
        else:
            logger.error(f"Form errors: {form.errors}")  # Log form errors
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = ContactEnquiryForm()

    context = {
        'form': form,
        'IsBagUpdated': False
    }

    return render(request,
                  'contact/contact.html', context)
