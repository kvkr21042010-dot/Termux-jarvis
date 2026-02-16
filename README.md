# Termux Jarvis AI

A fully functional voice assistant for Android running entirely inside Termux. It can make calls, send SMS, open apps, and browse Google using voice commands.

## 🌟 Features
* **Voice Activated:** Uses native Android speech-to-text.
* **Phone Calls:** Can search your contact list and make calls.
* **SMS Messaging:** Can send text messages to any contact.
* **App Launcher:** Opens WhatsApp, YouTube, Instagram, etc.
* **Smart Fallback:** If it doesn't know an app, it searches Google automatically.

## 📱 Prerequisites
Before installing, you **must** install these two apps on your Android phone:
1.  [Termux](https://f-droid.org/en/packages/com.termux/)
2.  [Termux:API](https://f-droid.org/en/packages/com.termux.api/)

**⚠️ CRITICAL STEP:**
After installing the **Termux:API** app, go to your phone's **Settings > Apps > Termux:API > Permissions** and allow:
* Contacts
* Microphone
* Phone / Call Logs
* SMS

## 🛠️ Installation

Run the following commands in Termux:

```bash
git clone [https://github.com/YOUR_USERNAME/Termux-Jarvis.git](https://github.com/YOUR_USERNAME/Termux-Jarvis.git)
cd Termux-Jarvis
bash setup.sh
