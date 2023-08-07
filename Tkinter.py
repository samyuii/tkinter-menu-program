# A simple Python menu program


import pywhatkit as pwk
import psutil
import pyaudio
import speech_recognition as sr
import subprocess
import numpy as np
import cv2
from PIL import Image
from geopy.geocoders import Nominatim
from googlesearch import search
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox

def show_menu():
    menu_text = "Welcome to the Menu!\n"
    menu_text += "1. To find RAM usage\n"
    menu_text += "2. To send Whatsapp msg\n"
    menu_text += "3. Speech to text\n"
    menu_text += "4. Image creation\n"
    menu_text += "5. Face picture crop\n"
    menu_text += "6. Sunglasses on Face picture\n"
    menu_text += "7. Know your GPS co-ordinates\n"
    menu_text += "8. Google search\n"
    menu_text += "9. Exit\n"
    return menu_text

def process_choice(choice):
    if choice == "1":
        ram_usage = f"RAM memory % used: {psutil.virtual_memory().percent}\nRAM Used (GB): {psutil.virtual_memory().used / 1000000000}"
        show_result(ram_usage)
    elif choice == "2":
        pwk.sendwhatmsg_instantly('+918824610711', 'Hello', 10)
        show_result("WhatsApp message sent!")
    elif choice == "3":
        listen_to_microphone()
    elif choice == "4":
        create_image()
    elif choice == "5":
        face_picture_crop()
    elif choice == "6":
        photo_path = "face.jpg"
        sunglasses_path = "sunglasses.png"
        output_path = "my_photo_with_sunglasses.jpg"
        paste_sunglasses(photo_path, sunglasses_path, output_path)
        show_result("Sunglasses applied to the image.")
    elif choice == "7":
        get_coordinates()
    elif choice == "8":
        search_query = input("Enter What You Want To Search for: ")
        top_5_results = google_search(search_query)
        result_text = f"Top 5 results for '{search_query}':\n"
        for i, result in enumerate(top_5_results, 1):
            result_text += f"{i}. {result}\n"
        show_result(result_text)
    elif choice == "9":
        show_result("Goodbye!")
        return True
    else:
        show_result("Invalid choice. Please try again.")
    return False

def show_result(result_text):
    messagebox.showinfo("Result", result_text)

def listen_to_microphone():
    p = pyaudio.PyAudio()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        show_result("Listening... Say something!")
        try:
            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source, timeout=5)

            recognized_text = recognizer.recognize_google(audio)

            process_text(recognized_text.lower())

        except sr.WaitTimeoutError:
            show_result("No speech detected within the timeout.")
        except sr.UnknownValueError:
            show_result("Could not understand the audio.")
        except sr.RequestError as e:
            show_result("Error with the speech recognition service; {0}".format(e))

    p.terminate()

def process_text(text):
    trigger_word = "execute"

    if trigger_word in text:
        command = text.replace(trigger_word, "").strip()
        show_result(f"Executing command: {command}")
        subprocess.run(command, shell=True)
    else:
        show_result(f"You said: {text}")

def create_image():
    canvas = np.zeros((100, 100, 3), dtype=np.uint8)
    canvas[:, :] = [255, 255, 255]
    canvas[0:33] = [0, 0, 255]
    canvas[33:68] = [255, 255, 255]
    canvas[34:67, 34:67] = [255, 0, 0]
    canvas[68:100] = [0, 255, 0]
    cv2.imshow('hi', canvas)
    cv2.waitKey()
    cv2.destroyAllWindows()

def face_picture_crop():
    pic1 = cv2.imread("using.jpg")
    pic01 = pic1[300:500, 200:650]
    pic2 = cv2.imread("target.jpg")
    pic2[75:400, 80:350] = pic1[75:400, 80:350]
    cv2.imshow("faceCrop", pic2)
    cv2.waitKey()
    cv2.destroyAllWindows()

def paste_sunglasses(photo_path, sunglasses_path, output_path):
    face_width = 2000

    photo = Image.open(photo_path)
    sunglasses = Image.open(sunglasses_path)

    sunglasses_width = face_width // 1
    sunglasses = sunglasses.resize((sunglasses_width, sunglasses_width * sunglasses.height // sunglasses.width))

    paste_x = 1300
    paste_y = 1000

    photo.paste(sunglasses, (paste_x, paste_y), sunglasses)

    photo.save(output_path)

def get_coordinates():
    geolocator = Nominatim(user_agent="GetLoc")
    location = geolocator.geocode("jaipur")
    if location:
        result_text = f"Address: {location.address}\nLatitude = {location.latitude}\nLongitude = {location.longitude}"
        show_result(result_text)
    else:
        show_result("Location not found.")

def google_search(query, num_results=5):
    search_results = search(query, num_results)
    return search_results

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menu")


    def on_button_click():
        user_choice = choice_var.get()
        exit_flag = process_choice(user_choice)

        if exit_flag:
            root.destroy()

    choice_var = tk.StringVar()
    choice_var.set("1")
    tk.Label(root, text=show_menu(), justify=tk.LEFT).pack()
    tk.Entry(root, textvariable=choice_var).pack()
    tk.Button(root, text="Submit", command=on_button_click).pack()

    root.mainloop()