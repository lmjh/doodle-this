// INITIALISE ELEMENTS AND STYLES

// initialise Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(
    tooltipTriggerEl));

// find sketchbook element
const canvas = document.querySelector('#sketchbook');
// initialise Atrament canvas
const sketchbook = new Atrament(canvas, {
    width: 1280,
    height: 720,
    // set colour to the current value of the coloris color picker 
    color: document.getElementById('coloris-picker').value,
    // set weight to the current value of the stroke weight slider 
    weight: parseInt(document.getElementById('stroke-weight').value),
});

// initialise Coloris colour picker
Coloris({
    el: '.coloris',
    theme: 'polaroid',
    themeMode: 'dark',
    alpha: false,
    format: 'rgb',
    defaultColor: "#000000" ,
});

// set the cursor element's colour to the value of the Coloris picker
$('#cursor').css('background-color', document.getElementById('coloris-picker').value);

// call resizeCanvas function
resizeCanvas();

// DECLARE FUNCTIONS

/**
 * Uses CSS transforms to scale the contents of the #sketchbook-scaler element
 */
function resizeCanvas() {
    // find sketchbook-scaler and scaler-holder divs
    let scaler = document.getElementById('sketchbook-scaler');
    let holder = document.getElementById('scaler-holder');

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
    $('#scaler-holder').height(scaler.getBoundingClientRect().height);
}

/**
 * Takes a colour as a string and uses it to set the Atrament canvas' current colour
 */
function changeAtramentColor(color) {
    sketchbook.color = color;
}

/**
 * Takes a colour as a string and uses it to set the Coloris picker's value and displayed colour
 */
function changeColorisColor(color) {
    $('.coloris').val(color);
    $('.clr-field').css('color', color);
}

/**
 * Takes a colour as a string and uses it to set the cursor preview colour
 */
function changeCursorColor(color) {
    $('#cursor').css('background-color', color);
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

/**
 * Takes a selected tool button node and sets that tool as the Atrament canvas' current mode.
 * Removes the 'active-tool' class from all tool buttons, then adds it to the selected tool butotn. 
 */
function changeTool(selectedTool) {
    sketchbook.mode = selectedTool.value;
    $('.tool-button').removeClass('active-tool');
    selectedTool.classList.add('active-tool');
}

/**
 * Changes the stroke weight of the Atrament canvas to the value of the triggering event's target and updates the cursor
 * preview to match.
 */
function changeWeight(e) {
    // convert the event taget's value to an int
    let weight = parseInt(e.target.value);
    // pass to Atrament canvas
    sketchbook.weight = weight;
    // set cursor preview to same width and height as canvas tool
    $('#cursor').css('width', weight).css('height', weight);
}

// ADD EVENT LISTENERS

// add an event listener to set the Atrament canvas colour and cursor preview colour when a colour is selected with the 
// Coloris picker
document.addEventListener('coloris:pick', event => {
    let color = event.detail.color;
    changeAtramentColor(color);
    changeCursorColor(color);
});

// add event listener to call resizeCanvas function on window resize.
// to prevent multiple successive resize operations, add a short delay so that resize function is not called until the 
// user has stopped resizing the window (based on this answer from SO: https://stackoverflow.com/a/15205745)
let resizeTimer = null;
window.addEventListener("resize", function() {
    if (resizeTimer != null) window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function() {
        resizeCanvas();
    }, 200);
});

// add an event listener to the element that holds the preset colour buttons
document.getElementById("preset-colour-holder").addEventListener("click", function(e) {
    // if the user clicks on one of the colour buttons inside the holder element
    if (e.target && e.target.matches(".colour-button")) {
        // pass the button to the findColor function to get its background colour as an rgb() formatted string
        let color = findColor(e.target);
        // pass the returned colour to the changeColor function
        changeAtramentColor(color);
        changeColorisColor(color);
        changeCursorColor(color);
    }
});

// add an event listener for the custom event 'colorpicked', triggered when the colour picker tool is used
sketchbook.addEventListener('colorpicked', function(e) {
    // use the colour returned by the colorpicked event to update the Coloris plugin and cursor preview 
    changeColorisColor(e.color);
    changeCursorColor(e.color);
});

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
});

// add event listener to change Atrament canvas stroke weight when slider is changed
document.getElementById('stroke-weight').addEventListener('change', changeWeight);

// add event listener to clear Atrament canvas when clear confirmation button is clicked
document.getElementById('clear-sketchbook').addEventListener('click', function() {
    sketchbook.clear();
});