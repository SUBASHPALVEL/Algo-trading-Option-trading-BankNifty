"""
author SubashPalvel

It is used for the live execution for Algorithmic trading

"""

# 1 import statements

from kiteconnect import KiteConnect
import csv
import time
import math
from datetime import datetime, timedelta
import acctkn

# 2 importing models from acctkn.py

att = acctkn.att()
ap = acctkn.atp()

# 3 Accessing KiteConnect

kite = KiteConnect(api_key=ap)
kite.set_access_token(att)

orders = []
WeeklyExpiry = "2021-01-14"
Specify_the_Entry_TIME_HHMM = "1511"

# 4 Defining place order and returning Order ID


def def_place_mkt_order_buy(symbl):
    try:
        order_id = kite.place_order(
            tradingsymbol=symbl,
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NFO,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=25,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS,
            price=None,
            validity=None,
            disclosed_quantity=None,
            trigger_price=None,
            squareoff=None,
            stoploss=None,
            trailing_stoploss=None,
            tag=None,
        )

        print("Order placed. ID is:", order_id)
        return order_id
    except Exception as e:
        print("exception occured:" + str(e))


# 5 Defining buy order
def ORDER_mkt_order_BUY():
    tradingsymbol = "NIFTY BANK"
    ohlc = kite.ohlc("NSE:{}".format(tradingsymbol))
    ltp = ohlc["NSE:{}".format(tradingsymbol)]["last_price"]  # to get spot price
    print("\n BANKNIFTY SPOT Price:", ltp)
    val = ltp + 100
    val2 = math.fmod(val, 100)
    x = val - val2
    abs_val = "{:.0f}".format(x)  # to remove .0 string.
    PE_PRICE = "{}".format("{:.0f}".format(x + 0))
    PE_PRICE_2 = "{}".format("{:.0f}".format(x - 300))
    print(
        "\n Identified ATM:",
        "{:.0f}".format(x),
        "So OTM (ATM-500) would be :",
        PE_PRICE_2,
    )
    bn = "BANKNIFTY"

    # for saving in csv

    with open("bn_instruments.txt", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for column in csv_reader:
            if (
                column[5] == PE_PRICE_2
                and column[3] == bn
                and column[4] == WeeklyExpiry
                and column[7] == "PE"
            ):

                ord_id = def_place_mkt_order_buy(column[2])
                orders.append(ord_id)
                print("\n CALL contract BUY Executed: ", column[2])

    print("\n The Executed order IDs are : ", orders)


# 6 Defining long put options


def PLACE_Long_Put_Options():

    print("\n Current time: ", datetime.now())
    curr_dt = time.strftime("%Y%m%d", time.localtime())

    set_order_placement_time_first = curr_dt + Specify_the_Entry_TIME_HHMM
    print("\n Order placement TIME configured as : ", set_order_placement_time_first)

    while True:

        curr_tm_chk = time.strftime("%Y%m%d%H%M", time.localtime())
        if (
            set_order_placement_time_first == curr_tm_chk
            or curr_tm_chk > set_order_placement_time_first
        ):
            print("\n The order execution started")
            ORDER_mkt_order_BUY()
            break
        else:
            print(
                "\n Going to wait 5 more seconds till: ",
                set_order_placement_time_first,
                " & CURRENT TIME IS",
                datetime.now(),
            )
            time.sleep(5)


PLACE_Long_Put_Options()
