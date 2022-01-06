from sys import platform
from selenium import webdriver

from src.app_interface import Application
import tkinter as tk
import locale
import os.path
import config

# Set formatting for currency.
if platform == "win32":
    # Windows formatting
    locale.setlocale(locale.LC_ALL, 'English_United States.1252')
else:
    # Linux/OS X formatting
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


account_value = float(config.initial_amount)

# Check if csv file already exists, if not create it.
if not os.path.exists("output/trade_report.csv"):
    trades_file = open("output/trade_report.csv", "w")
    with open("output/trade_report.csv", "w") as file:
        pass


try:
    driver = webdriver.Chrome()
    driver.get(config.signin_url)
except Exception as e:
    print('+ Error Involving Chrome Driver + \n')
    print(str(e) + '\n')
    quit()



# Create tkinter window/app
root = tk.Tk()
root.title('paper trading view by Xibalbas')
root["bg"] = "#1E1E1E"
root.attributes('-topmost', True)
root.geometry("300x500+0+0")
app = Application(root)
app['bg'] = config.background_color
app.configure()
app.mainloop()
