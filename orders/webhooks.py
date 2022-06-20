from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listens for webhooks from Stripe
    """
    # get secrets from settings
    wh_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get webhook data and verify signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, wh_secret
        )
    except ValueError as e:
        # handle invalid payload error
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # handle invalid signature error
        return HttpResponse(status=400)
    except Exception as e:
        # handle other errors
        return HttpResponse(content=e, status=400)

    # handle the event
    print(f'Handled event type {event["type"]}')

    return HttpResponse(status=200)
