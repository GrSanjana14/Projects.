from plyer import notification

notification.notify(
    title="⚠ Packet Sniffing Detected ⚠",
    message= "Suspicious activity detected: Your network traffic may be monitored. Please check your connection security .",
    timeout=10
)

        