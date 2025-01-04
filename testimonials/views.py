from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TestimonialForm
from .models import Testimonial
from django.http import HttpResponse


def testimonials_view(request):
    """
    Display a list of all testimonials, ordered by creation date.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the testimonials page with all testimonials.
    """
    testimonials = Testimonial.objects.all().order_by('-created_at')

    context = {
        'testimonials': testimonials,
        'only_success_message': True,
    }
    return render(
        request, 'testimonials/testimonials.html',
        context
    )


@login_required
def add_testimonials_view(request):
    """
    Handle the creation of a new testimonial.

    If the request method is POST and the form is valid, the testimonial
    is saved with the current user as the owner. Otherwise, an empty
    form is displayed.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the testimonials page upon successful
                      submission or re-renders the add testimonial form.
    """
    request.session['IsBagUpdated'] = False

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(
                request,
                'Your testimonial has been added successfully!'
            )
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    context = {
        'form': form,
    }
    return render(
        request,
        'testimonials/add_testimonials.html', context)


@login_required
def delete_testimonials_view(request, testimonial_id):
    """
    Handle the deletion of a testimonial.

    Only the owner of the testimonial or a superuser can delete it.
    If the user lacks permission, they are redirected with a warning message.

    Args:
        request: The HTTP request object.
        testimonial_id (int): The ID of the testimonial to be deleted.

    Returns:
        HttpResponse: Redirects to the testimonials page upon deletion
                      or permission denial.
    """
    request.session['IsBagUpdated'] = False

    testimonial = get_object_or_404(Testimonial, id=testimonial_id)

    if testimonial.user != request.user and not request.user.is_superuser:
        messages.warning("You dont have permission to delete this testimonial")
        return redirect('testimonials')

    testimonial.delete()
    messages.success(request, "Testimonial deleted successfully.")
    return redirect('testimonials')


@login_required
def edit_testimonials_view(request, testimonial_id):
    """
    Handle the editing of an existing testimonial.

    Only the owner of the testimonial or a superuser can edit it. If the
    form submission is valid, the testimonial is updated. Otherwise, the
    form pre-filled with the current data is displayed.

    Args:
        request: The HTTP request object.
        testimonial_id (int): The ID of the testimonial to be edited.

    Returns:
        HttpResponse: Redirects to the testimonials page upon successful update
                      or re-renders the edit testimonial form.
    """

    request.session['IsBagUpdated'] = False

    testimonial = get_object_or_404(Testimonial, id=testimonial_id)

    if testimonial.user != request.user and not request.user.is_superuser:
        messages.warning("You dont have permission to delete this testimonial")
        return redirect('testimonials')
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your testimonial has been updated successfully!"
            )
            return redirect('testimonials')
    else:
        form = TestimonialForm(instance=testimonial)

    context = {
        'form': form,
        'testimonial': testimonial,
    }
    return render(
        request,
        'testimonials/edit_testimonials.html',
        context
    )

# Reset flag for success message in login page
def reset_shopping_bag_flag(request):
    """Reset the 'IsBagUpdated' session flag."""
    request.session['IsBagUpdated'] = False
    return HttpResponse(status=200)  # Empty response with 200 OK status