"""
Created 17/03/2021 at 23:45 GMT by grump
"""

import PySimpleGUI as sg
import wordcounter as wc

DEFAULT_TEXT = "Notepad reproduction using PySimpleGUI."
DEFAULT_FONT = "JetBrains Mono"

menu = [["&File", ["&Open (CTRL+O)", "&Save (CTRL+S)", "S&ave As", "&Close (CTRL+Q)", "&Exit (CTRL+W)"]],
        ["&Statistics", ["&Word Count"]]]
layout = [[sg.Menu(menu)],
          [sg.Multiline(default_text=DEFAULT_TEXT,
                        size=(222, 55), font=("Consolas", 11), pad=(0, 0),
                        enable_events=True, focus=True, metadata=["", False],
                        key="-EDITOR-", border_width=0, background_color="White")]]

window = sg.Window("Notepad--", layout, size=(1600, 900),
                   background_color="White", return_keyboard_events=True)


def save(element, text):
    with open(element.metadata[0], "w") as file:
        file.write(text)
        element.metadata[1] = False


def save_as(element, text):
    path = sg.popup_get_file("Choose the name of the file to save as:")
    if path is None:
        return -1
    element.metadata[0] = path
    save(element, text)
    return 0


while True:
    event, values = window.read()
    editor = window["-EDITOR-"]
    print(event)

    if event == "-EDITOR-":  # Might be overzealous but best I've got
        # Multiline has been modified
        editor.metadata[1] = True

    if event in ("Exit (CTRL+W)", "w:87", None):
        break

    if event in ("Open (CTRL+O)", "o:79", "Close (CTRL+Q)", "q:81"):
        # Is there currently a file in use?
        if editor.metadata[1]:
            # If yes, does the user wish to save the current progress?
            save_choice = sg.popup_yes_no("Do you wish to save the current file?")
            if save_choice == "Yes":
                # If yes, do we know the filepath?
                if editor.metadata[0]:
                    # If yes, save to the file
                    save(editor, editor.get())
                else:
                    # If no, ask for the filepath then save to it
                    exit_code = save_as(editor, editor.get())
                    if exit_code == -1:
                        # User chose to cancel 'save as'
                        continue
        if event in ("Open (CTRL+O)", "o:79"):
            # Ask the user for the filepath to open
            path = sg.popup_get_file("Choose the file to open:")
            if path is None:
                # User has closed the pop-up (i.e. cancel operation)
                continue
            # Open it
            with open(path, "r") as file:
                editor.metadata = [path, False]
                editor.update(file.read())
        else:
            editor.metadata = ["", False]
            editor.update("")

    if event in ("Save (CTRL+S)", "s:83"):
        if editor.metadata[0]:
            save(editor, editor.get())
        else:
            save_as(editor, editor.get())

    if event == "Save As":
        save_as(editor, editor.get())

    if event == "Word Count":
        _, counts = wc.word_counter(editor.get())
        col1 = sg.Column([[sg.Text("Word Count")],
                          [sg.Text("Unique Words")]])
        col2 = sg.Column([[sg.Text(counts[1])],
                          [sg.Text(counts[0])]])
        wc_window = sg.Window("Word Counts", layout=[[col1, col2]],
                              auto_size_text=True)
        while True:
            event, _ = wc_window.read()
            if event in ("Exit", None):
                break
