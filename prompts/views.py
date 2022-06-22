from django.shortcuts import render
from django.http import JsonResponse


def get_prompt(request):
    """
    A view to generate and return a random drawing prompt
    """
    if request.is_ajax and request.method == "GET":
        prompt = "Test AJAX view"
        return JsonResponse({"prompt": prompt}, status=200)
