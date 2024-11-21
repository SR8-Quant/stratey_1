from typing import Dict, List, Any
from datetime import datetime
from data.models import Position, Trade

class MoneyManager:
    """Money management implementation"""
    
    def __init__(self, params: Dict[str, Any]):
        self.initial_capital = params['initial_capital']  # 初始資本
        self.max_drawdown = params['max_drawdown']  # 最大回撤（百分比）
        self.max_daily_loss = params['max_daily_loss']  # 最大每日損失（百分比）
        
    def calculate_position_value(
        self,
        positions: Dict[str, Position]
    ) -> float:
        """
        計算當前部位總價值
        :param positions: 當前部位的字典
        :return: 所有部位的總價值
        """
        # TODO:
        # 1. 遍歷 `positions` 中的每個部位。
        # 2. 將每個部位的價值（`current_price * shares`）加總。
        # 3. 返回總價值。
        pass
    
    def calculate_available_capital(
        self,
        positions: Dict[str, Position],
        cash: float
    ) -> float:
        """
        計算可用資本
        :param positions: 當前部位
        :param cash: 可用現金
        :return: 用於新交易的可用資本
        """
        # TODO:
        # 1. 計算所有部位的總價值，使用 `calculate_position_value`。
        # 2. 將總價值與 `self.initial_capital` 比較，確保未超過風險限制。
        # 3. 返回現金餘額作為可用資本。
        pass
    
    def check_risk_limits(
        self,
        positions: Dict[str, Position],
        trades: List[Trade]
    ) -> bool:
        """
        檢查是否超過風險限制
        :param positions: 當前部位
        :param trades: 今日的交易清單
        :return: 如果未超過風險限制，返回 True, 否則返回 False
        """
        # TODO:
        # 1. 計算當前部位的總價值。
        # 2. 使用 `calculate_daily_loss` 計算當日損失。
        # 3. 使用 `calculate_drawdown` 檢查當前回撤。
        # 4. 確保日損失與回撤均在設定的限制內。
        # 5. 返回檢查結果。
        pass
    
    def calculate_daily_loss(
        self,
        trades: List[Trade]
    ) -> float:
        """
        計算當日總損失
        :param trades: 今日的交易清單
        :return: 當日的總損失
        """
        # TODO:
        # 1. 遍歷 `trades`，檢查每筆交易的盈虧。
        # 2. 計算總盈虧，僅考慮虧損的交易。
        # 3. 返回總虧損值。
        pass
    
    def calculate_drawdown(
        self,
        equity_curve: List[float]
    ) -> float:
        """
        計算當前回撤
        :param equity_curve: 資本曲線（每個時間點的淨值）
        :return: 當前回撤百分比
        """
        # TODO:
        # 1. 找到 `equity_curve` 中的歷史最高淨值。
        # 2. 計算當前淨值與最高淨值的差值。
        # 3. 使用最高淨值將差值標準化，計算回撤百分比。
        # 4. 返回回撤百分比。
        pass
    
    # def adjust_position_size(
    #     self,
    #     base_size: int,
    #     risk_metrics: Dict[str, float]
    # ) -> int:
    #     """
    #     根據風險指標調整部位大小
    #     :param base_size: 基礎部位大小
    #     :param risk_metrics: 當前風險指標
    #     :return: 調整後的部位大小
    #     """
    #     # TODO:
    #     # 1. 根據風險指標調整 `base_size`。
    #     # 2. 確保調整後的部位大小不超過設定的風險限制。
    #     # 3. 返回調整後的部位大小。
    #     pass
