from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactEnquiryForm
from django.core.mail import send_mail
from django.conf import settings


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

            send_contact_confirmation_email(enquiry)

            messages.success(request, 'Thank you for contacting us!'
                             'We have received your Enquiry.'
                             'A confirmation email has'
                             'been sent to your mail id.')
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with '
                           'your submission. Please try again.')
    else:
        form = ContactEnquiryForm()

    context = {
        'form': form,
        'IsBagUpdated': False
    }

    return render(request,
                  'contact/contact.html', context)


def send_contact_confirmation_email(enquiry):
    """
    Send a confirmation email to the
    user after a successful enquiry.
    """
    send_mail(
        subject=f"Thank You for Your Enquiry: {enquiry.subject}",
        message=(
            f"Dear {enquiry.full_name},\n\n"
            "Thank you for reaching out to us regarding:"
                f"{enquiry.get_enquiry_type_display()}.\n"
            f"We have received your enquiry and will "
                "get back to you as soon as possible.\n\n"
            f"Subject: {enquiry.subject}\n"
            f"Message: {enquiry.message}\n\n"
            f"Best regards,\nPosters4U"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[enquiry.email],
        fail_silently=False,
    )