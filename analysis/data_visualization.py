import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database.mysql_operation import *

session = Session()
# 使用 session.query() 方法执行查询
# query = session.query(Household_data.household_income, Household_data.household_head_age,
#                       Household_data.household_head_sex, Household_data.num_family_members,
#                       Household_data.age_less_than_5, Household_data.age_5_17, Household_data.number_of_workers,
#                       Household_data.number_of_television, Household_data.number_of_car, Household_data.number_of_phone,
#                       Household_data.number_of_personal_computer, Household_data.total_household_expenditure)
# # query.statement返回一个SQLAlchemy的SQL语句对象，该对象表示执行的查询语句。query.session.bind则返回一个SQLAlchemy的engine对象，该对象表示连接到数据库的引擎
# data = pd.read_sql_query(query.statement, con=session.connection())

data_income = session.query(Household_data.household_income)
# 将查询结果转换为列表
income_list = [i[0] for i in data_income]

# 统计每个收入区间的数量
bins = [0, 100000, 500000, 1000000, 3000000, 12000000]
labels = ['<100k', '100-500k', '500-1000k', '1000-3000k', '>3000k']
counts, _ = np.histogram(income_list, bins=bins)

# 绘制饼状图
plt.pie(counts, labels=labels, autopct='%1.1f%%')
plt.title('Distribution of Household Income(PHP)')
plt.savefig('../web/static/image/income.jpg')
plt.show()

data_expenditure = session.query(Household_data.total_household_expenditure)

# 将查询结果转换为列表
expenditure_list = [i[0] for i in data_expenditure]

# 统计每个收入区间的数量
bins = [0, 100000, 500000, 1000000, 3000000, 12000000]
labels = ['<100k', '100-500k', '500-1000k', '1000-3000k', '>3000k']
counts, _ = np.histogram(expenditure_list, bins=bins)

# 绘制饼状图
plt.pie(counts, labels=labels, autopct='%1.1f%%')
plt.title('Distribution of Household Expenditure(PHP)')
plt.savefig('../web/static/image/expenditure.jpg')
plt.show()


# 关闭会话
session.close()
