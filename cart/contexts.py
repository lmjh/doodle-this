from django.conf import settings
from django.shortcuts import get_object_or_404
from prints.models import ProductVariant
from accounts.models import Drawing

def cart_contents(request):
    """
    Handles user shopping cart contents data
    """

    # get cart contents
    cart_contents = request.session.get('cart', [])
    cart_count = len(cart_contents)

    # instantiate variable for total costs
    items_total = 0

    # iterate over items in cart
    for item in cart_contents:
        # find variant
        variant = get_object_or_404(ProductVariant, pk=item['variant_id'])
        # set drawing_image to the url of the saved drawing or 'autosave' if
        # unsaved
        if item['drawing'] == 'autosave':
            item['drawing_image'] = 'autosave'
        else:
            drawing = get_object_or_404(Drawing, user_account=request.user.pk, save_slot=item['drawing'])
            item['drawing_image'] = drawing.image.url
        # add variant price * quantity to items_total
        items_total += variant.price * item['quantity']
        # generate the product variant's name
        item['name'] = f'{variant.product.display_name} - {variant.display_name}'
        # add the image url of the variant, if available
        if variant.image:
            item['image'] = variant.image.image.url
        # use product image if no variant image available
        else:
            item['image'] = variant.product.image.image.url
        item['price'] = variant.price * item['quantity']
        
        

    delivery = settings.STANDARD_DELIVERY_FEE

    grand_total = items_total + delivery

    # pass variables to context
    context = {
        'cart_contents': cart_contents,
        'items_total': items_total,
        'cart_count': cart_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
