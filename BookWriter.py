from pynput.keyboard import Key, Controller
import time
import tkinter.font
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

keyboard = Controller()


def ask_file():
    global file
    file = filedialog.askopenfile(initialdir="/")
    if file is not None:
        file_path_entry.insert(0, file.name)
    file = file.name


def char_width(char):
    character_dots = {
        " ": 3, "!": 1, '"': 3, "'": 1, "(": 3, ")": 3, "*": 3, ",": 1, ".": 1, ":": 1,
        ";": 1, "<": 4, ">": 4, "@": 6, "I": 3, "[": 3, "]": 3, "`": 2, "f": 4, "i": 1,
        "k": 4, "l": 2, "t": 3, "{": 3, "|": 1, "}": 3, "~": 6
    }
    for x in character_dots:
        if char == x:
            return character_dots[char]
    return 5


def color():
    color_codes = {
        "Dark Blue (§1)": "1", "Dark Green (§2)": "2", "Dark Aqua (§3)": "3", "Dark Red (§4)": "4",
        "Dark Purple (§5)": "5", "Gold (§6)": "6", "Gray (§7)": "7", "Dark Gray (8)": "8",
        "Blue (§9)": "9", "Green (§a)": "a", "Aqua (§b)": "b", "Red (§c)": "c", "Light Purple (§d)": "d",
        "Yellow (§e)": "e", "White (§f)": "f"
    }
    color_input = color_combo.get()
    for value in color_codes:
        if value == color_input:
            print(color_codes[value])
            return color_codes[value]
    return ""


def change_page(page, delay):
    if page == "left":
        keyboard.tap(Key.esc)
        time.sleep(delay)
        keyboard.tap(Key.right)
        time.sleep(delay)
        keyboard.tap(Key.enter)
        time.sleep(delay)
        return "right"
    elif page == "right":
        keyboard.tap(Key.esc)
        time.sleep(delay)
        keyboard.tap(Key.right)
        time.sleep(delay)
        keyboard.tap(Key.enter)
        time.sleep(delay)
        keyboard.tap(Key.right)
        time.sleep(delay)
        keyboard.tap(Key.right)
        time.sleep(delay)
        keyboard.tap(Key.enter)
        time.sleep(delay)
        return "left"


def select_page(delay):
    for x in range(4):
        keyboard.tap(Key.down)
        time.sleep(delay)
    keyboard.tap(Key.backspace)
    time.sleep(delay)
    keyboard.tap(Key.esc)
    for x in range(4):
        keyboard.tap(Key.down)
        time.sleep(delay)
        keyboard.tap(Key.backspace)
        time.sleep(delay)


def start():
    if not file == "":
        page_no = 0
        delay = 1
        page = "left"
        line = 1
        page_characters = 0
        word_pixel_width = 0
        line_character_pixels = 0
        time.sleep(2)
        text_color = color()
        select_page(delay)
        if text_color != "":
            keyboard.tap("§")
            keyboard.tap(text_color)
        if BoldVar.get():
            keyboard.tap("§")
            keyboard.tap("l")
        if ItalicVar.get():
            keyboard.tap("§")
            keyboard.tap("o")
        if ObfuscatedVar.get():
            keyboard.tap("§")
            keyboard.tap("k")
        with open(file, 'r') as f:
            text = f.read()
            for letters in text:
                pixel_width = char_width(letters)
                time.sleep(0.05)
                line_character_pixels += 1 + pixel_width
                word_pixel_width += 1 + pixel_width
                page_characters += 1
                keyboard.tap(letters)
                if letters == " ":
                    word_pixel_width = 0
                if page_no == 61:
                    keyboard.tap(Key.esc)
                    return 0
                if letters == "\n":
                    line += 1
                    line_character_pixels = 0
                    word_pixel_width = 0
                if line_character_pixels >= 90:
                    if line < 14 and line_character_pixels > 113:
                        line += 1
                        line_character_pixels = word_pixel_width
                    elif line == 14 or page_characters > 250 and letters == " " or page_characters == 255:
                        page = change_page(page, delay)
                        page_characters = 0
                        line = 0
                        page_no += 1
                        if text_color != "":
                            keyboard.tap("§")
                            keyboard.tap(text_color)
                        if BoldVar.get():
                            keyboard.tap("§")
                            keyboard.tap("l")
                        if ItalicVar.get():
                            keyboard.tap("§")
                            keyboard.tap("o")
                        if ObfuscatedVar.get():
                            keyboard.tap("§")
                            keyboard.tap("k")


file = ""
w = Tk()
w.title("Minecraft Book Writer")
w.geometry("400x300+50+50")
icon = PhotoImage(file="book.png")
w.iconphoto(False, icon)
w.resizable(False, False)
file_path_entry = tkinter.Entry(w, relief="groove")
file_path_entry.place(x=10, y=20, width=200, height=25)
browse = Button(w, text='Browse', height=1, command=lambda: ask_file(), relief="groove")
browse.place(x=215, y=20, width=50, height=25)
color_list = [
    "Dark Blue (§1)", "Dark Green (§2)", "Dark Aqua (§3)", "Dark Red (§4)", "Dark Purple (§5)",
    "Gold (§6)", "Gray (§7)", "Dark Gray (§8)", "Blue (§9)", "Green (§a)", "Aqua (§b)", "Red (§c)",
    "Light Purple (§d)", "Yellow (§e)", "White (§f)"
]
color_combo = ttk.Combobox(w, values=color_list)
color_combo.set("Color - Default")
color_combo['state'] = "readonly"
color_combo.place(x=10, y=70, width=150, height=25)
BoldVar = IntVar()
bold_checkbox = ttk.Checkbutton(w, text="Bold Text (§l)", onvalue=1, offvalue=2, variable=BoldVar)
bold_checkbox.place(x=10, y=120)
ItalicVar = IntVar()
italic_checkbox = ttk.Checkbutton(w, text="Italic Text (§o)", onvalue=1, offvalue=2, variable=ItalicVar)
italic_checkbox.place(x=10, y=140)
ObfuscatedVar = IntVar()
obfuscated_checkbox = ttk.Checkbutton(w, text="Obfuscated Text (§k)", onvalue=1, offvalue=2, variable=ObfuscatedVar)
obfuscated_checkbox.place(x=10, y=160)
cancel_button = Button(w, text='Close', height=1, command=lambda: w.destroy(), relief="groove")
cancel_button.place(x=260, y=260, width=65, height=30)
start_button = Button(w, text='Start', height=1, command=lambda: start(), relief="groove")
start_button.place(x=330, y=260, width=60, height=30)
w.mainloop()
