from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
word_dict = {}

try:
    word_dict = pd.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    word_dict = pd.read_csv("data/french_words.csv").to_dict(orient="records")


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_dict)

    canvas.itemconfig(card, image=front_card)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=change_card)


def change_card():
    global current_card
    canvas.itemconfig(card, image=back_card)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def known_word():
    word_dict.remove(current_card)
    pd.DataFrame(word_dict).to_csv("data/words_to_learn.csv", index=False)
    print(len(word_dict))
    new_card()


window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=change_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, font=("Arial", 40, "italic"), fill="black",)
card_word = canvas.create_text(400, 263, font=("Arial", 60, "bold"), fill="black")
canvas.grid(row=0, column=0, columnspan=2)

wrong = PhotoImage(file="images/wrong.png")
false_button = Button(image=wrong, highlightthickness=0, command=new_card)
false_button.grid(row=1, column=0)

correct = PhotoImage(file="images/right.png")
right_button = Button(image=correct, highlightthickness=0, bg=BACKGROUND_COLOR, command=known_word)
right_button.grid(row=1, column=1)

new_card()

window.mainloop()
