<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UPI Payment Button</title>
    <style>
        .upi-button {
            background-color: #4CAF50; /* Green background */
            border: none; /* Remove borders */
            color: white; /* White text */
            padding: 15px 32px; /* Some padding */
            text-align: center; /* Centered text */
            text-decoration: none; /* Remove underline */
            display: inline-block; /* Make the button inline-block */
            font-size: 16px; /* Increase font size */
            margin: 4px 2px; /* Some margin */
            cursor: pointer; /* Pointer/hand icon */
            border-radius: 8px; /* Rounded corners */
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <a id="upi-link" href="upi://pay?pa=maybesoumo@fam&pn=Soumo%20Das%20&am=1&cu=INR&tn=Pay%20Me&mode=00" class="upi-button">Pay via UPI</a>
    <p id="error-message" class="error"></p> <!-- Placeholder for error message -->

    <script>
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
        }

        // Update the UPI link on page load
        updateUPILink();
    </script>
</body>
</html>
