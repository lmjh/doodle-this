from django.shortcuts import render

from accounts.forms import DrawingForm
from accounts.models import Drawing


def index(request):
    """ A view to display the sketchbook page """

    # if user is authenticated
    if request.user.is_authenticated:
        # attach the form to save the current user's drawing into the database
        form = DrawingForm()
        account = request.user.useraccount
        saved_drawing_1 = Drawing.objects.filter(
            user_account=account,
            save_slot=1
            ).first()
        saved_drawing_2 = Drawing.objects.filter(
            user_account=account,
            save_slot=2
            ).first()
        saved_drawing_3 = Drawing.objects.filter(
            user_account=account,
            save_slot=3
            ).first()
        saved_drawings = [
            saved_drawing_1, saved_drawing_2, saved_drawing_3
        ]
    else:
        form = None
        saved_drawings = None

    context = {
        'form': form,
        'saved_drawings': saved_drawings,
    }
    return render(request, 'sketchbook/index.html', context)
