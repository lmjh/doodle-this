// INITIALISE ELEMENTS AND STYLES

// retrieve user image URLs from JSON, if present
const jsonData = JSON.parse(document.getElementById('jsonData').textContent);
// get document elements
const doodleOverlay = document.getElementById('doodle-overlay')
const selectVariant = document.getElementById('variant')
const selectDoodle = document.getElementById('doodle')
const productImage = document.getElementById('product-image')
const price = document.getElementById('price')

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
        positionOverlay(jsonData.overlay['default'])
    }

    // retrieve the autosave of the current doodle from localforage 
    localforage.getItem('autosave').then(function (blob) {
        // and load into the overlay image
        let drawingURL = URL.createObjectURL(blob);
        setOverlay(drawingURL);
        URL.revokeObjectURL(drawingURL);
    })
})

// DECLARE FUNCTIONS

/**
 *  Sets the width, top and left attributes of the absolute positionsed drawing
 *  preview overlay with data from the received array
 */
function positionOverlay(overlayArray) {
    doodleOverlay.style.width = overlayArray[0];
    doodleOverlay.style.left = overlayArray[1];
    doodleOverlay.style.top = overlayArray[2];
}

/**
 * Sets the src attribute of the drawing preview overlay
 */
function setOverlay(overlayUrl) {
    doodleOverlay.src = overlayUrl;
}

/**
 * Sets the src attribute of the product image
 */
function setProductImage(variantUrl) {
    productImage.src = variantUrl;
}

// ADD EVENT LISTENERS

// add an event listener to update the drawing preview overlay when the select-doodle select element is changed
selectDoodle.addEventListener('change', function (e) {
    // if the current doodle is selected
    if (e.target.value == 'autosave') {
        // retrieve the autosave of the current doodle from localforage 
        localforage.getItem('autosave').then(function (blob) {
            // and load into the preview overlay
            let drawingURL = URL.createObjectURL(blob);
            setOverlay(drawingURL);
            URL.revokeObjectURL(drawingURL);
        })
    } else {
        // if a saved doodle is selected, load its url from the jsonData file
        let drawingURL = jsonData['drawingUrls'][e.target.value]
        // then load that image into the preview overlay
        doodleOverlay.src = drawingURL;
    }
})

selectVariant.addEventListener('change', function (e) {
    // update the price to display the price of selected variant
    price.innerText = jsonData.variantPrices[e.target.value]

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
        positionOverlay(jsonData.overlay['default'])
    }
})
