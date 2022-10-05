import pyRofex
import enum
import configparser


class States(enum.Enum):
    WAITING_MARKET_DATA = 0
    WAITING_CANCEL = 1
    WAITING_ORDERS = 2


class MyStrategy:

    def __init__(self, config, instrument, size, spread):
        # Define variables
        self.instrument = instrument
        self.comision = 0
        self.initial_size = size
        self.buy_size = size
        self.sell_size = size
        self.spread = spread
        self.tick = 0.05
        self.my_order = dict()
        self.last_md = None
        self.state = States.WAITING_MARKET_DATA

        # Initialize the environment
        pyRofex.initialize(user=config['pyrofex'].get('user'),
                           password=config['pyrofex'].get('password'),
                           account=config['pyrofex'].get('account'),
                           environment=pyRofex.Environment.REMARKET)

        # Initialize Websocket Connection with the handler
        pyRofex.init_websocket_connection(
            market_data_handler=self.market_data_handler,
            order_report_handler=self.order_report_handler
        )
        print('Is connected ' +
              str(pyRofex.components.globals.environment_config[pyRofex.Environment.REMARKET]['ws_client'].connected))
        # Subscribes for Market Data
        pyRofex.market_data_subscription(
            tickers=[
                self.instrument
            ],
            entries=[
                pyRofex.MarketDataEntry.BIDS,
                pyRofex.MarketDataEntry.OFFERS
            ]
        )

        # Subscribes to receive order report for the default account
        pyRofex.order_report_subscription()

    # Defines the handlers that will process the messages.
    def market_data_handler(self, message):
        if self.state is States.WAITING_MARKET_DATA:
            print("Processing Market Data Message Received: {0}".format(message))
            self.last_md = None
            bid = message["marketData"]["BI"]
            offer = message["marketData"]["OF"]
            if bid and offer:  # check that market spread exist
                bid_px = bid[0]["price"]
                offer_px = offer[0]["price"]
                bid_offer_spread = round(offer_px - bid_px, 2)
                if bid_offer_spread >= self.spread:
                    print(self.my_order)
                    if self.my_order:
                        print('Orders')
                        sides = {k:v['orderReport']['side'] for k,v in self.my_order.items()} #v.values()["orderReport"]["side"]
                        print(sides)
                        for order in self.my_order.values():  # we only update if there is previous BID or offer
                            if (order["orderReport"]["side"] == "BUY" and \
                                    order["orderReport"]["price"] < bid_px) or "BUY" not in sides.values():  # if existing mm order is not at TOB, send new order market price plus one tick
                                self._send_order(pyRofex.Side.BUY, round(bid_px + self.tick, 2), self.buy_size)
                            elif (order["orderReport"]["side"] == "SELL" and \
                                    order["orderReport"]["price"] > offer_px) or "SELL" not in sides.values():
                                self._send_order(pyRofex.Side.SELL, round(offer_px - self.tick, 2), self.sell_size)
                    else:  # first orders from algo
                        if self.buy_size > 0:
                            self._send_order(pyRofex.Side.BUY, round(bid_px + self.tick, 2), self.buy_size)
                        if self.sell_size > 0:
                            self._send_order(pyRofex.Side.SELL, round(offer_px - self.tick, 2), self.sell_size)
                else:  # Lower spread
                    self._cancel_if_orders()  # Cancel all
            else: # no bid or offer
                self._cancel_if_orders()
        else:  # Ii no waiting MD, save
            self.last_md = message

    # Defines the handlers that will process the Order Reports.
    def order_report_handler(self, order_report):
        print("Order Report Message Received: {0}".format(order_report))
        if order_report["orderReport"]["clOrdId"] in self.my_order.keys():
            self._update_size(order_report)
            if order_report["orderReport"]["status"] in ("NEW", "PARTIALLY_FILLED"):
                print("processing new order")
                self.my_order[order_report["orderReport"]["clOrdId"]] = order_report
            elif order_report["orderReport"]["status"] == "FILLED":
                print("processing filled")
                del self.my_order[order_report["orderReport"]["clOrdId"]]
            elif order_report["orderReport"]["status"] == "CANCELLED":
                print("processing cancelled")
                del self.my_order[order_report["orderReport"]["clOrdId"]]

            if self.state is States.WAITING_CANCEL:
                if not self.my_order:
                    self.state = States.WAITING_MARKET_DATA
                    if self.last_md:
                        self.market_data_handler(self.last_md)
            elif self.state is States.WAITING_ORDERS:  # was waiting order NEW or  FILLED/PARTIALLY_FILLED
                for order in self.my_order.values():  # sended order was PENDING_NEW
                    if not order:
                        return  # Exit waiting NEW order to arrive
                self.state = States.WAITING_MARKET_DATA  # With only one order we enter in market data wait status
                if self.last_md:
                    self.market_data_handler(self.last_md) # Send last MD message not processed for waiting order or cancel

    def _update_size(self, order):
        if order["orderReport"]["status"] in ("PARTIALLY_FILLED", "FILLED"):
            if order["orderReport"]["side"] == "BUY":
                self.buy_size -= round(order["orderReport"]["lastQty"])
            if order["orderReport"]["side"] == "SELL":
                self.sell_size -= round(order["orderReport"]["lastQty"])
            if self.sell_size == self.buy_size == 0:
                self.sell_size = self.buy_size = self.initial_size

    def _cancel_if_orders(self):
        if self.my_order:
            self.state = States.WAITING_CANCEL
            for order in self.my_order.values():
                pyRofex.cancel_order(order["orderReport"]["clOrdId"])
                print("canceling order %s" % order["orderReport"]["clOrdId"])

    def _send_order(self, side, px, size):
        self.state = States.WAITING_ORDERS
        order = pyRofex.send_order(
            ticker=self.instrument,
            side=side,
            size=size,
            price=round(px, 2),
            order_type=pyRofex.OrderType.LIMIT,
            cancel_previous=True
        )
        self.my_order[order["order"]["clientId"]] = None
        print("sending %s order %s@%s - id: %s" % (side, size, px, order["order"]["clientId"]))


if __name__ == "__main__":
    config = configparser.SafeConfigParser()
    found_config_file = config.read('config.cfg')
    MyStrategy(config, "PAMP/DIC22", 5, 20)

