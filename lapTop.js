// Function to generate a rainbow gradient QR code
function generateQRCode(link) {
    const qrCodeContainer = document.getElementById('qr-code');
    qrCodeContainer.innerHTML = ''; // Clear any existing QR code

    // Create a new QRCodeStyling instance
    const qrCode = new QRCodeStyling({
        width: 300,
        height: 300,
        data: link,
        image: '/mnt/data/308837678-237b9244-5f20-4b9e-abe5-e4af90b21a96%20(1).jpg', // Your background image
        imageOptions: {
            crossOrigin: 'anonymous',
            margin: 20,
        },
        dotsOptions: {
            color: '#4CAF50',
            type: 'dots',
        },
        backgroundOptions: {
            color: '#FFFFFF',
        },
        imageOptions: {
            hideBackgroundDots: true,
            imageSize: 0.4,
        },
    });

    // Render the QR code inside the container
    qrCode.append(qrCodeContainer);
}

// Function to handle page load and updates
window.onload = function() {
    updateUPILink(); // Initial update

    // Event listener for changes in URL parameters
    window.addEventListener('popstate', function(event) {
        updateUPILink();
    });

    // Event listener for Binance Pay button click
    const binancePayButton = document.getElementById('binance-button');
    binancePayButton.addEventListener('click', function(event) {
        const binancePage = document.getElementById('binance-page');
        binancePage.classList.toggle('visible');
    });
};
