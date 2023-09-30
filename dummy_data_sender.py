from pythonosc import udp_client
import time


def main():
    # Setup the OSC client with the target IP and port
    # Replace these values with the IP and port of the machine where your OSC server is running
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

    # Send an OSC message to trigger data saving
    # This will send a message to the address "/Interfaz/save_data" along with some dummy data
    
    client.send_message("/Interfaz/save_data", [])
    client.send_message("/Interfaz/year", ["2023"])
    client.send_message("/Interfaz/scene", ["2"])
    client.send_message("/Interfaz/subject", ["1"])

    # Wait for a while to ensure the message is sent before closing the script
    # You can remove this if not necessary
    time.sleep(1)


if __name__ == "__main__":
    main()
