import subprocess
import time
import sys
import json

# --- 1. THE BRAIN: APP DATABASE ---
# This dictionary maps spoken names to their "URL Schemes" or package links.
# You can add more here!
APPS = {
    # Social
    "whatsapp": "whatsapp://",
    "facebook": "fb://facewebmodal/f?href=https://www.facebook.com",
    "instagram": "instagram://",
    "twitter": "twitter://",
    "x": "twitter://",
    "snapchat": "snapchat://",
    "telegram": "tg://",
    "linkedin": "linkedin://",
    "reddit": "reddit://",
    "discord": "discord://",
    "tiktok": "snssdk1233://",  # Common TikTok scheme
    
    # Media
    "youtube": "vnd.youtube://",
    "spotify": "spotify://",
    "netflix": "nflx://",
    "hulu": "hulu://",
    "prime video": "primevideo://",
    
    # Tools
    "chrome": "googlechrome://",
    "google": "https://www.google.com",
    "gmail": "googlegmail://",
    "maps": "geo:0,0?q=",
    "uber": "uber://",
    "amazon": "com.amazon.mobile.shopping.web://",
    "play store": "market://details?id=com.termux", # Opens store
    "settings": "android.settings.SETTINGS" # Might require root/ADB, but tries standard intent
}

# --- 2. CORE FUNCTIONS ---

def speak(text):
    """Speaks text without blocking the code."""
    print(f">> Jarvis: {text}")
    # Using Popen for background speaking so it doesn't freeze
    subprocess.Popen(["termux-tts-speak", text]) 

def listen():
    """Captures voice input."""
    # This launches the popup.
    try:
        result = subprocess.run(
            ["termux-speech-to-text"], 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip().lower()
    except Exception:
        return ""

def get_contact_number(spoken_name):
    """Searches real Android contacts for a name."""
    print(f"...Searching contacts for '{spoken_name}'...")
    try:
        # Get contacts dump
        result = subprocess.run(["termux-contact-list"], capture_output=True, text=True)
        contacts = json.loads(result.stdout)
        
        # Filter for the name
        for c in contacts:
            if spoken_name in c['name'].lower():
                return c['number']
    except:
        pass
    return None

# --- 3. SMART ACTIONS ---

def open_app(app_name):
    """Tries to open an app. If unknown, searches Google."""
    if app_name in APPS:
        speak(f"Opening {app_name}...")
        subprocess.run(["termux-open-url", APPS[app_name]])
    else:
        speak(f"I'm not sure how to open {app_name}, searching Google instead.")
        subprocess.run(["termux-open-url", f"https://www.google.com/search?q={app_name}"])
    
    # Wait for the screen to switch so we don't crash
    time.sleep(3)

def make_call(name):
    num = get_contact_number(name)
    if num:
        speak(f"Calling {name}...")
        subprocess.run(["termux-telephony-call", num])
        time.sleep(3)
    else:
        speak(f"I couldn't find {name} in your contacts.")

def send_sms(name):
    num = get_contact_number(name)
    if num:
        speak(f"What's the message for {name}?")
        # Short pause to ensure TTS is done
        time.sleep(1.5)
        msg = listen()
        if msg:
            speak("Sending message...")
            subprocess.run(["termux-sms-send", "-n", num, msg])
            speak("Sent.")
        else:
            speak("Message cancelled.")
    else:
        speak(f"I couldn't find {name} in your contacts.")

# --- 4. MAIN LOOP ---

def main():
    # Keep screen awake so it runs longer
    subprocess.run(["termux-wake-lock"])
    speak("Jarvis is ready.")
    
    while True:
        try:
            command = listen()
            
            if not command:
                # If nothing was said, wait a tiny bit and retry
                # This prevents CPU overheating from instant looping
                time.sleep(1) 
                continue
                
            print(f"User: {command}")

            # --- COMMANDS ---
            
            if "stop" in command or "exit" in command:
                speak("Goodbye.")
                subprocess.run(["termux-wake-unlock"])
                break

            elif "open" in command:
                # "open youtube" -> "youtube"
                app_name = command.replace("open", "").strip()
                open_app(app_name)

            elif "call" in command:
                # "call mom" -> "mom"
                name = command.replace("call", "").strip()
                make_call(name)

            elif "message" in command or "text" in command:
                # "message dad" -> "dad"
                name = command.replace("message", "").replace("text", "").strip()
                send_sms(name)

            elif "time" in command:
                 t = time.strftime("%I:%M %p")
                 speak(f"It is {t}")
            
            else:
                 # If command is unknown, maybe they just said an app name?
                 # Try to open it as a fallback
                 open_app(command)

            time.sleep(0.5)

        except KeyboardInterrupt:
            speak("Shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
