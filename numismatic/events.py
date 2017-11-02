import time
import json     # TOOD: use a faster json library if necessary
from enum import Enum
import math

import attr


class OrderType(str, Enum):
    TRADE = 'TRADE'
    BUY = 'BUY'
    SELL = 'SELL'
    BID = 'BID'
    ASK = 'ASK'
    CANCEL = 'CANCEL'


@attr.s
class Event:

    def json(self):
        return json.dumps(attr.asdict(self))


@attr.s(slots=True)
class Heartbeat(Event):
    exchange = attr.ib()
    symbol = attr.ib()
    timestamp = attr.ib(default=attr.Factory(time.time))


@attr.s(slots=True)
class PriceUpdate(Event):
    exchange = attr.ib(convert=str)
    symbol = attr.ib(convert=str)
    price = attr.ib(convert=float)

@attr.s(slots=True)
class Ticker(PriceUpdate):
    best_bid = attr.ib(convert=float, default=math.nan)
    best_ask = attr.ib(convert=float, default=math.nan)
    volume_24h = attr.ib(convert=float, default=math.nan)
    open_24h = attr.ib(convert=float, default=math.nan)
    high_24h = attr.ib(convert=float, default=math.nan)
    low_24h = attr.ib(convert=float, default=math.nan)

@attr.s(slots=True)
class Trade(PriceUpdate):
    volume = attr.ib(convert=float)
    type = attr.ib(convert=OrderType, default='TRADE')
    timestamp = attr.ib(convert=float, default=attr.Factory(time.time))
    id = attr.ib(convert=str, default='')

@attr.s(slots=True)
class Order(Event):
    exchange = attr.ib(convert=str)
    symbol = attr.ib(convert=str)
    price = attr.ib(convert=float, default=math.nan)
    volume = attr.ib(convert=float, default=math.nan)
    type = attr.ib(convert=OrderType, default='TRADE')
    timestamp = attr.ib(convert=float, default=attr.Factory(time.time))
    id = attr.ib(convert=str, default='')

    @id.validator
    def _validate_id(self, attribute, value):
        if not value:
            self.id = self.price
