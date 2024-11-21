
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Union, Any
from enum import Enum

"""
1. 定義固定變數 : trade type & position type
2. stock data : 
    a. is_valid : 確認價量的validness
    b. 計算VWAP 
    c. 計算成交量
    d. 轉換資料成 dict
    
3. position(倉位管理) :
    a. calculate_profit : 計算損益
    b. calculate_roi : 計算ROI
    c. update_stop_loss : 更新止損價
    d. to_dict : 轉換成 dict
    
4. trade :
    a. calculate_value : 計算成交金額
    b. calculate_cost : 計算成本
    c. to_dict : 轉換成 dict         """ 


class TradeType(Enum):
    """Trade type enumeration"""
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ADD = "ADD"   # 加倉
    REDUCE = "REDUCE"  # 減倉 

class PositionType(Enum):
    """Position type enumeration"""
    LONG = "LONG"
    SHORT = "SHORT"



############################################################
@dataclass
class StockData:
    code: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    estimated_volume: Optional[float] = None
    vwap: Optional[float] = None

    @property
    def is_valid(self) -> bool:
        """Check if the data is valid."""
        return all([
            self.open > 0,
            self.high >= self.open,
            self.low <= self.open,
            self.volume > 0,
            self.amount > 0
        ])

    def calculate_vwap(self) -> float:
        """Calculate VWAP (Volume Weighted Average Price)."""
        self.vwap = self.amount / self.volume if self.volume > 0 else 0
        return self.vwap

    def to_dict(self) -> Dict[str, Any]:
        """Convert the StockData to a dictionary."""
        return {
            "code": self.code,
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "amount": self.amount,
            "estimated_volume": self.estimated_volume,
            "vwap": self.vwap,
        }



######################################################
@dataclass
class Trade:
    stock_code: str
    timestamp: datetime
    trade_type: TradeType
    position_type: PositionType
    price: float
    shares: int
    position_id: str
    commission: float = 0.0
    slippage: float = 0.0

    def calculate_value(self) -> float:
        """Calculate the trade value."""
        return self.price * self.shares

    def calculate_cost(self) -> float:
        """Calculate total cost including commission and slippage."""
        return self.calculate_value() + self.commission + self.slippage

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Trade to a dictionary."""
        return {
            "stock_code": self.stock_code,
            "timestamp": self.timestamp,
            "trade_type": self.trade_type.value,
            "position_type": self.position_type.value,
            "price": self.price,
            "shares": self.shares,
            "position_id": self.position_id,
            "commission": self.commission,
            "slippage": self.slippage,
        }

##################################################################

@dataclass
class Position:
    stock_code: str
    position_type: PositionType
    entry_price: float
    current_price: float
    shares: int
    entry_time: datetime
    stop_loss_price: Optional[float] = None
    take_profit_price: Optional[float] = None
    position_id: Optional[str] = None

    def calculate_profit(self) -> float:
        """Calculate profit or loss."""
        return (self.current_price - self.entry_price) * self.shares

    def calculate_roi(self) -> float:
        """Calculate Return on Investment (ROI)."""
        if self.entry_price > 0:
            return self.calculate_profit() / (self.entry_price * self.shares)
        return 0.0

    def update_stop_loss(self, new_stop_loss: float) -> None:
        """Update the stop-loss price."""
        self.stop_loss_price = new_stop_loss

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Position to a dictionary."""
        return {
            "stock_code": self.stock_code,
            "position_type": self.position_type.value,
            "entry_price": self.entry_price,
            "current_price": self.current_price,
            "shares": self.shares,
            "entry_time": self.entry_time,
            "stop_loss_price": self.stop_loss_price,
            "take_profit_price": self.take_profit_price,
            "position_id": self.position_id,
        }


if __name__ == "__main__":
# Example stock data
    stock = StockData(
        code="AAPL",
        timestamp=datetime.now(),
        open=150.0,
        high=155.0,
        low=148.0,
        close=154.0,
        volume=1000,
        amount=150000.0
    )
    print(stock.is_valid)  # Output: True
    print(stock.to_dict())

    # Example position
    position = Position(
        stock_code="AAPL",
        position_type=PositionType.LONG,
        entry_price=150.0,
        current_price=154.0,
        shares=10,
        entry_time=datetime.now()
    )
    print(position.calculate_profit())  # Output: 40.0
    print(position.to_dict())

    # Example trade
    trade = Trade(
        stock_code="AAPL",
        timestamp=datetime.now(),
        trade_type=TradeType.ENTRY,
        position_type=PositionType.LONG,
        price=150.0,
        shares=10,
        position_id="123"
    )
    print(trade.calculate_value())  # Output: 1500.0
    print(trade.to_dict())

    
    



