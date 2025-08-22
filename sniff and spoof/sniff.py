from scapy.all import sniff, ARP
import os
import desktopalert
import emailalert

# Function to detect packet sniffing
def detect_packet_sniffing(packet):
    if packet.haslayer(ARP):
        if packet[ARP].op == 1:  # who-has (request)
            print(f"ARP Request: {packet[ARP].psrc} is asking about {packet[ARP].pdst}")
            print(f"Source IP: {packet[ARP].psrc}, Destination IP: {packet[ARP].pdst}")
        if packet[ARP].op == 2:  # is-at (response)
            print(f"ARP Response: {packet[ARP].hwsrc} has address {packet[ARP].psrc}")
            print(f"Source IP: {packet[ARP].psrc}, Destination IP: {packet[ARP].pdst}")

# Function to detect spoofing
def detect_spoofing(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:  # is-at (response)
        real_mac = os.popen(f"arp -n {packet[ARP].psrc}").read()
        if packet[ARP].hwsrc not in real_mac:
            alert_user(f"Potential Spoofing Detected: {packet[ARP].psrc} is being spoofed by {packet[ARP].hwsrc}")
            print(f"Source IP: {packet[ARP].psrc}, Destination IP: {packet[ARP].pdst}")

# Function to alert the user
def alert_user(message):
    print(f"ALERT: {message}")

# Main function to start sniffing and detecting
def main():
    print("Starting packet sniffing and spoofing detection...")
    sniff(prn=lambda x: detect_packet_sniffing(x) or detect_spoofing(x), store=0)

if __name__ == "__main__":#Ensures the main function is called only when the script is executed directly 
    main()
