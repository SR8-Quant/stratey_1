# data/repository.py

from typing import Dict, List, Optional, Union
import pandas as pd
from datetime import datetime
from data.database import DatabaseConnection
from data.models import StockData, Trade, Position

class StockDataRepository:
    """Stock data repository"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        self.cache = {}
        
    def get_stock_data(
        self,
        stock_code: str,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Get stock historical data"""
        pass
    
    def get_intraday_data(
        self,
        stock_code: str,
        date: datetime
    ) -> pd.DataFrame:
        """Get stock intraday data"""
        pass
    
    def get_market_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Get market data"""
        pass
    
    def get_volume_profile(
        self,
        stock_code: str,
        date: datetime,
        lookback: int = 260
    ) -> pd.DataFrame:
        """Get volume profile data"""
        pass
    
    def save_trade(self, trade: Trade) -> None:
        """Save trade record"""
        pass
    
    def get_trades(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Trade]:
        """Get historical trades"""
        pass
    
    def clear_cache(self) -> None:
        """Clear data cache"""
        pass