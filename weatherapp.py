from tkinter import *
from tkinter import messagebox
import pymysql
import hashlib
import requests
import json
import datetime
from PIL import ImageTk, Image

# Database Configuration
db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="ashish123",
    database="weather_app_db"
)

cursor = db.cursor()

# Create User Table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
)
""")
db.commit()


def hash_password(password):
    # Hash the password before storing it in the database
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    username = username_entry.get()
    password = password_entry.get()

    # Hash the password before storing it
    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        messagebox.showinfo("Registration", "Registration Successful!")
    except pymysql.Error as err:
        messagebox.showerror("Error", f"Error during registration: {err}")
        db.rollback()


def login_user():
    username = username_login.get()
    password = password_login.get()

    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login", "Login Successful!")
        show_weather_app()  # Call the weather app function after successful login
    else:
        messagebox.showerror("Error", "Invalid credentials")


def show_weather_app():
    global root
    root.withdraw()  # Hide the login/registration window


    # ...
    root = Tk()
    root.title("Weather App")
    root.geometry("450x700")
    root['background'] = "white"


    new = ImageTk.PhotoImage(Image.open('logo.gif'))
    panel = Label(root, image=new)
    panel.place(x=0, y=520)


    dt = datetime.datetime.now()
    date = Label(root, text=dt.strftime('%A--'), bg='white', font=("bold", 15))
    date.place(x=5, y=130)
    month = Label(root, text=dt.strftime('%m %B'), bg='white', font=("bold", 15))
    month.place(x=100, y=130)


    hour = Label(root, text=dt.strftime('%I : %M %p'),
                    bg='white', font=("bold", 15))
    hour.place(x=10, y=160)


    if int((dt.strftime('%I'))) >= 8 & int((dt.strftime('%I'))) <= 5:
        img = ImageTk.PhotoImage(Image.open('moon.gif'))
        panel = Label(root, image=img)
        panel.place(x=210, y=200)
    else:
        img = ImageTk.PhotoImage(Image.open('sun.gif'))
        panel = Label(root, image=img)
        panel.place(x=210, y=200)


    city_name = StringVar()
    city_entry = Entry(root, textvariable=city_name, width=45)
    city_entry.grid(row=1, column=0, ipady=10, stick=W+E+N+S)


    def city_name():

        api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q="
                                + city_entry.get() + "&units=metric&appid="+ '01a4311c563183760a2bad439be67ee7')

        api = json.loads(api_request.content)


        y = api['main']
        current_temprature = y['temp']
        humidity = y['humidity']
        tempmin = y['temp_min']
        tempmax = y['temp_max']

        x = api['coord']
        longtitude = x['lon']
        latitude = x['lat']

        z = api['sys']
        country = z['country']
        citi = api['name']


        lable_temp.configure(text=current_temprature)
        lable_humidity.configure(text=humidity)
        max_temp.configure(text=tempmax)
        min_temp.configure(text=tempmin)
        lable_lon.configure(text=longtitude)
        lable_lat.configure(text=latitude)
        lable_country.configure(text=country)
        lable_citi.configure(text=citi)



    city_nameButton = Button(root, text="Search", command=city_name)
    city_nameButton.grid(row=1, column=1, padx=5, stick=W+E+N+S)


        # Country Names and Coordinates
    lable_citi = Label(root, text="...", width=0,
                    bg='white', font=("bold", 15))
    lable_citi.place(x=10, y=63)

    lable_country = Label(root, text="...", width=0,
                        bg='white', font=("bold", 15))
    lable_country.place(x=135, y=63)

    lable_lon = Label(root, text="...", width=0,
                    bg='white', font=("Helvetica", 15))
    lable_lon.place(x=25, y=95)
    lable_lat = Label(root, text="...", width=0,
                    bg='white', font=("Helvetica", 15))
    lable_lat.place(x=95, y=95)

        # Current Temperature

    lable_temp = Label(root, text="...", width=0, bg='white',
                    font=("Helvetica", 110), fg='black')
    lable_temp.place(x=18, y=220)

        # Other temperature details

    humi = Label(root, text="Humidity: ", width=0,
                bg='white', font=("bold", 15))
    humi.place(x=3, y=400)

    lable_humidity = Label(root, text="...", width=0,
                        bg='white', font=("bold", 15))
    lable_humidity.place(x=107, y=400)


    maxi = Label(root, text="Max. Temp.: ", width=0,
                bg='white', font=("bold", 15))
    maxi.place(x=3, y=430)

    max_temp = Label(root, text="...", width=0,
                    bg='white', font=("bold", 15))
    max_temp.place(x=128, y=430)


    mini = Label(root, text="Min. Temp.: ", width=0,
                bg='white', font=("bold", 15))
    mini.place(x=3, y=460)

    min_temp = Label(root, text="...", width=0,
                    bg='white', font=("bold", 15))
    min_temp.place(x=128, y=460)


        # Note
    note = Label(root, text="All temperatures in degree celsius",
                bg='white', font=("italic", 10))
    note.place(x=95, y=495)


    root.mainloop()


# Main Application Window
root = Tk()
root.title("User Authentication")
root.geometry("300x200")

# Registration
Label(root, text="Registration").pack(pady=5)

username_label = Label(root, text="Username:")
username_label.pack()
username_entry = Entry(root)
username_entry.pack()

password_label = Label(root, text="Password:")
password_label.pack()
password_entry = Entry(root, show="*")
password_entry.pack()

register_button = Button(root, text="Register", command=register_user)
register_button.pack(pady=10)

# Login
Label(root, text="Login").pack(pady=5)

username_label_login = Label(root, text="Username:")
username_label_login.pack()
username_login = Entry(root)
username_login.pack()

password_label_login = Label(root, text="Password:")
password_label_login.pack()
password_login = Entry(root, show="*")
password_login.pack()

login_button = Button(root, text="Login", command=login_user)
login_button.pack(pady=10)

root.mainloop()
