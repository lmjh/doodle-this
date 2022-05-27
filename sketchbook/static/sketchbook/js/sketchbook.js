// Initialise Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(
    tooltipTriggerEl))

// Find sketchbook element
const canvas = document.querySelector('#sketchbook');

// Initialise Atrament canvas
const sketchpad = new Atrament(canvas, {
    width: 1280,
    height: 720,
    color: "#000000",
    weight: 20,
});

// use CSS transform to scale the contents of the #sketchbook-scaler element
function resizeCanvas() {
    // find sketchbook-scaler and scaler-holder divs
    let scaler = document.getElementById('sketchbook-scaler')
    let holder = document.getElementById('scaler-holder')

    // assign sketchbook-holder width to a variable
    let holderWidth = holder.getBoundingClientRect().width;

    // divide holderWidth by the fixed width of the sketchbook to find the scaling ratio
    // limit to 3 decimal places
    let scale = (holderWidth / 1340).toFixed(3);

    // set the scaler to transform from the top left
    scaler.style.transformOrigin = '0 0';
    // scale the contents of the scaler by the calculated ratio
    scaler.style.transform = 'scale(' + scale + ')';

    // set scaler-holder height to height of scaler to fix layout bug
    $('#scaler-holder').height(scaler.getBoundingClientRect().height)
};

// call resizeCanvas function
resizeCanvas();

// add event listener to call resizeCanvas function on window resize
// to prevent multiple successive resize operations, add a short delay so that resize function is not called until the 
// user has stopped resizing the window (based on this answer from SO: https://stackoverflow.com/a/15205745)
let resizeTimer = null

addEventListener("resize", function() {
    if (resizeTimer != null) window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function() {
        resizeCanvas();
    }, 200);
});