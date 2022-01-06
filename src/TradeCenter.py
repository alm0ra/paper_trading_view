import pandas as pd


class TradeEngine:

    def __init__(self) -> None:
        self.open_orders = []
        self.open_positions = []
        self.trade_list = []

        self.close_price = None
        self.high_price = None
        self.low_price = None
        self.csv_template = None

    def save_trade_report(self):
        """
            Get all Trade and save them in a Csv file
        """
        self.csv_template = pd.DataFrame(
            columns=['symbol', 'order_status', 'position_status', 'side', 'enter_price',
                     'stop_loss', 'take_profit', 'volume', 'commission', 'unrealized_profit_loss',
                     'realized_profit_loss', 'close_price', 'trade_status',
                     'realized_profit_loss_percent', 'final_volume'])
        for trade in self.trade_list:
            self.csv_template = self.csv_template.append(trade, ignore_index=True)

        self.csv_template.to_csv('./out.csv')

    def clean_all(self):
        """
            clean all Open orders / open positions / trade history
        """
        self.open_orders = []
        self.open_positions = []
        self.trade_list = []

    def clean_all_orders(self):
        """
            clean all open orders
        """
        self.open_orders = []

    def check_orders(self, high, low):
        """
            Check all Limit orders with every candle and if executed it wil be known as a position
        """

        for order in self.open_orders:

            if order["order_status"] != "BadOrdering(10001)":

                enter_price = float(order["enter_price"])
                side = order["side"]

                if order["order_type"] == "limit":
                    if low <= enter_price <= high:
                        self.execute_limit_order(order)

                    if side == "long":
                        if low < enter_price:
                            order["order_status"] = "BadOrdering(10001)"
                    if side == "short":
                        if high > enter_price:
                            order["order_status"] = "BadOrdering(10001)"

    def check_positions(self, high, low):
        """
            Check all open positions with every candle and if closed it wil be known as a Trade in Trade History
        """
        for position in self.open_positions:
            sl = float(position["stop_loss"])
            tp = float(position["take_profit"])
            side = position["side"]

            if side == "long":

                if low <= sl <= high or low < sl:
                    self.close_position(position=position, closed_price=sl)
                if low <= tp <= high or high > tp:
                    self.close_position(position=position, closed_price=tp)

            if side == "short":

                if low <= sl <= high or high > sl:
                    self.close_position(position=position, closed_price=sl)
                if low <= tp <= high or low < tp:
                    self.close_position(position=position, closed_price=tp)

    def place_market_order(self, symbol: str, entry_price: float, sl: float, tp: float, volume: float,
                           commission: float, side: str) -> None:
        """
        it uses for placing a market order (this order will be executed at entry price,
        entry price is close price of current candle)
        """
        position = {
            "symbol": f"{symbol}",
            "order_status": "executed",
            "position_status": "open",
            "order_type": "market",
            "side": f"{side}",
            "enter_price": f"{entry_price}",
            "stop_loss": f"{sl}",
            "take_profit": f"{tp}",
            "volume": f"{volume}",
            "commission": f"{commission}",
            "unrealized_profit_loss": "",
            "realized_profit_loss": "",
            "close_price": "",
            "trade_status": "",  # sl_hit, tp_hit, closed
            "realized_profit_loss_percent": "",
            "final_volume": "",
        }

        self.open_positions.append(position)

    def place_limit_order(self, symbol: str, entry_price: float, sl: float, tp: float, volume: float,
                          commission: float, side: str):
        """
            it uses for placing a Limit Order (this order will be executed when price arrived to entry price)
            Notice1 : BadOrdering(10001)
                    it's status of order that we can't execute them because they are not Limit order anymore
                    Limit Order side Long:
                        Bad Condition:
                            current price < Enter price
                        if price is under enter price we can't execute this order, and we know this as bad order

                    Limit Order side short:
                        Bad Condition:
                            current price > Enter price
                        if price is upper enter price we can't execute this order, and we know this as bad order

        """
        order = {
            "symbol": f"{symbol}",
            "order_status": "open",
            "position_status": "NotExecuted",
            "order_type": "limit",
            "side": f"{side}",
            "enter_price": f"{entry_price}",
            "stop_loss": f"{sl}",
            "take_profit": f"{tp}",
            "volume": f"{volume}",
            "commission": f"{commission}",
            "unrealized_profit_loss": "",
            "realized_profit_loss": "",
            "close_price": "",
            "trade_status": "",  # sl_hit, tp_hit, closed
            "realized_profit_loss_percent": "",
            "final_volume": "",
        }
        self.open_orders.append(order)

    def execute_limit_order(self, order):
        """
            it uses for executing limit orders (it changes an order to position)
        """
        # remove from open orders
        if order["order_status"] != "BadOrdering(10001)":
            self.open_orders.remove(order)

            order["order_status"] = "executed"
            order["position_status"] = "open"
            # add to open positions
            self.open_positions.append(order)

    def calculate_account_loss_profit(self, account_balance):
        """
            Get all Trade and add profits or losses to account balance
        """
        for trade in self.trade_list:
            account_balance += float(trade["realized_profit_loss"])

        return account_balance

    def close_all_positions(self, closed_price):
        """
            Get all open positions and close them
        """
        for position in self.open_positions:
            self.close_position(position=position, closed_price=closed_price)

    def close_position(self, position, closed_price):
        """
            closing open position and write into trade history .
        """
        self.open_positions.remove(position)
        position["position_status"] = "closed"
        position["close_price"] = closed_price
        position["unrealized_profit_loss"] = 0

        entry_price = float(position["enter_price"])
        sl = float(position["stop_loss"])
        tp = float(position["take_profit"])
        volume = float(position["volume"])
        side = str(position["side"])

        if side == "long":
            if closed_price == sl:

                position["trade_status"] = "sl_hit"
                position["realized_profit_loss"] = - volume * (entry_price - sl) / entry_price
                position["realized_profit_loss_percent"] = - (entry_price - sl) / entry_price * 100
                position["final_volume"] = volume - volume * (entry_price - sl) / entry_price

            elif closed_price == tp:
                position["trade_status"] = "tp_hit"
                position["realized_profit_loss"] = volume * (tp - entry_price) / entry_price
                position["realized_profit_loss_percent"] = (tp - entry_price) / entry_price * 100
                position["final_volume"] = volume + volume * (tp - entry_price) / entry_price

            else:
                position["trade_status"] = "closed"

                if closed_price > entry_price:

                    position["realized_profit_loss"] = volume * (closed_price - entry_price) / entry_price
                    position["realized_profit_loss_percent"] = (closed_price - entry_price) / entry_price * 100
                    position["final_volume"] = volume + volume * (closed_price - entry_price) / entry_price

                else:
                    position["realized_profit_loss"] = - volume * (entry_price - closed_price) / entry_price
                    position["realized_profit_loss_percent"] = - (entry_price - closed_price) / entry_price * 100
                    position["final_volume"] = volume - volume * (entry_price - closed_price) / entry_price

        if side == "short":

            if closed_price == sl:

                position["trade_status"] = "sl_hitted"
                position["realized_profit_loss"] = - volume * (sl - entry_price) / entry_price
                position["realized_profit_loss_percent"] = - (sl - entry_price) / entry_price * 100
                position["final_volume"] = volume - volume * (sl - entry_price) / entry_price

            elif closed_price == tp:
                position["trade_status"] = "tp_hitted"
                position["realized_profit_loss"] = volume * (entry_price - tp) / entry_price
                position["realized_profit_loss_percent"] = (entry_price - tp) / entry_price * 100
                position["final_volume"] = volume + volume * (entry_price - tp) / entry_price

            else:
                position["trade_status"] = "closed"

                if closed_price > entry_price:

                    position["realized_profit_loss"] = - volume * (closed_price - entry_price) / entry_price
                    position["realized_profit_loss_percent"] = - (closed_price - entry_price) / entry_price * 100
                    position["final_volume"] = volume - volume * (closed_price - entry_price) / entry_price

                else:

                    position["realized_profit_loss"] = volume * (entry_price - closed_price) / entry_price
                    position["realized_profit_loss_percent"] = (entry_price - closed_price) / entry_price * 100
                    position["final_volume"] = volume + volume * (entry_price - closed_price) / entry_price

        self.trade_list.append(position)

