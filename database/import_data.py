import csv
import pymysql

# 连接到数据库
conn = pymysql.connect(host='localhost', user='root', password='ciOGrBs4p6_-', database='hetas_data', charset='utf8mb4')

# 创建一个游标对象
cur = conn.cursor()

# 打开CSV文件, 'r'表示读取模式
with open('data/12.csv', 'r', encoding='utf-8') as csvfile:
    # 创建CSV文件的阅读器对象
    reader = csv.reader(csvfile)
    # 跳过CSV文件的第一行
    next(reader)
    print(reader)
    # 遍历剩余行并插入到数据库中
    for row in reader:
        sql = "insert into expenditure_data(year_time, region, expenditure, salary, " \
              "per_capita_gdp, regional_consumer_price_index, unemployment_rate) " \
              "values (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])))

# 提交更改并关闭游标和连接
conn.commit()
cur.close()
conn.close()
