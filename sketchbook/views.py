from django.shortcuts import render

from accounts.forms import DrawingForm


def index(request):
    """ A view to display the sketchbook page """

    # if user is authenticated
    if request.user.is_authenticated:
        # attach the form to save the current user's drawing into the database
        form = DrawingForm()
    else:
        form = None

    context = {'form': form}
    return render(request, 'sketchbook/index.html', context)
