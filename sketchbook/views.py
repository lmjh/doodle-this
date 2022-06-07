from django.shortcuts import render
from django.urls import reverse

from accounts.forms import DrawingForm
from accounts.models import Drawing


def index(request):
    """ A view to display the sketchbook page """

    # create a dictionary to store urls for javascript functions
    # this dictionary will be output to the template as JSON using the
    # json_script filter, then accessed in javascript with JSON.parse()
    urls = {
        'save_drawing': reverse('save_drawing'),
        'get_drawing': reverse('get_drawing'),
    }

    # also create a dictionary to store drawing titles
    titles = {}

    form = None
    saved_drawings = None

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

        # iterate through saved_drawings array
        for count, drawing in enumerate(saved_drawings):
            # set title to the title of the drawing if one is present, or an
            # empty string if no drawing found or drawing doesn't have a title
            if drawing:
                title = drawing.title or ""
            else:
                title = ""
            # save the titles to the titles dictionary
            titles[f"title_{count + 1}"] = title

    template = 'sketchbook/index.html'

    context = {
        'form': form,
        'saved_drawings': saved_drawings,
        'urls': urls,
        'titles': titles
    }

    return render(request, template, context)
