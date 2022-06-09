// INITIALISE ELEMENTS AND STYLES

// find sketchbook element
const canvas = document.querySelector('#sketchbook');
// initialise Atrament canvas
const sketchbook = new Atrament(canvas, {
    width: 1280,
    height: 720,
    adaptiveStroke: false,
    // set colour to the current value of the coloris color picker 
    color: document.getElementById('coloris-picker').value,
    // set weight to the current value of the stroke weight slider 
    weight: parseInt(document.getElementById('stroke-weight').value),
});

// parse the urls dictionary object passed from the view and assign to a variable
const urls = JSON.parse(document.getElementById('urls').textContent);

// parse the titles dictionary object passed from the view and assign to a variable
// declared as 'var' as it will be updated by the application
var titles = JSON.parse(document.getElementById('titles').textContent);

// initialise Coloris colour picker
Coloris({
    el: '.coloris',
    theme: 'polaroid',
    themeMode: 'dark',
    alpha: false,
    format: 'rgb',
    defaultColor: "#000000",
});

// set the cursor element's colour to the value of the Coloris picker
$('#cursor').css('background-color', document.getElementById('coloris-picker').value);

// call resizeCanvas function
resizeCanvas();

// call configureSketchbook function
configureSketchbook()

// call the updateTitleField function
updateTitleField()

// set the load button state for save slot one, which is selected on page load
setLoadButtonState("1");

// if an autosave state is present, load it
localforage.keys().then(function(keys) {
    if (keys.includes('autosave')) {
        loadDrawingFromLocal('autosave');
    }
}).catch(function(err) {
    // This code runs if there were any errors
    console.log(err);
});

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

    // scale the contents of the scaler by the calculated ratio
    scaler.style.transform = 'scale(' + scale + ')';

    // set scaler-holder height to height of scaler to fix layout bug
    $('#scaler-holder').height(scaler.getBoundingClientRect().height);

    // find paper background element
    paper = $('#paper')

    // set background to same height and width as canvas by multiplying canvas dimensions by scaling ratio
    $('#paper').height(720 * scale)
    $('#paper').width(1280 * scale)

    // transform paper by inverse of scaling ratio to cancel out transform and fix visual distortions
    paper.css('transform', 'scale(' + (1 / scale) + ')');
}

function configureSketchbook() {
    if (localStorage.hasOwnProperty('color')) {
        // if color is saved in local storage, load color
        let color = localStorage.color;
        changeAtramentColor(color);
        changeColorisColor(color);
        changeCursorColor(color);
    } else {
        // if color is not saved in local storage, set to black and save
        let color = "rgb(0, 0, 0, 255)";
        changeAtramentColor(color);
        changeColorisColor(color);
        changeCursorColor(color);
    }

    if (localStorage.hasOwnProperty('weight')) {
        // if weight is saved in local storage, load weight
        let weight = parseInt(localStorage.weight);
        changeWeight(weight);
    } else {
        // if weight is not saved in local storage, set to 20 and save
        let weight = 20;
        changeWeight(weight)
    }

    if (localStorage.hasOwnProperty('paperType')) {
        // if paperType is saved in local storage, load paperType
        let paperType = localStorage.paperType;
        changePaper(paperType);
    } else {
        // if paperType is not saved in local storage, set to 'watermarked' and save
        let paperType = 'watermark';
        changePaper(paperType)
    }

    if (localStorage.hasOwnProperty('smoothing')) {
        // if smoothing is saved in local storage, load smoothing
        let smoothing = parseFloat(localStorage.smoothing);
        changeSmoothing(smoothing);
    } else {
        // if smoothing is not saved in local storage, set to 0.65 and save
        let smoothing = 0.65;
        changeSmoothing(smoothing)
    }

    if (localStorage.hasOwnProperty('adaptiveStroke')) {
        // if adaptiveStroke is saved in local storage, load adaptiveStroke
        let adaptiveStroke = localStorage.adaptiveStroke;
        // set adaptiveStroke to boolean true if the string matches 'on', false if it doesn't
        sketchbook.adaptiveStroke = adaptiveStroke == 'on';
    } else {
        // if adaptiveStroke is not saved in local storage, set to 'off' and save
        adaptiveStroke = 'off';
        sketchbook.adaptiveStroke = false;
    }

    // set page controls to match saved settings
    $('#stroke-weight').val(localStorage.weight)
    $('#smoothing').val(localStorage.smoothing)
    // check the checkboxes with an ids matching the saved values
    $(`#${localStorage.paperType}`).prop('checked', true)
    $(`#${localStorage.adaptiveStroke}`).prop('checked', true)
}

/**
 * Takes a colour as a string and uses it to set the Atrament canvas' current colour. Saves the selected colour in
 * local storage.
 */
function changeAtramentColor(color) {
    sketchbook.color = color;

    localStorage.setItem('color', color);
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
 * Changes the stroke weight of the Atrament canvas to the received int and updates the cursor preview to match. Saves
 * selected weight in local storage.
 */
function changeWeight(weight) {
    // pass to Atrament canvas
    sketchbook.weight = weight;
    // set cursor preview to same width and height as canvas tool
    $('#cursor').css('width', weight).css('height', weight);

    localStorage.setItem('weight', weight);
}

/**
 * Changes the stroke smoothing factor of the Atrament canvas to the value of received float. Saves the value to local
 * storage.
 */
function changeSmoothing(smoothing) {
    // pass float to Atrament canvas
    sketchbook.smoothing = smoothing;

    localStorage.setItem('smoothing', smoothing);
}

/**
 * Changes the background of the sketchbook according to the received string. Saves the setting to local storage.
 */
function changePaper(paperType) {
    // find the paper background element
    paper = $('#paper');
    // remove all paper classes
    paper.removeClass('plain-paper watermarked-paper lined-paper squared-paper');

    localStorage.setItem('paperType', paperType);

    // use the received string to set the paper class
    switch (paperType) {
        case "none":
            paper.addClass('plain-paper');
            break;
        case "watermark":
            paper.addClass('watermarked-paper');
            break;
        case "lined":
            paper.addClass('lined-paper');
            break;
        case "squared":
            paper.addClass('squared-paper');
            break;
        default:
            // default to plain paper
            paper.addClass('plain-paper');
    }
}

/**
 * Converts canvas drawing to blob, gathers form data and sends to server to save drawing in database
 */
function saveDrawingToDb() {
    // convert canvas drawing to blob
    canvas.toBlob(function (blob) {
        // create a new FormData object
        let formData = new FormData();
        // find csrf token elements and assign to variable
        let csrf = document.getElementsByName('csrfmiddlewaretoken');
        // find selected save_slot radio button and assign to variable
        let saveSlot = parseInt($('input[name=drawing-save-slot]:checked', '#drawing-form').val());
        // get value of title field
        let title = $('#id_title').val();
        // append csrf token, save_slot, title and canvas blob to form
        formData.append('csrfmiddlewaretoken', csrf[0].value)
        formData.append('save_slot', saveSlot);
        formData.append('title', title);
        formData.append('image', blob, 'drw.png');

        // send form and image to server with jquery AJAX
        $.ajax({
            type: 'POST',
            url: urls.save_drawing,
            enctype: 'multipart/form-data',
            data: formData,
            success: function (response) {
                // display alert to notify user of successful save
                displayToast('success', 'Your drawing has been saved!')
                // find the preview image corresponding to the selected save slot
                let savePreview = $('#save-preview-' + saveSlot)
                // update the preview image with the url returned in the JSON response
                savePreview.attr('src', response['url'])
                // update the title dictionary with the submitted title
                updateTitleDict(saveSlot, title)
                // update the load button state
                setLoadButtonState(saveSlot)
            },
            error: function (error) {
                displayToast('error', 'Something seems to have gone wrong. Please try again.')
            },
            cache: false,
            // set contentType and processData to false to allow passing files
            // to the server
            contentType: false,
            processData: false,
        })
    })
}

/**
 * Sends a request to the server with the currently selected save slot and then loads the returned image onto the canvas
 */
function loadDrawingFromDb() {
    // get the currently selected save_slot
    let saveSlot = parseInt($('input[name=drawing-save-slot]:checked', '#drawing-form').val());
    let data = {
        'save_slot': saveSlot
    };
    // get the url for the get_drawing view
    let url = urls.get_drawing;

    // initiate a ajax request
    $.ajax({
        url: url,
        type: "GET",
        data: data,
        // on success, load the image
        success: function (response) {
            // clear canvas
            sketchbook.clear()
            // get canvas context
            let canvasContext = canvas.getContext('2d');

            // disable image smoothing
            canvasContext.mozImageSmoothingEnabled = false;
            canvasContext.webkitImageSmoothingEnabled = false;
            canvasContext.msImageSmoothingEnabled = false;
            canvasContext.imageSmoothingEnabled = false;

            // instantiate a new Image object
            let drawing = new Image();

            // update the canvas once the image has been loaded
            drawing.onload = function (event) {
                canvasContext.drawImage(event.target, 0, 0);
                displayToast('success', 'Your drawing has been loaded!')
            }

            // set the src attribute of the new Image as the response url 
            drawing.src = response.url;
        },
        error: function (response) {
            displayToast('error', 'Something seems to have gone wrong. Please try again.')
        }
    });
}

/**
 * Converts canvas drawing to blob and uses localForage to save it locally under the given key
 */
function saveDrawingToLocal(key) {
    // convert canvas drawing to blob
    canvas.toBlob(function (blob) {
        // save the blob locally with localForage
        localforage.setItem(key, blob).catch(function (err) {
            // catch any errors and print to console
            console.log("Error: " + err);
        })
    })
}

/**
 * Uses localForage to load a blob from the given key and draws it on the canvas
 */
function loadDrawingFromLocal(key) {
    //  retreieve blob at given key from local storage using localForage
    localforage.getItem(key).then(function (blob) {
        // clear canvas
        sketchbook.clear()
        // get canvas context
        let canvasContext = canvas.getContext('2d');

        // disable image smoothing
        canvasContext.mozImageSmoothingEnabled = false;
        canvasContext.webkitImageSmoothingEnabled = false;
        canvasContext.msImageSmoothingEnabled = false;
        canvasContext.imageSmoothingEnabled = false;

        // instantiate a new Image object
        let drawing = new Image();

        // update the canvas once the image has been loaded
        drawing.onload = function (event) {
            // revoke the no longer needed object url
            URL.revokeObjectURL(event.target.src);
            canvasContext.drawImage(event.target, 0, 0);
        }

        // create an object url for the blob and assign it as the src attribute of the image 
        drawing.src = URL.createObjectURL(blob);
    }).catch(function (err) {
        // catch any errors and print to console
        console.log("Error: " + err);
    })
};

/**
 * Disable all controls in the save / load modal
 */
function disableSaveLoadButtons () {
    $('#save-dialog-toggle').prop('disabled', true);
    $('#load-dialog-toggle').prop('disabled', true);
    $('#save-slot-1').prop('disabled', true);
    $('#save-slot-2').prop('disabled', true);
    $('#save-slot-3').prop('disabled', true);
    $('#id_title').prop('disabled', true);
}

/**
 * Pass selected save slot to the setLoadButtonState function to enable load button if a drawing is saved there.
 * Enable all other controls in the save / load modal.
 */
function enableSaveLoadButtons () {
    let saveSlot = $("#drawing-save-slot input[type='radio']:checked").val();
    setLoadButtonState(saveSlot);
    $('#save-dialog-toggle').prop('disabled', false);
    $('#save-slot-1').prop('disabled', false);
    $('#save-slot-2').prop('disabled', false);
    $('#save-slot-3').prop('disabled', false);
    $('#id_title').prop('disabled', false);
}

/**
 * Restores the save/load modal to its default state.
 */
function restoreSaveLoadState() {
    // re-enable the buttons
    enableSaveLoadButtons();
    // remove the 'show' class from the two collapsible elements of the modal
    $('#save-confirm').removeClass('show');
    $('#load-confirm').removeClass('show');
}

/**
 * Updates the title input field with the value of the currently selected save slot
 */
function updateTitleField() {
    let saveSlot = parseInt($('input[name=drawing-save-slot]:checked', '#drawing-form').val());
    let title = titles[`title_${saveSlot}`];
    $('#id_title').val(title);
}

/**
 * Updates the title dictionary corresponding to the given save slot with the given string
 */
function updateTitleDict(saveSlot, newTitle) {
    titles[`title_${saveSlot}`] = newTitle;
}

/**
 * Enables or disables the load drawing button when the user selects a save slot
 */
 function setLoadButtonState(saveSlot) {
    // if the preview image for the selected save slot is the default blank image, disable the load button
    if ($(`#save-preview-${saveSlot}`).attr('src') == '/media/svg/blank.svg') {
        $('#load-dialog-toggle').prop('disabled', true);
    } else {
        // otherwise, enable the button
        $('#load-dialog-toggle').prop('disabled', false);
    }
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
window.addEventListener("resize", function () {
    if (resizeTimer != null) window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () {
        resizeCanvas();
    }, 200);
});

// add an event listener to the element that holds the preset colour buttons
document.getElementById("preset-colour-holder").addEventListener("click", function (e) {
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
sketchbook.addEventListener('colorpicked', function (e) {
    // use the colour returned by the colorpicked event to update the Coloris plugin and cursor preview 
    changeColorisColor(e.color);
    changeCursorColor(e.color);
});

// add an event listener to the element that holds the tool buttons
document.getElementById("tool-holder").addEventListener("click", function (e) {
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
document.getElementById('stroke-weight').addEventListener('change', function (e) {
    // convert the event taget's value to an int
    let weight = parseInt(e.target.value);
    // pass to the changeWeight function
    changeWeight(weight);
});

// add event listener to clear Atrament canvas when clear confirmation button is clicked
document.getElementById('clear-sketchbook').addEventListener('click', function () {
    sketchbook.clear();
    // remove undoCache and disable undo button when clearing canvas
    localforage.removeItem('undoCache').then( function () {
        $('#undo-side').prop('disabled', true);
        $('#undo-bottom').prop('disabled', true);
    }).catch(function(error) {
        console.log(error);
    })
    // also remove autosave
    localforage.removeItem('autosave').catch(function(error) {
        console.log(error);
    })

});

// add event listener to change Atrament canvas stroke smoothing factor when slider is changed
document.getElementById('smoothing').addEventListener('change', function (e) {
    // convert the value of the slider to a float and pass to the changeSmoothing function
    smoothing = parseFloat(e.target.value);
    changeSmoothing(smoothing);
});

// add event listener to change the paper background when the selected checkbox changes
document.getElementById('paper-type').addEventListener('click', function (e) {
    if (e.target && e.target.matches(".btn-check")) {
        // pass the id of the triggering button to the changePaper function
        changePaper(e.target.id);
    }
});

// add an event listener to the element that holds the adaptive stroke radio buttons
document.getElementById("adaptive-stroke").addEventListener("click", function (e) {
    // if the user selects one of the radio buttons
    if (e.target && e.target.matches(".btn-check")) {
        let adaptiveStroke = e.target.id;

        // the expression adaptiveStroke == 'on' will evaluate to true if user selects the 'on' button.
        // otherwise it will evaluate to false.
        sketchbook.adaptiveStroke = adaptiveStroke == 'on';

        localStorage.setItem('adaptiveStroke', adaptiveStroke);
    }
});

// add an event listener to the element that holds the save and load buttons
document.getElementById("save-load-buttons").addEventListener("click", function (e) {
    if (e.target && e.target.matches(".btn")) {
         // if the user activates either of the buttons, disable the form controls
        disableSaveLoadButtons();
    }
});

// add an event listener to the save-confirm collapsible dialog
document.getElementById("save-confirm").addEventListener("click", function (e) {
    if (e.target && e.target.matches(".cancel-button")) {
        // if the user activates the cancel button, re-activate the form controls
        enableSaveLoadButtons();
    } else if (e.target && e.target.matches("#save-drawing")) {
        // if the user activates the save-drawing button, save the canvas to the database
        saveDrawingToDb();
        // and re-activate the form controls
        enableSaveLoadButtons();
    }
});

// add an event listener to the load-confirm collapsible dialog
document.getElementById("load-confirm").addEventListener("click", function (e) {
    if (e.target && e.target.matches(".cancel-button")) {
        // if the user activates the cancel button, re-activate the form controls
        enableSaveLoadButtons();
    } else if (e.target && e.target.matches("#load-drawing")) {
        // if the user activates the load-drawing button, re-activate the form controls
        enableSaveLoadButtons();
        // and load the selected drawing to the canvas
        loadDrawingFromDb();
    }
});

// add an event listener to the save slot modal to restore the it to its default state after closing.
document.getElementById('saveModal').addEventListener('hidden.bs.modal', restoreSaveLoadState)

// add an event listener to the save slot selection checkboxes
document.getElementById('drawing-save-slot').addEventListener('click', function (e) {
    if (e.target && e.target.matches(".btn-check")) {
        // get the value the triggering button
        saveSlot = e.target.value;
        // pass the save slot to the functions to update the title field and enable/diable the load button
        updateTitleField(saveSlot);
        setLoadButtonState(saveSlot);
    }
});

// add event listener to the sketchbook to store the state before a stroke is drawn
sketchbook.addEventListener('strokestart', function() {
    // call the saveDrawingToLocal function to store the canvas state for undo
    saveDrawingToLocal('undoCache');
    // enable the undo buttons
    $('#undo-side').prop('disabled', false);
    $('#undo-bottom').prop('disabled', false);
})

// add event listener to the sketchbook to store the state before a fill is drawn
sketchbook.addEventListener('fillstart', function() {
    // call the saveDrawingToLocal function to store the canvas state for undo
    saveDrawingToLocal('undoCache');
    // enable the undo buttons
    $('#undo-side').prop('disabled', false);
    $('#undo-bottom').prop('disabled', false);
})

// add event listener to the side menu undo button
document.getElementById('undo-side').addEventListener('click', function() {
    // on click, load the undo cache onto the canvas
    loadDrawingFromLocal('undoCache');
    // remove the undo cache from memory
    localforage.removeItem('undoCache').then( function () {
        // disable undo buttons once cache is removed
        $('#undo-side').prop('disabled', true);
        $('#undo-bottom').prop('disabled', true);
        // update the autosave file
        saveDrawingToLocal('autosave');
    }).catch(function(error) {
        console.log(error);
    })
})

// add event listener to the bottom menu undo button
document.getElementById('undo-bottom').addEventListener('click', function() {
    // on click, load the undo cache onto the canvas
    loadDrawingFromLocal('undoCache');
    // remove the undo cache from memory
    localforage.removeItem('undoCache').then( function () {
        // disable undo buttons once cache is removed
        $('#undo-side').prop('disabled', true);
        $('#undo-bottom').prop('disabled', true);
        // update the autosave file
        saveDrawingToLocal('autosave');
    }).catch(function(error) {
        console.log(error);
    })
})

// add event listener to the sketchbook to store the state after a stroke is drawn
sketchbook.addEventListener('strokeend', function() {
    // call the saveDrawingToLocal function to store the canvas state for autosave
    saveDrawingToLocal('autosave');
})

// add event listener to the sketchbook to store the state after a fill is drawn
sketchbook.addEventListener('fillend', function() {
    // call the saveDrawingToLocal function to store the canvas state for autosave
    saveDrawingToLocal('autosave');
})
