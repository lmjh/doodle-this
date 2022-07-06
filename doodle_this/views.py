from django.shortcuts import render


def handler404(request, exception):
    """
    Error handler for 404 - Page Not Found
    """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """
    Error handler for 500 - Internal Server Error
    """
    return render(request, "errors/500.html", status=500)
