from django.shortcuts import render
from django.urls import reverse

from accounts.forms import DrawingForm
from accounts.models import Drawing


def index(request):
    """ A view to display the sketchbook page """

    # if user is authenticated
    if request.user.is_authenticated:
        # attach the form to save the current user's drawing into the database
        form = DrawingForm()
        account = request.user.useraccount
        # search the database for saved drawings
        # these queries resolve to 'None' if no matching record is found
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

    # create a dictionary to store urls for javascript functions
    # this dictionary will be output to the template as JSON using the
    # json_script filter, then accessed in javascript with JSON.parse()
    urls = {
        'save_drawing': reverse('save_drawing'),
        'get_drawing': reverse('get_drawing'),
    }

    template = 'sketchbook/index.html'

    context = {
        'form': form,
        'saved_drawings': saved_drawings,
        'urls': urls
    }

    return render(request, template, context)
