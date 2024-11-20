# config/settings.py

from typing import Dict, Any
from pathlib import Path
from datetime import time

class TradingConfig:
    """Trading system configuration"""
    
    # Database settings
    DB_CONFIG: Dict[str, Any] = {
        'host': 'localhost',
        'database': 'trading_db',
        'user': 'trader',
        'password': 'your_password',
        'port': 5432
    }
    
    # Trading parameters
    TRADING_PARAMS: Dict[str, Any] = {
        'initial_capital': 1000000,
        'commission_rate': 0.001425,
        'min_volume': 2000,
        'min_amount': 100000000,  # 1億
        'volume_surge_ratio': 3.0,  # 3倍量
        'max_position_multiplier': 5,  # 最大加倉倍數
        'price_tick': 0.01,  # 最小價格單位
        'max_positions': 10  # 最大持倉數量
    }
    
    # Time settings
    TIME_SETTINGS: Dict[str, Any] = {
        'market_open': time(9, 0),
        'market_close': time(13, 30),
        'early_entry': time(9, 5),
        'late_entry': time(9, 30),
        'exit_times': [time(13, 0), time(13, 30)]
    }
    
    # Risk management settings
    RISK_SETTINGS: Dict[str, Any] = {
        'stop_loss_range': (0.01, 0.04),  # (1%, 4%)
        'max_drawdown': 0.1,  # 10%
        'max_daily_loss': 0.05  # 5%
    }