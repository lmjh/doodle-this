from django.http import HttpResponse


class StripeWebhookHandler:
    """
    Handles webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def generic_event_handler(self, event):
        """
        Handles all webhook events that don't have another handler
        """
        # return an http response with the type of the event and a 200
        # status code
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def payment_intent_succeeded_handler(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def payment_intent_failed_handler(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
