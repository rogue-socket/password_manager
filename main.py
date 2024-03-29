import tkinter as tk
from tkinter import messagebox
import pandas as pd
from os.path import exists
import random
import pyperclip


data_temp_dict = {
    "websites": {},
    "usernames": {},
    "passwords": {}
}


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_password():
    random_password_list = []
    random_password_str = ""
    small_lets = random.randint(3, 5)
    for i in range(small_lets):
        random_password_list.append(chr(random.randint(ord('A'), ord('Z'))))
    for j in range(8 - small_lets):
        random_password_list.append(chr(random.randint(ord('a'), ord('z'))))
    small_lets = random.randint(3, 5)
    for k in range(small_lets):
        random_password_list.append(chr(random.randint(ord('0'), ord('9'))))
    for number in range(8 - small_lets):
        ran = random.choice([[33, 47], [58, 64], [91, 96], [123, 126]])
        random_password_list.append(chr(random.randint(ran[0], ran[1])))
    random.shuffle(random_password_list)
    for elem in random_password_list:
        random_password_str += elem
    # Copies the password generated to the clipboard of the system in use
    pyperclip.copy(random_password_str)
    
    password_entry.delete(0, 'end')
    password_entry.insert(0, random_password_str)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    global data_temp_dict
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()
    print(website, username, password)
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Incomplete Data", message="Please dont leave any of the fields empty")
    else:
        # Confirmation Pop Up
        is_ok = messagebox.askokcancel(title="Confirm Username and Password",
                                       message=f"Website: {website}\nUsername: {username}\nPassword: {password}")

        if is_ok:
            # Save to file
            if exists("data.csv"):
                data_temp = pd.read_csv("data.csv")
                data_temp_dict = data_temp.to_dict()

            data_temp_dict["websites"][len(data_temp_dict["websites"])] = website
            data_temp_dict["usernames"][len(data_temp_dict["usernames"])] = username
            data_temp_dict["passwords"][len(data_temp_dict["passwords"])] = password

            data_frame = pd.DataFrame(data_temp_dict)
            data_frame.to_csv("data.csv", index=False)

            # Clear the text-boxes
            website_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            email_entry.insert(0, "yash.testboi@gmail.com")
            password_entry.delete(0, 'end')

            # Clear the dictionary of data
        data_temp_dict = {
            "websites": {},
            "usernames": {},
            "passwords": {}
        }


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.minsize(width=470, height=300)

# Image
canvas = tk.Canvas(height=200, width=200)
lock = tk.PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=lock)
canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

password_label = tk.Label(text="Password")
password_label.grid(row=3, column=0)

email_label = tk.Label(text="Email/Username")
email_label.grid(row=2, column=0)

# Entry
email_entry = tk.Entry(width=55)
email_entry.insert(0, "yash.testboi@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = tk.Entry(width=36)
password_entry.grid(row=3, column=1)

website_entry = tk.Entry(width=55)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2)

# Buttons
generate_button = tk.Button(text="Generate Password", command=random_password)
generate_button.grid(row=3, column=2)

add_button = tk.Button(text="Add Password", width=47, command=add_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
