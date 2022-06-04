from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import UserAccount
from .forms import DefaultAddressForm, NameUpdateForm


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
