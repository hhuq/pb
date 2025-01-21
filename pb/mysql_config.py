import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# MySQL 数据库配置
use_remote_db = True  # 设置为 True 使用远程数据库，False 使用本地数据库
selected_db = 'remote' if use_remote_db else 'local'
db_config = {
    'remote': {
        'host': '211.87.224.231:8123',
        'user': 'root',
        'password': '12345',
        'database': 'programmableweb'
    },
    'local': {
        'host': 'localhost:3306',
        'user': 'root',
        'password': 'root',
        'database': 'programmableweb'
    }
}

connection_string = f"mysql+pymysql://{db_config[selected_db]['user']}:{db_config[selected_db]['password']}@" \
                    f"{db_config[selected_db]['host']}/{db_config[selected_db]['database']}"
engine = sqlalchemy.create_engine(connection_string)


# 测试数据库连接
def test_db_connection():
    try:
        # 使用 pd.read_sql 执行查询并获取数据库版本
        query = "SELECT VERSION()"
        db_version = pd.read_sql(query, engine)

        # 格式化输出信息
        version_info = db_version.iloc[0, 0]  # 获取查询结果中的数据库版本
        print(f"成功连接到数据库！\n数据库版本: {version_info}")
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}\n")
        return False



# 从 MySQL 数据库中读取数据集
def load_data_from_mysql(table_name):
    # SQL 查询语句
    query = f"SELECT * FROM {table_name}"  # 表名
    df = pd.read_sql(query, engine)
    return df


# 将数据保存到 MySQL 数据库,若已存在表，则replace
def save_data_to_mysql(df, table_name):
    df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    print(f"数据已成功写入数据库表 {table_name} 中。")


# 调试信息
# test_db_connection()
