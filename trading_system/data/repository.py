# data/repository.py

from typing import Dict, List, Optional, Union
import pandas as pd
from datetime import datetime
from data.database import DatabaseConnection
from data.models import StockData, Trade, Position

""" 負責數據的讀取、處理邏輯和應用程式的數據存取介面。"""


class StockDataRepository:
    """Stock data repository"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        self.cache = {}    # 字典結構，用於儲存常用數據以減少查詢次數
        
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
        """獲取大盤、指數data"""
        pass
    
    
    def get_volume_profile(
        self,
        stock_code: str,
        date: datetime,
        lookback: int = 252
    ) -> pd.DataFrame:
        """計算股票在一段時間內的交易量分佈，通常用於分析支持和阻力位"""
        pass
    
    
    def save_trade(self, trade: Trade) -> None:
        """將一筆交易記錄(Trade)保存到資料庫中"""
        pass
    
    def get_trades(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Trade]:
        """查詢指定時間範圍內的歷史交易記錄"""
        pass
    
    def clear_cache(self) -> None:
        """清空緩存中的數據，強制後續查詢直接訪問資料庫"""
        pass