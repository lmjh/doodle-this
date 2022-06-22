$(document).ready(function () {
    // retrieve the autosave of the current drawing from localforage 
    localforage.getItem('autosave').then(function (blob) {
        // create an objectURL for the saved drawing 
        let autosaveURL = blob ? URL.createObjectURL(blob) : false;
        // iterate through images on page
        $('img').each(function () {
            // if the image's src is the default blank image
            if ($(this).attr('src') == '/media/svg/blank.svg' && autosaveURL) {
                // replace it with the autosave image
                $(this).attr('src', autosaveURL);
            }
        });
        URL.revokeObjectURL(autosaveURL);
    });
});