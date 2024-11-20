
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


######################################################
@dataclass
class StockData:
    """Stock data model"""
    code: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    estimated_volume: Optional[float] = None   # 估算交易量 
    vwap: Optional[float] = None   # VWAP
    
    
    
    @property
    def is_valid(self) -> bool:
        """Check if the data is valid"""
        return all([
            self.open > 0,
            self.high >= self.open,
            self.low <= self.open,
            self.volume > 0,
            self.amount > 0
        ])
        
    
    def calculate_vwap(self) -> float:
        """Calculate VWAP"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        pass


@dataclass
class Position:
    """Trading position model"""
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
        """計算當前盈虧"""
        pass
    
    def calculate_roi(self) -> float:
        """計算投資報酬率"""
        pass
    
    def update_stop_loss(self, new_stop_loss: float) -> None:
        """Update stop loss price"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        pass

#####################################################

@dataclass
class Trade:
    """Trade record model"""
    stock_code: str
    timestamp: datetime
    trade_type: TradeType      # 進場、出場、加倉、減倉
    position_type: PositionType   # long, short 
    price: float
    shares: int
    position_id: str
    commission: float = 0.0
    slippage: float = 0.0
    
    def calculate_value(self) -> float:
        """Calculate trade value including commission"""
        pass
    
    def calculate_cost(self) -> float:
        """Calculate total cost including commission and slippage"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        pass