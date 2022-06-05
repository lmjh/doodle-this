from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import UserAccount, Drawing
from .forms import DefaultAddressForm, NameUpdateForm, DrawingForm


@login_required
def profile(request):
    """ A view to display a user's profile page """

    account = get_object_or_404(UserAccount, user=request.user)
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        default_address_form = DefaultAddressForm(request.POST, instance=account)
        name_update_form = NameUpdateForm(request.POST, instance=user)
        if default_address_form.is_valid() and name_update_form.is_valid():
            name_update_form.save()
            default_address_form.save()
            messages.success(request, 'Profile updated successfully')

    template = 'accounts/profile.html'

    default_address_form = DefaultAddressForm(instance=account)
    name_update_form = NameUpdateForm(instance=user)
    context = {
        'default_address_form': default_address_form,
        'name_update_form': name_update_form,
        'test_account': account,
        'test_user': user,
    }
    return render(request, template, context)


@login_required
def save_drawing(request):
    """
    A view to save a user's drawing to the database
    """

    if request.method == 'POST':
        # find user account and retrieve selected save slot from form
        account = get_object_or_404(UserAccount, user=request.user)
        drawing_number = request.POST['number']

        # query database to find if current user has a drawing with the
        # selected save_slot number
        drawing_instance = Drawing.objects.filter(
            user_account=account,
            number=drawing_number
            ).first()

        # if the user already has a drawing with this save slot, set that
        # drawing object as the instance to be edited
        if drawing_instance:
            form = DrawingForm(request.POST, request.FILES, instance=drawing_instance)
        # otherwise, create a new object
        else:
            form = DrawingForm(request.POST, request.FILES)

        if form.is_valid():
            # set commit=False to allow attaching form data before saving
            drawing = form.save(commit=False)
            # set current user account as user_account foreign key and attach
            # submitted number and image data
            drawing.user_account = account
            drawing.number = drawing_number
            drawing.image = request.FILES['image']

            drawing.save()
            return JsonResponse({'message': 'Drawing successfully submitted.'})
