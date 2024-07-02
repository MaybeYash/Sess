// Function to parse URL parameters
function getQueryParams() {
    const params = {};
    const queryString = window.location.href.split('?')[1];
    if (queryString) {
        const pairs = queryString.split('&');
        for (let pair of pairs) {
            const [key, value] = pair.split('=');
            params[key.toLowerCase()] = decodeURIComponent(value);
        }
    }
    return params;
}

// Function to update UPI link with new amount
function updateUPILink() {
    const params = getQueryParams();
    let amount = 1; // Default amount
    const errorMessage = document.getElementById('error-message');

    if (params.send) {
        if (params.send.toLowerCase() === 'none') {
            amount = 0;
        } else {
            const parsedAmount = parseFloat(params.send);
            if (isNaN(parsedAmount) || parsedAmount <= 0) {
                errorMessage.textContent = 'Invalid amount specified. Please provide a valid positive number.';
                return;
            } else {
                amount = parsedAmount;
            }
        }
    }

    const upiLink = document.getElementById('upi-link');
    const upiHref = `upi://pay?pa=maybesoumo@fam&pn=Soumo%20Das%20&am=${amount}&cu=INR&tn=Pay%20Me&mode=00`;
    upiLink.href = upiHref;

    // Clear any previous error messages if amount is valid
    if (amount > 0 || params.send.toLowerCase() === 'none') {
        errorMessage.textContent = '';
    }

    // Generate QR code based on updated UPI link
    generateQRCode(upiHref, amount);
}

// Function to generate QR code
function generateQRCode(upiURL, amount) {
    const defaultImg = document.querySelector("#default-img");
    const loader = document.querySelector(".honeycomb");
    const qrCode = document.querySelector("#qrcode");
    const downloadButton = document.getElementById("download-button");

    defaultImg.style.display = "none";
    qrCode.style.display = "none";
    loader.style.display = "block";

    setTimeout(function () {
        let image = document.querySelector("#qrcode img");
        let canvasElement = document.querySelector("canvas");

        if (canvasElement) {
            canvasElement.remove();
        }

        if (image) {
            image.remove();
        }

        qrCode.style.display = "block";
        loader.style.display = "none";

        var qrcode = new QRCode("qrcode", upiURL, {
            width: 80,
            height: 80,
        });

        downloadButton.style.display = "block";
        createNotification(`QR Code for UPI payment of ${amount} INR Generated Successfully :)`, "success");
    }, 1200);
}

// Function to handle toast notifications
function createNotification(message, type) {
    const toasts = document.getElementById("toasts");
    const notif = document.createElement('div');
    notif.classList.add('toast');

    if (type === "success") {
        notif.classList.add('success');
    } else if (type === "fail") {
        notif.classList.add('fail');
    }

    notif.innerHTML = message;
    toasts.appendChild(notif);

    setTimeout(function () {
        notif.remove();
    }, 2000);
}

// Update the UPI link and generate QR code on page load
updateUPILink();
