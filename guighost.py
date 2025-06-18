import os
import time
import threading
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyautogui
import webbrowser
import urllib.parse
import customtkinter as ctk

# === Configuration ===
DEFAULT_COUNTRY_CODE = "91"
LISTEN_TIMEOUT = 30  # Extended timeout

# === Initialize TTS engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    def run_tts():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_tts, daemon=True).start()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (say 'g' to activate)")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=LISTEN_TIMEOUT)
        except sr.WaitTimeoutError:
            return ""
    try:
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "API error"

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That is too broad. Try being more specific, e.g., {e.options[0]}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on Wikipedia."
    except Exception:
        return "Something went wrong while accessing Wikipedia."

def open_app(command):
    apps = {
        "chrome": "start chrome",
        "brave": "start brave",
        "notepad": "start notepad",
        "calculator": "start calc",
        "vs code": "start code",
        "whatsapp": "start whatsapp",
        "spotify": "start spotify",
        "discord": "start discord",
        "steam": "start steam",
        "vlc": "start vlc",
        "firefox": "start firefox",
        "edge": "start msedge",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "paint": "start mspaint",
        "explorer": "start explorer",
        "task manager": "start taskmgr",
        "control panel": "start control",
        "mcafee": '"C:\\Program Files\\McAfee\\MSC\\mcuihost.exe"',
    }

    for key in apps:
        if key in command:
            os.system(apps[key])
            return
    speak("I don't know how to open that app yet.")

def type_in_notepad(text):
    os.system("start notepad")
    time.sleep(1.5)
    pyautogui.typewrite(text, interval=0.05)

def send_whatsapp_message(phone_number, message):
    encoded_msg = urllib.parse.quote(message)
    url = f"https://wa.me/{phone_number}?text={encoded_msg}"
    webbrowser.open(url)

def calculate_math(expression):
    try:
        allowed = "0123456789+-*/(). "
        if all(char in allowed for char in expression):
            result = eval(expression)
            return f"The answer is {result}"
        else:
            return "I can only calculate numbers and math operators."
    except:
        return "Sorry, I couldn't calculate that."

class GhostApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GHOST AI Assistant")
        self.geometry("700x500")
        self.resizable(False, False)

        self.output_box = ctk.CTkTextbox(self, width=680, height=400, corner_radius=10)
        self.output_box.grid(row=0, column=0, padx=10, pady=10)
        self.output_box.configure(state="disabled")

        self.start_button = ctk.CTkButton(self, text="Start GHOST", command=self.start_ghost)
        self.start_button.grid(row=1, column=0, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.running = False

    def append_text_typing(self, text, speaker="GHOST"):
        self.output_box.configure(state="normal")
        self.output_box.insert(ctk.END, f"{speaker}: ")
        self.output_box.configure(state="disabled")
        self.output_box.see(ctk.END)

        def delayed_speak():
            words = text.split()
            if len(words) >= 2:
                time.sleep(0.1)
                speak(text)

        threading.Thread(target=delayed_speak, daemon=True).start()

        def typewriter():
            for char in text:
                self.output_box.configure(state="normal")
                self.output_box.insert(ctk.END, char)
                self.output_box.configure(state="disabled")
                self.output_box.see(ctk.END)
                time.sleep(0.02)
            self.output_box.configure(state="normal")
            self.output_box.insert(ctk.END, "\n")
            self.output_box.configure(state="disabled")
            self.output_box.see(ctk.END)

        threading.Thread(target=typewriter).start()

    def start_ghost(self):
        if self.running:
            return
        self.running = True
        self.append_text_typing("GHOST is ready. Say 'g' to activate me.", "GHOST")
        threading.Thread(target=self.run_ghost, daemon=True).start()

    def run_ghost(self):
        while self.running:
            query = listen()
            print("Heard:", query)
            if query.startswith("g"):
                command = query.replace("g", "", 1).strip()

                if any(word in command for word in ["exit", "quit", "stop"]):
                    self.append_text_typing("Goodbye!", "GHOST")
                    self.running = False
                    break

                elif "play video" in command:
                    query = command.replace("play video", "").strip()
                    if query:
                        self.append_text_typing(f"Playing {query} on YouTube.", "GHOST")
                        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                        webbrowser.open(url)
                    else:
                        self.append_text_typing("What video would you like me to play?", "GHOST")


                elif "open" in command:
                    open_app(command)
                    self.append_text_typing(f"Opening app for command: {command}", "GHOST")

                elif "type" in command and "notepad" in command:
                    self.append_text_typing("What should I type?", "GHOST")
                    to_type = listen()
                    self.append_text_typing(f"Typing: {to_type}", "GHOST")
                    type_in_notepad(to_type)

                elif "whatsapp" in command and "message" in command:
                    self.append_text_typing("Yes, why not. But what is the phone number of the client?", "GHOST")
                    phone = listen().replace(" ", "").replace("+", "")
                    if not phone.startswith(DEFAULT_COUNTRY_CODE):
                        phone = DEFAULT_COUNTRY_CODE + phone
                    self.append_text_typing("Yes, why not. But now what is the message to send?", "GHOST")
                    message = listen()
                    self.append_text_typing("Opening WhatsApp with your message.", "GHOST")
                    send_whatsapp_message(phone, message)

                elif command.startswith("after me"):
                    to_repeat = command.replace("after me", "", 1).strip()
                    if to_repeat:
                        self.append_text_typing(to_repeat, "GHOST")
                    else:
                        self.append_text_typing("Please say what you want me to repeat.", "GHOST")

                elif "who are you" in command:
                    self.append_text_typing("I am an AI assistant made by Aman Singh with help of the Lucifer team.", "GHOST")

                elif any(op in command for op in ['+', '-', '*', '/', 'x']):
                    math_expr = command.replace('x', '*').replace('multiply', '*')
                    result = calculate_math(math_expr)
                    self.append_text_typing(result, "GHOST")

                else:
                    response = search_wikipedia(command)
                    self.append_text_typing(response, "GHOST")

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = GhostApp()
    app.mainloop()
