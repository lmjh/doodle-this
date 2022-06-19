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
const card = elements.create('card', {style: style});
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