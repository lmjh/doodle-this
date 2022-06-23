from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import UserAccount, Drawing
from .forms import DefaultAddressForm, NameUpdateForm, DrawingForm


@login_required
def profile(request):
    """A view to display a user's profile page"""

    # find user's UserAccount and User entries 
    account = get_object_or_404(UserAccount, user=request.user)
    user = get_object_or_404(User, username=request.user)

    if request.method == "POST":
        # update the user's default address and names if valid forms are posted
        default_address_form = DefaultAddressForm(
            request.POST, instance=account
        )
        name_update_form = NameUpdateForm(request.POST, instance=user)
        if default_address_form.is_valid() and name_update_form.is_valid():
            name_update_form.save()
            default_address_form.save()
            messages.success(request, "Profile updated successfully")

    template = "accounts/profile.html"

    # instantiate address and name update forms
    default_address_form = DefaultAddressForm(instance=account)
    name_update_form = NameUpdateForm(instance=user)

    # gather all of the user's orders
    orders = account.orders.all()

    # create an array to store user's saved drawings
    saved_drawings = []
    # and a dict to store drawing titles
    titles = {}

    # search the database for saved drawings and add to array
    for save_slot in range(1, 4):
        # this query resolves to 'None' if no matching record is found
        drawing = Drawing.objects.filter(
            user_account=account, save_slot=save_slot
        ).first()
        saved_drawings.append(drawing)

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

    context = {
        "default_address_form": default_address_form,
        "name_update_form": name_update_form,
        "test_account": account,
        "test_user": user,
        "orders": orders,
        "saved_drawings": saved_drawings,
        "titles": titles,
    }
    return render(request, template, context)


@login_required
def save_drawing(request):
    """
    A view to save a user's drawing to the database
    """
    if request.is_ajax and request.method == "POST":
        form = DrawingForm(request.POST, request.FILES)

        if form.is_valid():
            # set commit=False to allow attaching form data before saving
            drawing = form.save(commit=False)

            # find user account
            account = get_object_or_404(UserAccount, user=request.user)

            # set current user account as user_account foreign key
            drawing.user_account = account

            # query database to find if current user has a drawing saved in the
            # selected save_slot.
            # this query returns 'None' if no record is found:
            # (https://stackoverflow.com/a/29455777)
            save_slot_exists = Drawing.objects.filter(
                user_account=account, save_slot=drawing.save_slot
            ).first()

            # if the user already has a drawing in this save slot
            if save_slot_exists:
                # overwrite the save_slot
                drawing.id = save_slot_exists.id

            # save drawing
            drawing.save()

            # pass url of saved drawing back to javascript function
            response_url = drawing.image.url
            return JsonResponse({"url": response_url}, status=200)

        else:
            return JsonResponse({"error": "Form not valid."}, status=400)


@login_required
def get_drawing(request):
    """
    A view to retrieve a user's drawing from the database.
    """
    if request.is_ajax and request.method == "GET":
        # find the user's account and the requested save slot
        user_account = get_object_or_404(UserAccount, user=request.user)
        save_slot = request.GET.get("save_slot", None)

        # find the requested drawing or set to 'None'
        drawing = Drawing.objects.filter(
            user_account=user_account, save_slot=save_slot
        ).first()

        # if the drawing is found, return its url in a JsonResponse
        if drawing:
            response_url = drawing.image.url
            return JsonResponse({"url": response_url}, status=200)

        # if the drawing is not found, return a 404 error code
        return JsonResponse({}, status=404)
