import joblib
from keras.models import load_model


def linear_regression_predict(income, household_head_sex,
                              num_family_members, number_of_workers,
                              number_of_television, number_of_car, number_of_phone,
                              number_of_personal_computer):
    # 加载模型
    loaded_model = joblib.load('../analysis/linear_regression_model.pkl')
    input_features = [[income, household_head_sex,
                       num_family_members, number_of_workers,
                       number_of_television, number_of_car, number_of_phone,
                       number_of_personal_computer]]

    print(input_features)

    # 使用模型进行预测
    predicted_value = loaded_model.predict(input_features)
    print(predicted_value)

    # 返回预测结果，保留两位小数
    return round(predicted_value[0], 2)


def neural_networks_predict(income, household_head_sex,
                            num_family_members, number_of_workers,
                            number_of_television, number_of_car, number_of_phone,
                            number_of_personal_computer):
    # 加载模型
    model = load_model('../analysis/neural_networks_model.h5')
    input_features = [[income, household_head_sex,
                       num_family_members, number_of_workers,
                       number_of_television, number_of_car, number_of_phone,
                       number_of_personal_computer]]

    predicted_value = model.predict(input_features)
    predicted_value = float(predicted_value)
    print(predicted_value)
    # 返回预测结果
    return round(predicted_value, 2)
