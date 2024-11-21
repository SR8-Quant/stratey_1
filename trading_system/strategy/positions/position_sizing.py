import pandas as pd
import numpy as np
from typing import Dict, Optional, Any, List
from datetime import datetime
from data.models import Position, StockData, Trade
from strategy.filters.market_filter import MarketFilter


""" 
部位管理: 目前簡易實作 （需要重新撰寫）
1. 風險比例：資金分配上限
2. 市場條件: use market_filter
"""


class PositionSizer:
    
    def __init__(self, params: Dict[str, Any], market_filter: MarketFilter):
        self.initial_capital = params['initial_capital']
        self.max_position_multiplier = params['max_position_multiplier']
        self.risk_per_trade = params.get('risk_per_trade', 0.02)  # 每次交易的風險比例，預設為 2%
        self.market_filter = market_filter  # 市場過濾器實例
    
    def calculate_initial_position(
        self,
        capital: float,
        price: float,
        market_data: pd.DataFrame,
        trades: List[Trade]
    ) -> int:
        """
        計算初始部位大小，結合市場條件與過濾器結果動態調整
        :param capital: 可用資本
        :param price: 進場價格
        :param market_data: 大盤市場數據 DataFrame
        :param trades: 前一日的交易數據
        :return: 可交易的股數
        """
        # 1. 計算風險資金量
        risk_amount = capital * self.risk_per_trade
        
        # 2. 計算基礎部位大小
        base_size = risk_amount // price
        
        # 3. 應用市場過濾器
        market_trend = self.market_filter.analyze_market_trend(market_data)
        market_volume_condition = self.market_filter.check_market_volume(market_data)
        previous_profit = self.calculate_previous_profit(trades)
        position_factor = self.market_filter.calculate_position_factor(market_trend, previous_profit)
        
        # 4. 根據市場條件調整部位大小
        adjusted_size = self.adjust_position_size(base_size, position_factor, market_volume_condition)
        
        # 5. 確保部位大小不超過最大倍數限制
        max_size = (capital * self.max_position_multiplier) // price
        final_size = min(adjusted_size, max_size)
        
        return int(final_size)
    
    def calculate_previous_profit(self, trades: List[Trade]) -> float:
        """
        (OPTIONAL)
        計算前一日的總利潤
        :param trades: 前一日的交易數據
        :return: 總利潤（扣除成本後）
        """
        total_profit = 0.0
        for trade in trades:
            profit = trade.price * trade.shares - trade.commission - trade.slippage
            total_profit += profit
        return total_profit

    def adjust_position_size(
        self,
        base_size: int,
        position_factor: float,
        volume_condition: bool
    ) -> int:
        """
        根據市場條件調整部位大小
        :param base_size: 基礎部位大小
        :param position_factor: 根據市場條件計算的調整因子
        :param volume_condition: 是否符合交易量條件
        :return: 調整後的部位大小
        """
        # 如果市場量能條件不符合，縮小部位
        if not volume_condition:
            return int(base_size * 0.8)
        
        # 根據位置因子調整部位
        return int(base_size * position_factor)
    
    def calculate_total_exposure(
        self,
        positions: Dict[str, Position]
    ) -> float:
        """
        計算總市場曝險
        :param positions: 當前部位的字典
        :return: 總曝險佔資本的百分比
        """
        total_exposure = sum(position.current_price * position.shares for position in positions.values())
        return total_exposure / self.initial_capital
