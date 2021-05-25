"""
Created 12/03/21 at 13:3 GMT by SignyaLenthiel

Instructions:
Text Editor - Notepad style application that can open, edit, and save
text documents. Optional: Add syntax highlighting and other features.
"""

import PySimpleGUI as sg
import wordcounter as wc

default_font = "JetBrains Mono"

menu_layout: list = [["File", ["Open", "Save", "Save As", "Close", "Exit"]],
                     ["Statistics", ["Word Count"]]]

layout = [[sg.Menu(menu_layout)],
          [sg.Multiline(key="-EDITOR-TEXT-",  size=(222, 55), enable_events=True,
                        metadata=["", False], font=(default_font, ), focus=True,
                        default_text="This is a very simple example of "
                                     "a Notepad-like programme using "
                                     "PySimpleGUI.",
                        pad=(0, 0))]]

window = sg.Window("Text Editor", layout, size=(1600, 900),
                   return_keyboard_events=True)


def save(filepath, content):
    with open(filepath, "w") as file:
        file.write(content)


def save_as(content):
    filepath = sg.popup_get_file("Please choose the file to save to:",
                                 save_as=True)
    save(filepath, content)
    return filepath


def act_on_modified(element):
    if element.metadata[1]:
        if element.metadata[0] in ("", None):
            return save_as(element.get())
        else:
            save(element.metadata[0], element.get())
        return element.metadata[0]
    return ""


# while True:
#     event, values = window.read()
#     print(event)
#     editor = window["-EDITOR-TEXT-"]
#     # Checking if editor has been modified
#     if event == "-EDITOR-TEXT-":
#         editor.metadata[1] = True
#     # User has chosen to exit or
#     # User has chosen to close the current file (not the application)
#     if event in (sg.WIN_CLOSED, "Exit", "q:81", "Close"):
#         if editor.metadata[1]:
#             if editor.metadata[0] in ("", None):
#                 choice = sg.popup_yes_no("Do you want to save the contents?")
#                 if choice == "Yes":
#                     editor.metadata[0] = save_as(editor.get())
#         if event == "Close":
#             editor.update("")
#             editor.metadata[1] = False
#             continue
#         break
#     # User has chosen to open a file
#     # o:79 -> CTRL+O
#     if event in ("Open", "o:79"):
#         editor.metadata[0] = sg.popup_get_file("Please choose the file to open:")
#         if editor.metadata[0] is None:  # User has cancelled
#             continue
#         with open(editor.metadata[0], "r") as file:
#             editor.update(file.read())
#     # User has chosen to save or 'save as' the file
#     # s:83 -> CTRL+S ; S:83 -> ALT+CTRL+S
#     if event in ("Save", "Save As", "s:83", "S:83"):
#         if editor.metadata[0] in ("", None) or event in ("Saves As", "S:83"):
#             editor.metadata = save_as(editor.get())
#         else:
#             save(editor.metadata[0], editor.get())
#         editor.metadata[1] = False
#     # User asked to see the statistics
#     if event == "Word Count":
#         _, counts = wc.word_counter(editor.get())
#         sg.popup(f"Word count:    {counts[1]}\nUnique words: {counts[0]}")
#     # # User is looking for a certain string
#     # # f:70 -> CTRL + F
#     # if event == "f:70":
#     #     sg.popup_get_text("Enter the string to look for:")

while True:
    event, values = window.read()
    print(event)
    editor = window["-EDITOR-TEXT-"]
    # Checking if editor has been modified
    if event == "-EDITOR-TEXT-":
        editor.metadata[1] = True
    # Open
    if event == "Open":
        if editor.get():
            outcome = act_on_modified(editor)
        if outcome is None:
            continue
        filepath = sg.popup_get_file("Chose the file to open:")
        if filepath is None:
            continue
        with open(filepath, "r") as file:
            editor.update(file.read())
            editor.metadata = [filepath, False]
    # Save
    if event == "Save":
        outcome = act_on_modified(editor)
        if outcome is None:
            continue
        editor.metadata = [outcome, False]
    # Save As
    if event == "Save As":
        outcome = save_as(editor.get())
        if outcome is None:
            continue
        editor.metadata = [outcome, False]
    # Close
    if event == "Close":
        act_on_modified(editor)
        editor.metadata = ["", False]
    # Exit
    if event in ("Exit", None):
        act_on_modified(editor)
        break
