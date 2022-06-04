from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """ A view to display a user's profile page """

    return render(request, 'accounts/profile.html')
