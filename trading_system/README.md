## Structure 


trading_system/
├── config/
│   ├── __init__.py
│   ├── settings.py          # 系統配置（資料庫連接、交易參數等）
│   └── logging_config.py    # 日誌配置
├── data/
│   ├── __init__.py
│   ├── database.py         # 資料庫連接和基本操作
│   ├── repository.py       # 資料存取層
│   └── models.py          # 資料模型定義
├── strategy/
│   ├── __init__.py
│   ├── filters/
│   │   ├── __init__.py
│   │   ├── volume_filter.py      # 成交量相關篩選
│   │   ├── market_filter.py      # 大盤條件篩選
│   │   └── price_filter.py       # 價格相關篩選
│   ├── positions/
│   │   ├── __init__.py
│   │   ├── entry.py             # 進場邏輯
│   │   ├── exit.py              # 出場邏輯
│   │   └── position_sizing.py   # 部位大小計算
│   └── risk_management/
│       ├── __init__.py
│       ├── stop_loss.py         # 停損邏輯
│       └── money_management.py   # 資金管理
├── backtest/
│   ├── __init__.py
│   ├── engine.py               # 回測引擎
│   ├── performance.py          # 績效計算（從sr8_performance.py優化）
│   └── visualization.py        # 視覺化功能
├── utils/
│   ├── __init__.py
│   ├── datetime_utils.py       # 時間相關工具
│   └── calculations.py         # 通用計算功能
├── main.py                     # 主程式入口
└── requirements.txt            # 專案依賴