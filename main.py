from tkinter import *
from tkinter import messagebox
import random
import clipboard
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def search():
    website_to_search = w_entry.get().lower()
    try:
        with open('data.json', mode='r') as data_file:
            try:
                data = json.load(data_file)
                email = data[website_to_search]['email']
                password = data[website_to_search]['password']
            except KeyError:
                messagebox.showinfo("Error", f"No details for {website_to_search} Found!")
            else:
                messagebox.showinfo(website_to_search, f"Email: {email}\nPassword: {password}")
    except FileNotFoundError:
        messagebox.showinfo("Error", "No Data File Found!")


def generate_password():
    password_letters = [random.choice(letters) for _ in range(10)]
    password_symbols = [random.choice(symbols) for _ in range(4)]
    password_numbers = [random.choice(numbers) for _ in range(4)]

    password = password_letters + password_numbers + password_symbols
    random.shuffle(password)
    generated_password = ''.join(password)
    p_entry.insert(0, generated_password)
    clipboard.copy(generated_password)


def add_data():
    website = w_entry.get().lower()
    email = em_entry.get()
    password = p_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }
    if website != "" or password != "":

        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it okay to save?")

        if is_ok:
            try:
                with open('data.json', mode='r') as data_file:
                    # Load previous data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open('data.json', mode="w") as data_file:
                    # Saved updated Data
                    json.dump(new_data, data_file, indent=4)

            except json.decoder.JSONDecodeError:
                with open('data.json', mode="w") as data_file:
                    # Saved updated Data
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updated old data with new data
                data.update(new_data)

                with open('data.json', mode="w") as data_file:
                    # Saved updated Data
                    json.dump(data, data_file, indent=4)
            finally:
                w_entry.delete(0, END)
                p_entry.delete(0, END)
                w_entry.focus()
    else:
        messagebox.showerror(title="Form", message="You have left some fields empty")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
canvas.grid(column=1, row=0)
logo_img = PhotoImage(file="logo.png")
logo = canvas.create_image(100, 100, image=logo_img)

w_label = Label(text="Website:", bg="white")
w_label.grid(column=0, row=1)

em_label = Label(text="Email/Username:", bg="white")
em_label.grid(column=0, row=2)

p_label = Label(text="Password:", bg="white")
p_label.grid(column=0, row=3)

w_entry = Entry(width=21)
w_entry.focus()
w_entry.grid(column=1, row=1)

em_entry = Entry(width=45)
em_entry.insert(0, 'example@gmail.com')
em_entry.grid(column=1, row=2, columnspan=2)

p_entry = Entry(width=21)
p_entry.grid(column=1, row=3)

search_button = Button(text="Search", command=search)
search_button.grid(column=2,row=1)

gp_button = Button(text="Generate Password", command=generate_password)
gp_button.grid(column=2, row=3)

add_button = Button(text="Add", width=35, command=add_data)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
