from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to display the sketchbook page """

    return render(request, 'sketchbook/index.html')
