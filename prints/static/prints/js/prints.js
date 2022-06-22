// INITIALISE ELEMENTS AND STYLES

// retrieve user image URLs from JSON, if present
const jsonData = JSON.parse(document.getElementById('jsonData').textContent);
// get document elements
const drawingOverlay = document.getElementById('drawing-overlay');
const selectVariant = document.getElementById('variant');
const selectDrawing = document.getElementById('drawing');
const productImage = document.getElementById('product-image');
const price = document.getElementById('price');
const addToCart = document.getElementById('add-to-cart');

$( document ).ready(function() {
    // if currently selected variant has an image
    if (jsonData.variantUrls[selectVariant.value]) {
        // set that image as the displayed product image
        setProductImage(jsonData.variantUrls[selectVariant.value]);
        // and load that image's overlay position data
        positionOverlay(jsonData.overlay[selectVariant.value]);
        
    } else {
        // if currently selected variant doesn't have an image,
        // load the default product image and overlay position data
        setProductImage(jsonData.variantUrls['default']);
        positionOverlay(jsonData.overlay['default']);
    }

    // retrieve the autosave of the current drawing from localforage 
    localforage.getItem('autosave').then(function (blob) {
        // if the returned object is nuot null
        if (blob != null) {
            // load into the preview overlay
            let drawingURL = URL.createObjectURL(blob);
            setOverlay(drawingURL);
            URL.revokeObjectURL(drawingURL);
        } else {
            // if the returned object is null, use a placeholder
            let drawingURL = '/media/svg/placeholder.svg';
            setOverlay(drawingURL);
        }
    }).catch(function() {
        // if there were any errors, use a placeholder image
        let drawingURL = '/media/svg/placeholder.svg';
        setOverlay(drawingURL);
    });
});

// DECLARE FUNCTIONS

/**
 *  Sets the width, top and left attributes of the absolute positionsed drawing
 *  preview overlay with data from the received array
 */
function positionOverlay(overlayArray) {
    drawingOverlay.style.width = overlayArray[0];
    drawingOverlay.style.left = overlayArray[1];
    drawingOverlay.style.top = overlayArray[2];
}

/**
 * Sets the src attribute of the drawing preview overlay
 */
function setOverlay(overlayUrl) {
    drawingOverlay.src = overlayUrl;
}

/**
 * Sets the src attribute of the product image
 */
function setProductImage(variantUrl) {
    productImage.src = variantUrl;
}

// ADD EVENT LISTENERS

// add an event listener to update the drawing preview overlay when the select-drawing select element is changed
selectDrawing.addEventListener('change', function (e) {
    // if the current drawing is selected
    if (e.target.value == '0') {
        // retrieve the autosave of the current drawing from localforage 
        localforage.getItem('autosave').then(function (blob) {
            if (blob != null) {
                // and load into the preview overlay
                let drawingURL = URL.createObjectURL(blob);
                setOverlay(drawingURL);
                URL.revokeObjectURL(drawingURL);
            } else {
                // if the returned object is null, use a placeholder
                let drawingURL = '/media/svg/placeholder.svg';
                setOverlay(drawingURL);
            }
        }).catch(function() {
            // if there were any errors, use a placeholder image
            let drawingURL = '/media/svg/placeholder.svg';
            setOverlay(drawingURL);
        });
    } else {
        // if a saved drawing is selected, load its url from the jsonData file
        let drawingURL = jsonData.drawingUrls[e.target.value];
        // then load that image into the preview overlay
        drawingOverlay.src = drawingURL;
    }
});

selectVariant.addEventListener('change', function (e) {
    // update the price to display the price of selected variant
    price.innerText = jsonData.variantPrices[e.target.value];

    // if the selected variant has an image
    if (jsonData.variantUrls[e.target.value]) {
        // set that image as the displayed product image
        setProductImage(jsonData.variantUrls[e.target.value]);
        // and load that image's overlay position data
        positionOverlay(jsonData.overlay[e.target.value]);   
    } else {
        // if selected variant doesn't have an image, load the default product 
        // image and overlay position data
        setProductImage(jsonData.variantUrls['default']);
        positionOverlay(jsonData.overlay['default']);
    }
});

// add event listener to form submit event
addToCart.addEventListener('submit', function (e) {
    // prevent default action
    e.preventDefault();
    // if the current drawing is selected
    if (selectDrawing.value == '0') {
        // retrieve the autosave of the current drawing from localforage 
        localforage.getItem('autosave').then(function (blob) {
            if (blob != null){
                // if the returned object is not null, submit the form
                addToCart.submit();
            } else {
                // if returned object is null, display an error and don't submit the form
                displayToast('error', 'No current sketchbook doodle found. Draw something cool on your sketchbook to print!');
            }
        }).catch(function() {
            // if there were any errors, display an error and don't submit the form
            displayToast('error', 'No current sketchbook doodle found. Draw something cool on your sketchbook to print!');
        });
    } else {
        // if current drawing is not selected, submit the form
        addToCart.submit();
    }
});