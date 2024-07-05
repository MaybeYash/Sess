<?php
// Retrieve user details
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$ip_address = $_SERVER['REMOTE_ADDR'];
$timestamp = date('Y-m-d H:i:s');
$referrer = $_SERVER['HTTP_REFERER'] ?? 'Direct visit';

// Telegram Bot API settings
$telegram_bot_token = 'YOUR_TELEGRAM_BOT_TOKEN';
$telegram_chat_id = 'YOUR_TELEGRAM_CHAT_ID';

// Compose message
$message = "New visitor details:\n";
$message .= "Timestamp: $timestamp\n";
$message .= "IP Address: $ip_address\n";
$message .= "User Agent: $user_agent\n";
$message .= "Referrer: $referrer";

// Send message to Telegram
$api_url = "https://api.telegram.org/bot$telegram_bot_token/sendMessage";
$params = [
    'chat_id' => $telegram_chat_id,
    'text' => $message,
];

// Use cURL to send POST request
$ch = curl_init($api_url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);
?>
