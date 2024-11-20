import psycopg2

db_config = {
    'host': '120.126.194.247',
    'port': 5432,
    'database': 'postgres',  # 替換為你的資料庫名稱
    'user': 'aden',
    'password': 'sr8aden', 
}

try:
    connection = psycopg2.connect(**db_config)
    print("連線成功")
except Exception as e:
    print("連線失敗:", e)