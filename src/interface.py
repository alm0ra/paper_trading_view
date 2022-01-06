# Create main app tkinter frame.
# from src.app import account_value
import config
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Radiobutton, Listbox, Frame, messagebox
from pathlib import Path
from selenium import webdriver

order_type = None

try:
    driver = webdriver.Chrome()
    driver.get("https://www.tradingview.com/#signin")
except Exception as e:
    print('+ Error Involving Chrome Driver + \n')
    print(str(e) + '\n')
    print('Visit: https://github.com/Robswc/tradingview-trainer/wiki/Errors')
    print('Report this error here: https://github.com/Robswc/tradingview-trainer/issues')
    input()
    quit()


class Application(Frame):

    def __init__(self, master=None, bg=config.bg_color):
        super().__init__(master)

        self.entry_image_2 = None
        self.save_report_image = None
        self.next_button_image = None
        self.cal_risk_image = None
        self.short_button_image = None
        self.image_5 = None
        self.long_button_image = None
        self.image_4 = None
        self.image_3 = None
        self.image_2 = None
        self.image_1 = None
        self.canvas = None
        self.limit_price_entry = None
        self.risk_entry = None
        self.order_vol_entry = None
        self.position_box = None
        self.take_profit_entry = None
        self.stop_loss_entry = None

        self.market_radio = None
        self.limit_radio = None

        self.save_report_button = None
        self.play_pause_button = None
        self.next_button = None
        self.cal_risk_button = None
        self.short_button = None
        self.long_button = None

        self.OUTPUT_PATH = None
        self.ASSETS_PATH = None
        self.play_button = True

        self.master = master
        self.master.configure(background=config.bg_color)
        self.pack()
        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("./assets")
        return self.ASSETS_PATH / Path(path)

    def switch_market_mode(self, market_mode):
        if market_mode:
            global order_type
            order_type = 'market'
            self.limit_price_entry.delete(0, 'end')
            self.limit_price_entry.insert(0, "")
            self.limit_price_entry.config(state="disabled")
        else:
            order_type = 'limit'
            self.limit_price_entry.config(state="normal")

    # Switch play pause button to play mode and pause mode
    def switch_button(self):
        # global play_button
        # Determine if on/off
        if self.play_button:
            self.play_pause_button.config(image=self.pause_image)
            self.play_button = False
        else:
            self.play_pause_button.config(image=self.play_image)
            self.play_button = True

    def show_error(self, cause, exception, message):
        """
        A method for showing errors
        :param cause:
        :param exception:
        :param message:
        """
        messagebox.showerror(str(cause), str(str(exception) + '\n' + message))

    def get_price_data(self):
        try:
            self.open_price = float(driver.find_element_by_xpath(config.open_price_xpath).text)
            self.high_price = float(driver.find_element_by_xpath(config.high_price_xpath).text)
            self.low_price = float(driver.find_element_by_xpath(config.low_price_xpath).text)
            self.close_price = float(driver.find_element_by_xpath(config.close_price_xpath).text)
            self.last_price = float(driver.find_element_by_xpath(config.last_price).text)
        except:
            self.show_error('Get data', 'Xpath error', 'failed to get data')

    # Next bar action
    def next_bar_action(self):

        if self.play_button:
            self.switch_button()
        try:
            driver.find_element_by_xpath(config.next_button_xpath).click()
        except:
            self.show_error('Next Bar', 'Xpath error', 'Please report your error')
        self.get_price_data()

        print(self.close_price)

    # Create tkinter widgets.
    def create_widgets(self):

        self.canvas = Canvas(
            bg=config.bg_color,
            height=784,
            width=424,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        """
            Images are Here
        """

        self.image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            162.83984375,
            24.9375,
            image=self.image_1
        )
        self.image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(
            64.0,
            29.0,
            image=self.image_2
        )

        self.image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(
            197.8818359375,
            42.7685546875,
            image=self.image_3
        )

        self.image_4 = PhotoImage(
            file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(
            204.0,
            738.0,
            image=self.image_4
        )

        self.image_5 = PhotoImage(
            file=self.relative_to_assets("image_5.png"))
        self.canvas.create_image(
            212.0,
            769.0,
            image=self.image_5
        )

        """
            Buttons Are Here
        """
        # Long Button

        self.long_button_image = PhotoImage(
            file=self.relative_to_assets("button_1.png"))

        self.long_button = Button(
            image=self.long_button_image,
            borderwidth=5,
            highlightthickness=5,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.long_button.place(
            x=46.0,
            y=200.0,
            width=159.0,
            height=62.0
        )
        # Short Button
        self.short_button_image = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.short_button = Button(
            image=self.short_button_image,
            borderwidth=5,
            highlightthickness=5,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.short_button.place(
            x=212.0,
            y=200.0,
            width=159.0,
            height=62.0
        )

        # calculate Risk button

        self.cal_risk_image = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.cal_risk_button = Button(
            image=self.cal_risk_image,
            borderwidth=5,
            highlightthickness=5,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.cal_risk_button.place(
            x=69.0,
            y=534.0,
            width=117.0,
            height=38.0
        )

        # next button

        self.next_button_image = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.next_button = Button(
            image=self.next_button_image,
            borderwidth=5,
            highlightthickness=5,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.next_button.place(
            x=212.0,
            y=133.0,
            width=159.0,
            height=62.0
        )
        # play/pause button
        self.play_image = PhotoImage(
            file=self.relative_to_assets("button_5.png"))

        self.pause_image = PhotoImage(
            file=self.relative_to_assets("Button.png"))

        self.play_pause_button = Button(
            image=self.play_image,
            borderwidth=5,
            highlightthickness=5,
            command=self.switch_button,
            relief="flat"
        )
        self.play_pause_button.pack(pady=50)
        self.play_pause_button.place(
            x=46.0,
            y=133.0,
            width=159.0,
            height=62.0
        )

        # Save Report Button Info
        self.save_report_image = PhotoImage(
            file=self.relative_to_assets("button_8.png"))
        self.save_report_button = Button(
            image=self.save_report_image,
            borderwidth=5,
            highlightthickness=5,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.save_report_button.place(
            x=317.0,
            y=6.0,
            width=107.0,
            height=39.0
        )

        """
            Radio Buttons Are Here
        """
        # Radio Button Limit and Market
        self.limit_radio = Radiobutton(
            text="Limit",
            value="limit",
            command=lambda: self.switch_market_mode(False),
        )
        self.limit_radio.place(
            x=36.0,
            y=295.0,
            width=70.0,
            height=30.0
        )

        self.market_radio = Radiobutton(
            text="Market",
            value="Market",
            command=lambda: self.switch_market_mode(True),
        )
        self.market_radio.place(
            x=124.0,
            y=294.0,
            width=80.0,
            height=30.0
        )

        """
            Entry Are Here
        """

        # stop loss Entry
        self.entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(
            244.0,
            410.0,
            image=self.entry_image_1
        )
        self.stop_loss_entry = Entry(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.stop_loss_entry.place(
            x=128.0,
            y=397.0,
            width=232.0,
            height=24.0
        )

        # take profit Entry
        self.entry_image_2 = PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(
            244.0,
            441.0,
            image=self.entry_image_2
        )
        self.take_profit_entry = Entry(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.take_profit_entry.place(
            x=128.0,
            y=428.0,
            width=232.0,
            height=24.0
        )

        # order Volume Entry
        self.entry_image_3 = PhotoImage(
            file=self.relative_to_assets("entry_3.png"))
        self.canvas.create_image(
            244.0,
            472.0,
            image=self.entry_image_3
        )
        self.order_vol_entry = Entry(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.order_vol_entry.place(
            x=128.0,
            y=459.0,
            width=232.0,
            height=24.0
        )

        # Risk amount Entry
        self.entry_image_4 = PhotoImage(
            file=self.relative_to_assets("entry_4.png"))
        self.canvas.create_image(
            244.0,
            503.0,
            image=self.entry_image_4
        )
        self.risk_entry = Entry(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.risk_entry.place(
            x=128.0,
            y=490.0,
            width=232.0,
            height=24.0
        )

        # limit price entry
        self.entry_image_5 = PhotoImage(
            file=self.relative_to_assets("entry_5.png"))
        self.canvas.create_image(
            244.0,
            379.0,
            image=self.entry_image_5
        )
        self.limit_price_entry = Entry(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.limit_price_entry.place(
            x=128.0,
            y=366.0,
            width=232.0,
            height=24.0
        )

        # position history box
        self.position_box = Listbox(
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.position_box.place(
            x=10.0,
            y=603.0,
            width=405.0,
            height=111.0
        )

        """
            Text Areas Are Here
        """

        self.canvas.create_text(
            36.0,
            71.0,
            anchor="nw",
            text="Initial Balance:",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            144.0,
            71.0,
            anchor="nw",
            text="1500\n",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            144.0,
            88.0,
            anchor="nw",
            text="1875",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            144.0,
            105.0,
            anchor="nw",
            text="+ 25%",
            fill=config.profit_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            36.0,
            88.0,
            anchor="nw",
            text="Total Balance:",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            36.0,
            106.0,
            anchor="nw",
            text="Profit/Loss:",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            30.0,
            493.0,
            anchor="nw",
            text="Risk  %",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )

        self.canvas.create_text(
            135.0,
            327.0,
            anchor="nw",
            text="Order Details ",
            fill=config.textarea_color,
            font=("Viga Regular", 18 * -1)
        )

        self.canvas.create_text(
            200.0,
            534.0,
            anchor="nw",
            text="R:R = 1.8\n",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            200.0,
            549.0,
            anchor="nw",
            text="Vol calculated = 1.8\n",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            18.0,
            586.0,
            anchor="nw",
            text="Position History",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            30.0,
            368.0,
            anchor="nw",
            text="Limit Price",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            31.0,
            401.0,
            anchor="nw",
            text="Stop Loss",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            30.0,
            431.0,
            anchor="nw",
            text="Take Profit",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )

        self.canvas.create_text(
            30.0,
            461.0,
            anchor="nw",
            text="Order Volume",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )


def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    return ASSETS_PATH / Path(path)

# Create tkinter window/app
window = Tk()
window.title('PTV - Paper Trading View (by Ali)')
window["bg"] = config.bg_color
window.attributes('-topmost', True)
window.geometry("424x784")
window.resizable(False, False)
img = PhotoImage(file=relative_to_assets('iconnn.png'))
window.tk.call('wm', 'iconphoto', window._w, img)
app = Application(window)
app['bg'] = config.bg_color
app.configure()
app.mainloop()
