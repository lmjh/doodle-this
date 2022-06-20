// retrieve Stripe public key and client secret from page
const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);

// initialise stripe with key and instantiate stripe elements
const stripe = Stripe(stripePublicKey)
const elements = stripe.elements();

// create style variable to add styles to card
const style = {
    base: {
        iconColor: '#ebebeb',
        color: '#ebebeb',
        backgroundColor: '#202020',
        fontFamily: '"Quicksand", Arial, Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#ebebeb'
        }
    },
    invalid: {
        color: '#ff3a3a',
        iconColor: '#ff3a3a'
    }
};

// instantiate card with style variable and mount to checkout page element
const card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// add event listener to check for card errors and display them
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <div class='card-errors'>
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        </div>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// assign payment form to a const
const form = document.getElementById('payment-form')

// add an event listener to the payment form to submit payments
form.addEventListener('submit', function (ev) {
    // prevent submit button default actions and disable form and button
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#submit-order').attr('disabled', true);
    // show the loading overlay
    $('#loading-overlay').fadeToggle(100);

    // execute stripe confirm card payment functions
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            // fill billing details with form data
            billing_details: {
                // concatenate first and last names
                name: $.trim(form.first_name.value) + " " + $.trim(form.last_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email_address.value),
                address: {
                    line1: $.trim(form.address_1.value),
                    line2: $.trim(form.address_2.value),
                    city: $.trim(form.town.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postalCode: $.trim(form.postcode.value)
                }
            }
        }
    }).then(function (result) {
        // if error returned, display it
        if (result.error) {
            let errorDiv = document.getElementById('card-errors');
            let errorHtml = `
            <div class='card-errors'>
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            </div>
            `;
            $(errorDiv).html(errorHtml);
            // re-enable card and submit elements to allow user to fix error
            card.update({
                'disabled': false
            });
            $('#submit-order').attr('disabled', false);
            //  hide loading overlay
            $('#loading-overlay').fadeToggle(100);
        } else {
            // if payment succeeds, submit the form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});