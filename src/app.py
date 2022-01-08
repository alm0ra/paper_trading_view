# Create main app tkinter frame.
# from src.app import account_value
import config
from tkinter import *
from tkinter import ttk
from pathlib import Path
from tkinter import StringVar, messagebox
from selenium import webdriver
from TradeCenter import TradeEngine
from threading import Thread
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

order_type = None
process1 = None

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.tradingview.com/#signin")
    global action, action1
    action = ActionChains(driver)
    action.key_down(Keys.SHIFT)
    action.send_keys(Keys.DOWN)
    action.key_up(Keys.SHIFT)

    action1 = ActionChains(driver)
    action1.key_down(Keys.SHIFT)
    action1.send_keys(Keys.RIGHT)
    action1.key_up(Keys.SHIFT)

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
        self.low_price = None
        self.high_price = None
        self.open_positions_view = None
        self.open_positions_windows = None
        self.open_orders_windows = None
        self.trade_history_view = None
        self.trade_history_windows = None
        self.open_orders_view = None
        self.engine = TradeEngine()
        self.initial_account = 1000
        self.final_account = self.initial_account
        self.commission = 0
        self.symbol = "BTC/USDT"
        # TODO add symbol
        self.close_price = 57500
        self.first_time = True
        self.status = None
        self.p1 = None
        # self.loop = asyncio.get_event_loop()
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
        self.calculate_profit_loss()

    def relative_to_assets(self, path: str) -> Path:
        """
            it prepares file location in assets
        """
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("./assets")
        return self.ASSETS_PATH / Path(path)

    def switch_market_mode(self, market_mode):
        """
            a switch between market mode and Limit mode
        """
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
        global action
        action.perform()

        # Determine if on/off
        if self.play_button:
            try:
                # driver.find_element_by_xpath(config.play_pause_button_xpath).click()
                # button is playing
                self.play_pause_button.config(image=self.pause_image)
                self.play_button = False
                self.status = True
                # start a thread for getting price
                process1 = Thread(target=self.get_price_while_play)
                process1.start()
            except:
                self.show_error('Play Button', 'Xpath Error', 'failed to find')
        else:
            # button is paused
            try:
                # driver.find_element_by_xpath(config.play_pause_button_xpath).click()
                self.play_pause_button.config(image=self.play_image)
                self.play_button = True
                self.status = False
            except:
                self.show_error('Play Button', 'Xpath Error', 'failed to find')

    def show_error(self, cause, exception, message):
        """
            A method for showing errors
        """
        messagebox.showerror(str(cause), str(str(exception) + '\n' + message))

    def show_message(self, title, message):
        """
            A method for showing message
        """
        messagebox.showinfo(title=title, message=message)

    def balance_checker(self):
        self.final_account = self.engine.calculate_account_loss_profit(self.initial_account)

    # get data from candles
    def get_price_data(self):
        """
        A method for get price data from trading view
        """
        # try:

        self.open_price = float(driver.find_element_by_xpath(config.open_price_xpath).text)
        self.high_price = float(driver.find_element_by_xpath(config.high_price_xpath).text)
        self.low_price = float(driver.find_element_by_xpath(config.low_price_xpath).text)
        self.close_price = float(driver.find_element_by_xpath(config.close_price_xpath).text)
        self.symbol = str(driver.find_element_by_xpath(config.symbol_xpath).text)
        self.last_price = self.close_price
        self.engine.check_orders(low=self.low_price, high=self.high_price, close=self.close_price)
        self.engine.check_positions(low=self.low_price, high=self.high_price, close=self.close_price)
        if self.open_orders_view:
            self.show_open_order_history()
        if self.open_positions_view:
            self.show_open_position_history()
        if self.trade_history_view:
            self.show_trade_history()

        self.calculate_profit_loss()

        print(self.close_price)
        return True
        # except:
        #     self.show_error('Get data', 'Xpath error', 'failed to get data ')
        #     return False


    # action for play button while chart is playing
    def get_price_while_play(self):
        while True:
            sleep(0.09)
            out = self.get_price_data()
            if not self.status :
                break
            # if not out:
            #     # self.play_pause_button.config(image=self.play_image)
            #     # self.play_button = True
            #     # self.status = False
            #     break

    # Next bar action
    def next_bar_action(self):
        global action1

        if not self.play_button:
            self.switch_button()

        # try:
        action1.perform()
        self.get_price_data()
        # except:
        #     self.show_error('Next Bar', 'Xpath error', 'Please report your error')


    # Risk calculate Action
    def risk_action(self):
        global order_type
        sl = self.stop_loss_entry.get()
        tp = self.take_profit_entry.get()
        risk = self.risk_entry.get()

        # market order
        if order_type == "market":
            enter_price = self.close_price

            # Check inputs
            if not sl or not tp or not risk:
                self.show_error('Input', 'Empty items', 'Stop loss or Take profit or Risk must not be Empty')
            try:
                sl=float(sl)
                tp=float(tp)
                risk=float(risk)
            except ValueError:
                self.show_error('Value Error', 'Invalid Value amount', 'Stop loss or Take profit or Risk must not be Numbers')

            # calculate R:R and Volume
            if tp > enter_price > sl:
                # Long Position
                r_r = round((tp-enter_price) / (enter_price - sl), 2)
                volume = round(self.final_account * risk / ((enter_price-sl) / enter_price * 100),2)
                print(r_r)
                print(volume)
                self.r_r.config(text=r_r)
                self.volume_calculated.config(text=str(volume))
                self.order_vol_entry.delete(0, 'end')
                self.order_vol_entry.insert(0, str(volume))

            elif tp < enter_price < sl:
                # Short Position
                r_r = round((enter_price - tp) / (sl - enter_price), 2)
                volume = round(self.final_account * risk / ((sl-enter_price) / enter_price * 100),2)
                self.r_r.config(text=r_r)
                self.volume_calculated.config(text=str(volume))
                self.order_vol_entry.delete(0, 'end')
                self.order_vol_entry.insert(0, str(volume))
            else:
                self.show_error('sl , tp error ', 'Invalid', 'Check your Sl , Tp with Market Price')

        # Limit order
        else:
            limit_entry = self.limit_price_entry.get()

            # Check inputs
            if not sl or not tp or not limit_entry or not risk:
                self.show_error('Input', 'Empty items', 'limit_entry , Stop loss and Take profit must not be Empty')
            try:
                sl=float(sl)
                tp=float(tp)
                limit_entry=float(limit_entry)
                risk=float(risk)
            except ValueError:
                self.show_error('Value Error', 'Invalid Value amount', 'limit_entry, Stop loss and Take profit must not be Numbers')

            # calculate R:R and Volume
            if tp > limit_entry > sl:
                # Long Position
                r_r = round((tp-limit_entry) / (limit_entry - sl), 2)
                volume = round(self.final_account * risk / ((limit_entry-sl) / limit_entry * 100),2)
                print(r_r)
                print(volume)
                self.r_r.config(text=r_r)
                self.volume_calculated.config(text=str(volume))
                self.order_vol_entry.delete(0, 'end')
                self.order_vol_entry.insert(0, str(volume))

            elif tp < limit_entry < sl:
                # Short Position
                r_r = round((limit_entry - tp) / (sl - limit_entry), 2)
                volume = round(self.final_account * risk / ((sl-limit_entry) / limit_entry * 100),2)
                self.r_r.config(text=r_r)
                self.volume_calculated.config(text=str(volume))
                self.order_vol_entry.delete(0, 'end')
                self.order_vol_entry.insert(0, str(volume))

            else:
                self.show_error('sl , tp error ', 'Invalid', 'Check your Sl , Tp with limit_entry Price')

    def calculate_profit_loss(self):
        self.balance_checker()

        profit_loss = round((self.final_account - self.initial_account) / self.initial_account * 100, 2)

        if profit_loss > 0:
            self.profit_loss_baalance.config(text=str(profit_loss)+ "%", bg = "green")
        elif profit_loss < 0:
            self.profit_loss_baalance.config(text=str(profit_loss)+ "%", bg = "red")
        elif profit_loss == 0 :
            self.profit_loss_baalance.config(text=str(profit_loss) + "%", bg="#FFFFFF")

        self.commission_show.config(text=str(self.commission) + " %")
        self.initial_balance.config(text=str(self.initial_account) + " $")
        self.total_balance.config(text=str(self.final_account) + " $")


    def setting_action(self):
        top = Toplevel()
        top.title('PTV - Setting')
        top["bg"] = config.bg_color
        top.attributes('-topmost', True)
        top.geometry("500x200")
        top.resizable(False, False)
        img = PhotoImage(file=relative_to_assets('iconnn.png'))
        top.tk.call('wm', 'iconphoto', window._w, img)

        def submit_action():
            print("ok")
            self.initial_account = float(self.account_entry.get())
            self.commission = float(self.account_commission.get())
            self.commission_show.config(text=str(self.commission)+" %")
            self.final_account = self.initial_account
            self.initial_balance.config(text=str(self.initial_account) + " $")
            self.total_balance.config(text=str(self.final_account) + " $")
            self.calculate_profit_loss()
            top.destroy()

        submit = Button(
            top,
            borderwidth=5,
            highlightthickness=5,
            text="submit",
            command=submit_action,
            relief="flat"
        )
        submit.place(
            x=180.0,
            y=120.0,
            width=159.0,
            height=62.0
        )

        self.account_entry = Entry(
            top,
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.account_entry.place(
            x=210.0,
            y=60.0,
            width=232.0,
            height=30.0
        )

        self.text1 = Label(
            top,
            text='Initial Money Amount:',
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.text1.place(
            x=5.0,
            y=60.0,
        )
        self.account_commission = Entry(
            top,
            bd=0,
            bg=config.entry_bg_color,
            highlightthickness=0
        )
        self.account_commission.place(
            x=210.0,
            y=20.0,
            width=232.0,
            height=30.0
        )

        self.text2 = Label(
            top,
            text='commission per trade %:',
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.text2.place(
            x=5.0,
            y=20.0,
        )

    def entry_checker(self, side):
        global order_type
        sl = self.stop_loss_entry.get()
        tp = self.take_profit_entry.get()
        order_vol = self.order_vol_entry.get()
        if order_type == "market":
            entry_price = self.close_price
        else:
            entry_price = self.limit_price_entry.get()
        if sl and tp and order_vol and entry_price:
            try:
                sl = float(sl)
                tp = float(tp)
                order_vol = float(order_vol)
                entry_price = float(entry_price)
            except ValueError:
                self.show_error('Value Error', 'Invalid Value amount',
                                'limit_entry, Stop loss and Take profit must not be Numbers')
                return False
            if side == 'long':
                if sl < entry_price < tp:
                    return True
                else:
                    self.show_error('Error', 'SL, Tp', ' you put invalid stop loss and take profit')
                    return False
            if side == 'short':
                if sl > entry_price > tp:
                    return True
                else:
                    self.show_error('Error', 'SL, Tp', ' you put invalid stop loss and take profit')
                    return False
        else:
            return False

    def clear_entry(self):
        self.limit_price_entry.delete(0, 'end')
        self.limit_price_entry.insert(0, '')
        self.stop_loss_entry.delete(0, 'end')
        self.stop_loss_entry.insert(0, '')
        self.take_profit_entry.delete(0, 'end')
        self.take_profit_entry.insert(0, '')
        self.order_vol_entry.delete(0, 'end')
        self.order_vol_entry.insert(0, '')
        self.risk_entry.delete(0, 'end')
        self.risk_entry.insert(0, '')

    def send_order(self, side):

        if self.entry_checker(side):

            sl = float(self.stop_loss_entry.get())
            tp = float(self.take_profit_entry.get())
            order_vol = float(self.order_vol_entry.get())

            if order_type == "market":
                entry_price = float(self.close_price)
                self.engine.place_market_order(symbol=self.symbol, entry_price=entry_price, sl=sl, tp=tp, volume=order_vol,
                          commission=self.commission, side=side)
                if self.open_positions_view:
                    self.show_open_position_history()


            else:
                entry_price = float(self.limit_price_entry.get())
                self.engine.place_limit_order(symbol=self.symbol, entry_price=entry_price, sl=sl, tp=tp, volume=order_vol,
                          commission=self.commission, side=side)
                if self.open_orders_view:
                    self.show_open_order_history()

            # self.clear_entry()

            self.show_message(title="success", message="order submitted successfully")

    def save_report_action(self):
        if self.engine.trade_list:
            self.engine.save_trade_report()
            # show message that saved
            self.show_message(title="success", message="report was save into ./output/trade_report.csv")
        else:
            # show message there is no trade yet
            self.show_message(title="Notice", message="there is no Trade yet ")
    def restart_action(self):
        self.engine.clean_all()
        self.final_account = 1000
        self.initial_account = 1000
        self.commission = 0
        self.calculate_profit_loss()
        if self.open_orders_view:
            self.show_open_order_history()
        if self.open_positions_view:
            self.show_open_position_history()
        if self.trade_history_view:
            self.show_trade_history()
        self.clear_entry()

    def close_all_pos_action(self):
        if self.engine.open_positions:
            self.engine.close_all_positions(self.close_price)
            self.show_message(title="Done", message=f"all open positions closed at price {self.close_price}")
            self.show_trade_history()

            if self.open_positions_view:
                self.show_open_position_history()

        else:
            self.show_message(title="info", message="you don't have any open position")

    def cancel_all_open_orders_action(self):
        self.engine.clean_all_orders()
        if self.open_orders_view:
            self.show_open_order_history()
        self.show_message(title="Done", message="all open orders canceled")

    # def calculate_final_account(self):
    #     self.final_account = self.engine.calculate_account_loss_profit(self.final_account)

    def show_trade_history(self):
        count = 0
        self.trade_history_view.delete(*self.trade_history_view.get_children())
        for trade in self.engine.trade_list:
            self.trade_history_view.insert(parent='',
                                           index='end',
                                           iid=count,
                                           text="",
                                           values=(
                                                trade["symbol"],
                                                trade["side"],
                                                trade["enter_price"],
                                                trade["stop_loss"],
                                                trade["take_profit"],
                                                trade["volume"],
                                                trade["close_price"],
                                                trade["trade_status"],
                                                trade["realized_profit_loss"],
                                                trade["realized_profit_loss_percent"],
                                                trade["order_type"],
                                            ))
            count += 1

    def show_open_order_history(self):
        count = 0
        self.open_orders_view.delete(*self.open_orders_view.get_children())
        for order in self.engine.open_orders:
            self.open_orders_view.insert(parent='',
                                           index='end',
                                           iid=count,
                                           text="",
                                           values=(
                                                order["symbol"],
                                                order["side"],
                                                order["enter_price"],
                                                order["stop_loss"],
                                                order["take_profit"],
                                                order["volume"],
                                                order["order_status"],
                                                order["position_status"],
                                                order["order_type"],
                                            ))
            count +=1

    def show_open_position_history(self):
        count = 0
        self.open_positions_view.delete(*self.open_positions_view.get_children())
        for position in self.engine.open_positions:
            self.open_positions_view.insert(parent='',
                                         index='end',
                                         iid=count,
                                         text="",
                                         values=(
                                             position["symbol"],
                                             position["side"],
                                             position["enter_price"],
                                             position["stop_loss"],
                                             position["take_profit"],
                                             position["volume"],
                                             position["order_status"],
                                             position["position_status"],
                                             position["order_type"],
                                             position["unrealized_profit_loss"],
                                         ))
            count += 1

    def trade_history_action(self):
        self.trade_history_windows = Toplevel()
        self.trade_history_windows.title('PTV - Trade History')
        self.trade_history_windows["bg"] = config.bg_color
        self.trade_history_windows.attributes('-topmost', True)
        self.trade_history_windows.geometry("1100x200")
        self.trade_history_windows.resizable(False, False)
        img = PhotoImage(file=relative_to_assets('iconnn.png'))
        self.trade_history_windows.tk.call('wm', 'iconphoto', window._w, img)
        # frame
        tree_frame = Frame(self.trade_history_windows)
        tree_frame.place(
            x=5,
            y=5,
            width=1090,
            height=190
        )
        # TreeView Scroll Bar
        tree_scrollbar = Scrollbar(tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.trade_history_view = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scrollbar.set,

        )
        self.trade_history_view.place(
            x=5,
            y=5,
            height=190,
            width=1070,
        )
        tree_scrollbar.config(command=self.trade_history_view.yview)
        # format our columns
        self.trade_history_view['columns'] = ("symbol", "side", "EP", "SL", "TP", "Vol", "Close_price", "Trade_status",
                                              "profit/loss", "profit/loss %", "order_type")
        self.trade_history_view.column("#0", anchor=W, width=10)
        self.trade_history_view.column("symbol", anchor=CENTER, width=50)
        self.trade_history_view.column("side", anchor=CENTER, width=50)
        self.trade_history_view.column("EP", anchor=CENTER, width=50)
        self.trade_history_view.column("SL", anchor=CENTER, width=50)
        self.trade_history_view.column("TP", anchor=CENTER, width=50)
        self.trade_history_view.column("Vol", anchor=CENTER, width=50)
        self.trade_history_view.column("Close_price", anchor=CENTER, width=70)
        self.trade_history_view.column("Trade_status", anchor=CENTER, width=75)
        self.trade_history_view.column("profit/loss", anchor=CENTER, width=80)
        self.trade_history_view.column("profit/loss %", anchor=CENTER, width=80)
        self.trade_history_view.column("order_type", anchor=CENTER, width=70)


        # # Create Headings
        self.trade_history_view.heading("#0", anchor=W, text="ID")
        self.trade_history_view.heading("symbol", text="symbol", anchor=CENTER)
        self.trade_history_view.heading("side", text="side", anchor=CENTER)
        self.trade_history_view.heading("EP", text="EP", anchor=CENTER)
        self.trade_history_view.heading("SL", text="SL", anchor=CENTER)
        self.trade_history_view.heading("TP", text="TP", anchor=CENTER)
        self.trade_history_view.heading("Vol",text="Vol", anchor=CENTER)
        self.trade_history_view.heading("Close_price", text="Close_price", anchor=CENTER)
        self.trade_history_view.heading("Trade_status", text="Trade_status", anchor=CENTER)
        self.trade_history_view.heading("profit/loss", text="profit/loss", anchor=CENTER)
        self.trade_history_view.heading("profit/loss %", text="profit/loss %", anchor=CENTER)
        self.trade_history_view.heading("order_type", text="order_type", anchor=CENTER)
        self.show_trade_history()


    def open_orders_action(self):
        self.open_orders_windows = Toplevel()
        self.open_orders_windows.title('PTV - open orders')
        self.open_orders_windows["bg"] = config.bg_color
        self.open_orders_windows.attributes('-topmost', True)
        self.open_orders_windows.geometry("1100x200")
        self.open_orders_windows.resizable(False, False)
        img = PhotoImage(file=relative_to_assets('iconnn.png'))
        self.open_orders_windows.tk.call('wm', 'iconphoto', window._w, img)
        # frame
        tree_frame = Frame(self.open_orders_windows)
        tree_frame.place(
            x=5,
            y=5,
            width=1090,
            height=190
        )
        # TreeView Scroll Bar
        tree_scrollbar = Scrollbar(tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.open_orders_view = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scrollbar.set,

        )
        self.open_orders_view.place(
            x=5,
            y=5,
            height=190,
            width=1070,
        )
        tree_scrollbar.config(command=self.open_orders_view.yview)
        self.open_orders_view['columns'] = ("symbol", "side", "EP", "SL", "TP", "Vol", "order_status", "position_status",
                                            "order_type")
        self.open_orders_view.column("#0", anchor=W, width=10)
        self.open_orders_view.column("side", anchor=CENTER, width=50)
        self.open_orders_view.column("symbol", anchor=CENTER, width=50)
        self.open_orders_view.column("EP", anchor=CENTER, width=50)
        self.open_orders_view.column("SL", anchor=CENTER, width=50)
        self.open_orders_view.column("TP", anchor=CENTER, width=50)
        self.open_orders_view.column("Vol", anchor=CENTER, width=50)
        self.open_orders_view.column("order_status", anchor=CENTER, width=70)
        self.open_orders_view.column("position_status", anchor=CENTER, width=75)
        self.open_orders_view.column("order_type", anchor=CENTER, width=70)


        # # Create Headings
        self.open_orders_view.heading("#0", anchor=W, text="ID")
        self.open_orders_view.heading("symbol", text="symbol", anchor=CENTER)
        self.open_orders_view.heading("side", text="side", anchor=CENTER)
        self.open_orders_view.heading("EP", text="EP", anchor=CENTER)
        self.open_orders_view.heading("SL", text="SL", anchor=CENTER)
        self.open_orders_view.heading("TP", text="TP", anchor=CENTER)
        self.open_orders_view.heading("Vol",text="Vol", anchor=CENTER)
        self.open_orders_view.heading("order_status", text="order_status", anchor=CENTER)
        self.open_orders_view.heading("position_status", text="position_status", anchor=CENTER)
        self.open_orders_view.heading("order_type", text="order_type", anchor=CENTER)
        self.show_open_order_history()

    def open_positions_actions(self):
        self.open_positions_windows = Toplevel()
        self.open_positions_windows.title('PTV - open positions')
        self.open_positions_windows["bg"] = config.bg_color
        self.open_positions_windows.attributes('-topmost', True)
        self.open_positions_windows.geometry("1100x200")
        self.open_positions_windows.resizable(False, False)
        img = PhotoImage(file=relative_to_assets('iconnn.png'))
        self.open_positions_windows.tk.call('wm', 'iconphoto', window._w, img)

        # frame
        tree_frame = Frame(self.open_positions_windows)
        tree_frame.place(
            x=5,
            y=5,
            width=1090,
            height=190
        )
        # TreeView Scroll Bar
        tree_scrollbar = Scrollbar(tree_frame)
        tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.open_positions_view = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scrollbar.set,

        )
        self.open_positions_view.place(
            x=5,
            y=5,
            height=190,
            width=1070,
        )
        tree_scrollbar.config(command=self.open_positions_view.yview)
        self.open_positions_view['columns'] = ("symbol","side", "EP", "SL", "TP", "Vol", "order_status", "position_status",
                                            "order_type", "unrealized_pnl_p")
        self.open_positions_view.column("#0", anchor=W, width=10)
        self.open_positions_view.column("symbol", anchor=CENTER, width=50)
        self.open_positions_view.column("side", anchor=CENTER, width=50)
        self.open_positions_view.column("EP", anchor=CENTER, width=50)
        self.open_positions_view.column("SL", anchor=CENTER, width=50)
        self.open_positions_view.column("TP", anchor=CENTER, width=50)
        self.open_positions_view.column("Vol", anchor=CENTER, width=50)
        self.open_positions_view.column("order_status", anchor=CENTER, width=70)
        self.open_positions_view.column("position_status", anchor=CENTER, width=75)
        self.open_positions_view.column("order_type", anchor=CENTER, width=70)
        self.open_positions_view.column("unrealized_pnl_p", anchor=CENTER, width=80)


        # # Create Headings
        self.open_positions_view.heading("#0", anchor=W, text="ID")
        self.open_positions_view.heading("symbol", text="symbol", anchor=CENTER)
        self.open_positions_view.heading("side", text="side", anchor=CENTER)
        self.open_positions_view.heading("EP", text="EP", anchor=CENTER)
        self.open_positions_view.heading("SL", text="SL", anchor=CENTER)
        self.open_positions_view.heading("TP", text="TP", anchor=CENTER)
        self.open_positions_view.heading("Vol",text="Vol", anchor=CENTER)
        self.open_positions_view.heading("order_status", text="order_status", anchor=CENTER)
        self.open_positions_view.heading("position_status", text="position_status", anchor=CENTER)
        self.open_positions_view.heading("order_type", text="order_type", anchor=CENTER)
        self.open_positions_view.heading("unrealized_pnl_p", text="unreal pnl %", anchor=CENTER)
        self.show_open_position_history()



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
            command=lambda: self.send_order('long'),
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
            command=lambda: self.send_order('short'),
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
            command=self.risk_action,
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
            command=self.next_bar_action,
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
            command=self.save_report_action,
            relief="flat"
        )
        self.save_report_button.place(
            x=317.0,
            y=6.0,
            width=107.0,
            height=39.0
        )

        self.setting_button_image = PhotoImage(
            file=self.relative_to_assets("Button11.png"))
        self.setting_button= Button(
            image=self.setting_button_image,
            borderwidth=5,
            highlightthickness=5,
            command=self.setting_action,
            relief="flat"
        )
        self.setting_button.place(
            x=317.0,
            y=50.0,
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


        self.open_orders_button= Button(
            text="Open Orders",
            borderwidth=5,
            highlightthickness=5,
            command=self.open_orders_action,
            relief="flat"
        )
        self.open_orders_button.place(
            x=10.0,
            y=603.0,
            width=107.0,
            height=39.0
        )

        self.open_positions_button= Button(
            text="Open Positions",
            borderwidth=5,
            highlightthickness=5,
            command=self.open_positions_actions,
            relief="flat"
        )
        self.open_positions_button.place(
            x=10.0,
            y=650.0,
            width=107.0,
            height=39.0
        )

        self.trade_history_button= Button(
            text="Trade History",
            borderwidth=5,
            highlightthickness=5,
            command=self.trade_history_action,
            relief="flat"
        )
        self.trade_history_button.place(
            x=10.0,
            y=700.0,
            width=107.0,
            height=39.0
        )

        self.clear_all_orders_button= Button(
            text="cancel open orders",
            borderwidth=5,
            highlightthickness=5,
            command=self.cancel_all_open_orders_action,
            relief="flat"
        )
        self.clear_all_orders_button.place(
            x=250.0,
            y=603.0,
            width=150.0,
            height=39.0
        )
        self.close_all_positions= Button(
            text="close all positions",
            borderwidth=5,
            highlightthickness=5,
            command=self.close_all_pos_action,
            relief="flat"
        )
        self.close_all_positions.place(
            x=250.0,
            y=650.0,
            width=150.0,
            height=39.0
        )
        self.restart_button= Button(
            text="Restart",
            borderwidth=5,
            highlightthickness=5,
            command=self.restart_action,
            relief="flat"
        )
        self.restart_button.place(
            x=250.0,
            y=700.0,
            width=150.0,
            height=39.0
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
            250.0,
            106.0,
            anchor="nw",
            text="commission:",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 13 * -1)
        )
        self.commission_show = Label(
            text=str(self.commission) + " %",
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.commission_show.place(
            x=340.0,
            y=106.0,
        )
        self.total_balance = Label(
            text=str(self.final_account) + " $",
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.total_balance.place(
            x=144.0,
            y=88.0,
        )

        self.initial_balance = Label(
            text=str(self.initial_account) + " $",
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.initial_balance.place(
            x=144.0,
            y=71.0,
        )

        self.profit_loss_baalance = Label(
            text="0 %",
            bg="green",
            font=("Ubuntu Regular", 14 * -1)
        )
        self.profit_loss_baalance.place(
            x=144.0,
            y=105.0,
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
            text="R:R =\n",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )
        self.r_r = Label(
            text='None',
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.r_r.place(
            x=275.0,
            y=534.0,
        )

        self.canvas.create_text(
            200.0,
            549.0,
            anchor="nw",
            text="Volume = \n",
            fill=config.textarea_color,
            font=("Ubuntu Regular", 14 * -1)
        )
        self.volume_calculated = Label(
            text='None',
            font=("Ubuntu Regular", 14 * -1),
            bg="#FFFFFF"
        )
        self.volume_calculated.place(
            x=275.0,
            y=549.0,
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
