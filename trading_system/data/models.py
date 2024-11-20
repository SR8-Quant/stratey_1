# data/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Union
from enum import Enum

class TradeType(Enum):
    """Trade type enumeration"""
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ADD = "ADD"
    REDUCE = "REDUCE"

class PositionType(Enum):
    """Position type enumeration"""
    LONG = "LONG"
    SHORT = "SHORT"

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
    estimated_volume: Optional[float] = None
    vwap: Optional[float] = None
    
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
        """Calculate current profit/loss"""
        pass
    
    def calculate_roi(self) -> float:
        """Calculate ROI"""
        pass
    
    def update_stop_loss(self, new_stop_loss: float) -> None:
        """Update stop loss price"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        pass

@dataclass
class Trade:
    """Trade record model"""
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
        """Calculate trade value including commission"""
        pass
    
    def calculate_cost(self) -> float:
        """Calculate total cost including commission and slippage"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        pass