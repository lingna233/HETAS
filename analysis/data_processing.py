import joblib
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error  # MAE
from sklearn.metrics import r2_score  # R^2
from tensorflow import keras

from database.mysql_operation import *

session = Session()
# 使用 session.query() 方法执行查询
query = session.query(Household_data.household_income, Household_data.household_head_sex,
                      Household_data.num_family_members, Household_data.number_of_workers,
                      Household_data.number_of_television, Household_data.number_of_car, Household_data.number_of_phone,
                      Household_data.number_of_personal_computer, Household_data.total_household_expenditure)
# query.statement返回一个SQLAlchemy的SQL语句对象，该对象表示执行的查询语句。query.session.bind则返回一个SQLAlchemy的engine对象，该对象表示连接到数据库的引擎
data = pd.read_sql_query(query.statement, con=session.connection())

data.loc[:, 'total_household_expenditure'] /= 6.60

# 关闭会话
session.close()

print(data.head())  # 查看前5行数据
print(data.info())  # 查看数据类型和缺失的值

# 找出重复行
duplicate_rows = data[data.duplicated()]
print('重复行数：', duplicate_rows.shape[0])

print(data.head())  # 查看前5行数据


# 计算特征之间的相关系数
corr = data.corr()

# 设置热力图大小和字体大小
plt.figure(figsize=(10, 8))
sns.set(font_scale=1.2)

# 创建热力图2
sns.heatmap(corr, vmin=-1, vmax=1, annot=True, annot_kws={'fontsize': 12, 'fontweight': 'bold'})

# 调整图像布局
plt.tight_layout()

# 保存热力图
plt.savefig('../web/static/image/heatmap.jpg')

# 显示图像
plt.show()

# 删除不需要的列（特征）
x = data.drop(['total_household_expenditure'], axis=1)

# 目标变量
y = data['total_household_expenditure']

# 将数据集分为训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=48)


# 线性回归
def linear_regression():
    # 定义线性回归模型对象
    linreg = LinearRegression()

    # 对训练集进行拟合
    linreg.fit(x_train, y_train)

    # 对测试集进行预测
    y_pred = linreg.predict(x_test)

    # 根据公式，得到平均绝对误差, 决定系数
    mae = mean_absolute_error(y_test, y_pred)  # 平均绝对误差
    rr = r2_score(y_test, y_pred)  # 决定系数

    # MAE
    print("MAE:", mae)  # 显示平均绝对误差, 越接近0越好
    # R^2
    print("R^2:", rr)  # 显示决定系数, 越接近1越好

    # 做ROC曲线，对预测的数据和测试集里的数据进行对比
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 在右上角显示标签
    plt.xlabel("household")
    plt.ylabel("Consumption")
    plt.savefig('../web/static/image/ROC.jpg')
    plt.show()

    # 做残差图，对预测的数据和测试集里的数据进行对比
    residuals = y_test - y_pred
    plt.scatter(y_pred, residuals)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.savefig('../web/static/image/residual_plot.jpg')
    plt.show()

    # 保存模型
    joblib.dump(linreg, 'linear_regression_model.pkl')
    # # 加载模型
    # loaded_model = joblib.load('linear_regression_model.pkl')


# 神经网络
def neural_networks():
    # 构建模型
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(8,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)
    ])

    # 编译模型
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mae')

    # 加载数据并训练模型
    model.fit(x_train, y_train, epochs=1000)

    # 使用模型进行预测
    predictions = model.predict(x_test)

    # 创建一个散点图，将真实值和预测值绘制在同一张图中
    plt.scatter(y_test, predictions)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')

    # 添加一条标识线（identity line）
    plt.plot([0, max(y_test)], [0, max(y_test)], 'k--')

    # 设置图像的标题
    plt.title('Neural Networks Model Prediction')

    # 保存图像
    plt.savefig('../web/static/image/scatter_plot.jpg')

    # 显示图像
    plt.show()

    # 保存模型
    model.save('neural_networks_model.h5')

    # from keras.models import load_model
    #
    # # 加载模型
    # model = load_model('neural_networks_model.h5')


# 运行线性回归
linear_regression()

# 运行神经网络
neural_networks()
