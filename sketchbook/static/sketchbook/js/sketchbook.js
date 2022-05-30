// initialise Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(
    tooltipTriggerEl))

// find sketchbook element
const canvas = document.querySelector('#sketchbook');

// initialise Atrament canvas
const sketchbook = new Atrament(canvas, {
    width: 1280,
    height: 720,
    color: "#000000",
    weight: 20,
});

/**
 * Uses CSS transforms to scale the contents of the #sketchbook-scaler element
 */
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

/**
 * Takes a colour as a string and uses it to set the Atrament canvas' current colour.
 */
function changeColor(color) {
    // set the received colour as the canvas' current colour
    sketchbook.color = color;
}

/**
 * Takes a clicked preset colour button and finds its background colour. Finding the colours programmatically like this 
 * rather than using a fixed set of options means that the colour presets can be easily changed with CSS root variables 
 * and the correct colour will automatically found and passed to the Atrament canvas.
 */
function findColor(clickedButton) {
        // get the computed style of the received button element
        let compStyle = window.getComputedStyle(clickedButton);
        // assign the background colour to a variable and return it
        let color = compStyle.getPropertyValue('background-color');
        return color;
}

// add an event listener to the element that holds the preset colour buttons
document.getElementById("preset-colour-holder").addEventListener("click", function(e) {
    // if the user clicks on one of the colour buttons inside the holder element
    if (e.target && e.target.matches(".colour-button")) {
        // pass the button to the findColor function to get its background colour as an rbg() formatted string
        let color = findColor(e.target)
        // pass the returned colour to the changeColor function
        changeColor(color);
        }
})

/**
 * Takes a selected tool button node and sets that tool as the Atrament canvas' current mode.
 * Removes the 'active-tool' class from all tool buttons, then adds it to the selected tool butotn. 
 */
function changeTool(selectedTool) {
    sketchbook.mode = selectedTool.value;
    $('.tool-button').removeClass('active-tool');
    selectedTool.classList.add('active-tool');
}

// add an event listener to the element that holds the tool buttons
document.getElementById("tool-holder").addEventListener("click", function(e) {
    // if the user presses enter with one of the tool buttons focused, the button will be the event target
    if (e.target && e.target.matches(".tool-button")) {
        // pass the value of the button to the changeTool function
        changeTool(e.target);
        }
    // if the user clicks on one of the tool buttons, the svg image will be the event target
    else if (e.target && e.target.matches(".tool-icon")) {
        // pass the value of the image's parent button element to the changeTool function
        changeTool(e.target.parentElement);
        }
})