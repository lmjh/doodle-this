// declare toastCount at top level to allow generating a unique id for each toast
let toastCount = 0;

function generateToast(tag, message, toastCount) {
    // create variables 
    let role = "";
    let aria = "";
    let cssClass = "";
    let timeout = "";

    // assign role, aria-live region type, class and timeout based on tag
    switch (tag) {
        case "debug":
            role = "alert"
            aria = "assertive"
            cssClass = "toast-debug"
            // do not timeout debug messages
            break;
        case "info":
            role = "status"
            aria = "polite"
            cssClass = "toast-info"
            timeout = "data-bs-delay='10000'" // 10 second delay
            break;
        case "success":
            role = "status"
            aria = "polite"
            cssClass = "toast-success"
            timeout = "data-bs-delay='10000'"
            break;
        case "error":
            role = "alert"
            aria = "assertive"
            cssClass = "toast-error"
            timeout = "data-bs-delay='20000'" // 20 second delay
            break;
        default:
            role = "status"
            aria = "polite"
            cssClass = "toast-info"
            timeout = "data-bs-delay='10000'"
    }

    // generate and return toast template
    let toastTemplate = 
    `<div role="${role}" aria-live="${aria}" aria-atomic="true" class="toast ${cssClass}" id="toast-${toastCount}" 
        ${timeout}>
        <div class="toast-body">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    </div>`
    return toastTemplate
}

function displayToast(tag, message) {
    // call the generateToast function to create a new toast
    let newToastTemplate = generateToast(tag, message, toastCount);

    // add the toast to the #toast-container element
    $('#toast-container').append(newToastTemplate);

    // find the new toast using its id
    let newToastElement = document.getElementById(`toast-${toastCount}`)

    // create a bootstrap Toast object with the toast and show it
    let newToast = new bootstrap.Toast(newToastElement)
    newToast.show();

    // add an event listener to destroy the toast after its display timer runs out
    newToastElement.addEventListener('hidden.bs.toast', function(event) {
        event.target.remove()
    })

    // increment the toast counter
    toastCount += 1;
}