# ====================================================================================================================
# /*
# App Name: Basic Universal Translator - The Cunning Linguist
# App URI: https://franklinmedia.com.au/apps/but-the-cunning-linguist/
# Author: Z3r0-K3lv1n
# Author URI: https://franklinmedia.com.au/z3r0-k3lv1n
# Description: The "Cunning Linguist" is a language translation tool that utilizes the OpenAI API and GPT-3 model to
# translate text from English to another language. The user can input the target language and the text to be
# translated through a graphical user interface (GUI) and receive the translation in real-time. The translation can
# also be copied to the clipboard or the input can be reset through the GUI. The app is written in Python and utilizes
# the tkinter library for the GUI and the configparser library to read in the API key from a configuration file.
# Tags: Python, Openai, ChatGPT, Tkinter, Pyperclip
# Version: 1.3.5
# License: Franklin Media Australia Pty Ltd - Private Use Copyright License
# License URI:https://www.franklinmedia.com.au/impressum-credits/website-terms-conditions/private-use-copyright-license/
# The Basic Universal Translator - The Cunning Linguist is privately licensed by Franklin Media Australia Pty Ltd for
# non-commercial use only. This means that you may use the software for personal purposes, but
# you may not distribute, sell, or use it for any business or commercial purpose without the express written permission
# of Franklin Media Australia Pty Ltd.
# By using The Basic Universal Translator - The Cunning Linguist, you agree to be bound by the terms of the Franklin
# Media Australia Pty Ltd - Private Use Copyright License. The full text of this license can be found here.
# Please note that this software is provided "as is" without warranty of any kind, express or implied. Franklin Media
# Australia Pty Ltd shall not be liable for any damages arising from the use of this software.
# If you have any questions or concerns about the license for The Basic Universal Translator - The Cunning Linguist,
# please comment to the Franklin Media Australia programmers through their GitHub Repository.
# */
# ====================================================================================================================

import tkinter as tk
import openai
import pyperclip
import configparser

# Set the model engine and temperature constants
MODEL_ENGINE = "text-davinci-003"
TEMPERATURE = 0.5


def read_api_key(file_path):
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(file_path)

    # Read the API key from the text file
    with open(config["openai"]["api_key_file"], "r") as f:
        api_key = f.read()

    return api_key


# Set the API key for OpenAI using the configuration file
openai.api_key = read_api_key("config.ini")


def translate():
    # Get the languages and the text to translate from the GUI
    source_language = source_language_entry.get()
    target_language = target_language_entry.get()
    text = text_entry.get("1.0", "end")

    # Use GPT-3 to translate the text
    prompt = f"You are a professional translator and speak and write every language known to humankind. Translate " \
             f"the following text from {source_language} to {target_language}: {text}"
    completions = openai.Completion.create(engine=MODEL_ENGINE, prompt=prompt, max_tokens=1024, n=1, stop=None,
                                           temperature=TEMPERATURE)
    translation = completions.choices[0].text

    # Update the label with the translated text
    translation_label.config(text=translation)


def copy_to_clipboard():
    # Get the translated text from the translation label
    translated_text = translation_label.cget("text")

    # Copy the translated text to the clipboard
    pyperclip.copy(translated_text)

    # Display a notification that the text has been copied
    notification_label.config(text="Copied to clipboard!")

    # Set a timer to clear the notification after a certain amount of time
    window.after(3000, lambda: notification_label.config(text=""))


def reset():
    # Clear the language and text entries
    source_language_entry.delete(0, 'end')
    target_language_entry.delete(0, 'end')
    text_entry.delete('1.0', 'end')

    # Clear the translated text and notification
    translation_label.config(text='')
    notification_label.config(text='')


# Create the main window
window = tk.Tk()
window.title("The Cunning Linguist - B.U.T. v1.3.5")

# Create a frame for the language entries
language_frame = tk.Frame(master=window)
language_frame.pack(padx=20, pady=20)

# Create labels and entries for the languages
source_language_label = tk.Label(master=language_frame, text="Source Language: ")
source_language_label.pack(side="left")
source_language_entry = tk.Entry(master=language_frame)
source_language_entry.pack(side="left")

target_language_label = tk.Label(master=language_frame, text="Target Language: ")
target_language_label.pack(side="left")
target_language_entry = tk.Entry(master=language_frame)
target_language_entry.pack(side="right")

# Create a frame for the text entry
text_frame = tk.Frame(master=window)
text_frame.pack(padx=20, pady=20)

# Create a label and text entry for the text
text_label = tk.Label(master=text_frame, text="Input Text")
text_label.pack(side="top")
text_entry = tk.Text(master=text_frame)
text_entry.pack(side="right")

# Create a frame for the translation, copy, and reset buttons
button_frame = tk.Frame(master=window)
button_frame.pack(padx=20, pady=20)

# Create a button to trigger the translation
translate_button = tk.Button(master=button_frame, text="Translate", command=translate)
translate_button.pack(side="left")

# Create a button to copy the translated text to the clipboard
copy_button = tk.Button(master=button_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side="right")

# Create a button to reset the form
reset_button = tk.Button(master=button_frame, text="Reset", command=reset)
reset_button.pack(side="right")

# Create a frame to hold the translated text
translation_frame = tk.Frame(master=window)
translation_frame.pack(padx=20, pady=20)

# Create a label to display the translated text
translation_label = tk.Label(master=translation_frame, text="Translation")
translation_label.pack()

# Create a label to display notifications
notification_label = tk.Label(master=window, text="")
notification_label.pack(padx=20, pady=20)

# Run the main loop
window.mainloop()
