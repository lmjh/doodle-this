// retrieve user image URLs from JSON, if present
const jsonData = JSON.parse(document.getElementById('jsonData').textContent);
// get document elements
const doodleOverlay = document.getElementById('doodle-overlay')
const selectVariant = document.getElementById('select-variant')
const selectDoodle = document.getElementById('select-doodle')
const productImage = document.getElementById('product-image')

$( document ).ready(function() {
    // if currently selected variant has an image
    if (jsonData.variantUrls[selectVariant.value]) {
        productImage.src = jsonData.variantUrls[selectVariant.value];
        positionOverlay(jsonData.overlay[selectVariant.value]);
        
    } else {
        productImage.src = jsonData.variantUrls['default'];
        positionOverlay(jsonData.overlay['default'])
    }

    // retrieve the autosave of the current doodle from localforage 
    localforage.getItem('autosave').then(function (blob) {
        // and load into the image in the preview modal
        let drawingURL = URL.createObjectURL(blob);
        doodleOverlay.src = drawingURL;
        URL.revokeObjectURL(drawingURL);
    })

    productImage.classList.remove("invisible");
    doodleOverlay.classList.remove("invisible");
})

function positionOverlay(overlayArray) {
    doodleOverlay.style.width = overlayArray[0];
    doodleOverlay.style.left = overlayArray[1];
    doodleOverlay.style.top = overlayArray[2];
}

function setOverlay(overlayUrl) {
    doodleOverlay.src = overlayUrl;
}


document.getElementById('select-doodle').addEventListener('change', function (e) {
    // if the current doodle is selected
    if (e.target.value == 'autosave') {
        // retrieve the autosave of the current doodle from localforage 
        localforage.getItem('autosave').then(function (blob) {
            // and load into the image in the preview modal
            let drawingURL = URL.createObjectURL(blob);
            doodleOverlay.src = drawingURL;
            URL.revokeObjectURL(drawingURL);
        })
    } else {
        // set 
        let drawingURL = jsonData['drawingUrls'][e.target.value]
        doodleOverlay.src = drawingURL;
    }
})