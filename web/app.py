from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from database.mysql_operation import *
from analysis.predict import linear_regression_predict, neural_networks_predict
from flask_paginate import Pagination

app = Flask(__name__)

app.secret_key = '123456789'


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))  # 重定向到主页


@app.route("/check_login", methods=['POST'])
def check():
    if request.method == 'POST':
        print('post请求')
        username = request.json.get('username')
        print(username)
        result = check_username(username)
        if result == 1:
            password = request.json.get('password')
            print(password)
            result1 = check_password(username, password)
            result2 = check_permissions(username)
            if result1 == 1 and result2 != 0:
                session['username'] = username
                dict1 = {"code": 200}  # 普通用户登录成功
                return jsonify(dict1)
            elif result1 == 1 and result2 == 0:  # 管理员登录成功
                session['username'] = username
                dict1 = {"code": 300}
                return jsonify(dict1)
            else:
                dict1 = {"code": 400,
                         'message': '密码错误'}
                return jsonify(dict1)
        else:
            print("没有该用户")
            dict1 = {"code": 400,
                     'message': '用户名或密码错误'}
            return jsonify(dict1)
    else:
        print('get请求')
        return 'OK'


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/do_register', methods=['POST'])
def do_register():
    if request.method == 'POST':
        print('post请求')
        username = request.json.get('username')
        print(username)
        password = request.json.get('password')
        permissions = ''
        result = add_user(username, password, permissions)
        if result == 1:
            dict1 = {"code": 200}  # 用户注册成功
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


@app.route('/data_inquire')
def data_inquire():
    return render_template("data_inquire.html")


@app.route('/data_predict')
def data_predict():
    username = session['username']
    datas = query_user_data2(username)
    num = datas.count() - 1
    # print(datas[datas.count() - 1].data_id)
    if datas.count() == 0 or datas.count() == 1:
        rtext = '数据不足，无法判断'
    elif datas[num].total_household_expenditure > datas[num - 1].total_household_expenditure:
        rtext = '家庭支出比上一次增加，建议减少支出'
    else:
        rtext = '家庭支出比上一次减少，建议继续保持'
    xdatas = []
    ydatas = []
    # 向xdatas和ydatas添加数据
    for data in datas:
        xdatas.append(data.data_id)
        ydatas.append(data.total_household_expenditure)
    print(xdatas, ydatas)
    return render_template("data_predict.html", rtext=rtext, xdatas=xdatas, ydatas=ydatas)


@app.route('/do_predict', methods=['POST'])
def do_predict():
    if request.method == 'POST':
        print('post请求')
        selected_model = request.json.get('selectedModel')
        income = int(request.json.get('income'))
        household_head_sex = int(request.json.get('household_head_sex'))
        num_family_members = int(request.json.get('num_family_members'))
        number_of_workers = int(request.json.get('number_of_workers'))
        number_of_television = int(request.json.get('number_of_television'))
        number_of_car = int(request.json.get('number_of_car'))
        number_of_phone = int(request.json.get('number_of_phone'))
        number_of_personal_computer = int(request.json.get('number_of_personal_computer'))
        print(selected_model, type(income))
        username = session['username']
        # print(username)
        if selected_model == 'linear_regression':
            output_household_expenditure = linear_regression_predict(income, household_head_sex,
                                                                     num_family_members, number_of_television,
                                                                     number_of_workers, number_of_car, number_of_phone,
                                                                     number_of_personal_computer)
            add_user_data(income, household_head_sex,
                          num_family_members, number_of_television,
                          number_of_workers, number_of_car, number_of_phone,
                          number_of_personal_computer, output_household_expenditure, username)

            # 返回 JSON 格式的响应
            return jsonify({"output_household_expenditure": output_household_expenditure})
        if selected_model == 'neural_networks':
            output_household_expenditure = neural_networks_predict(income, household_head_sex,
                                                                   num_family_members, number_of_television,
                                                                   number_of_workers, number_of_car, number_of_phone,
                                                                   number_of_personal_computer)
            add_user_data(income, household_head_sex,
                          num_family_members, number_of_television,
                          number_of_workers, number_of_car, number_of_phone,
                          number_of_personal_computer, output_household_expenditure, username)
            return jsonify({"output_household_expenditure": output_household_expenditure})
    else:
        print('get请求')
        return 'GET'


@app.route('/user_management')
def user_management():
    page = int(request.args.get("page", 1))
    result = list_user(page)
    users = result[0]
    total = result[1]

    paginate = Pagination(page=page, total=total)
    print(users)
    return render_template('user_management.html', users=users, paginate=paginate)


# 用户管理界面搜索功能
@app.route('/user_search', methods=['POST'])
def user_search():
    id = ''
    keyword = request.form.get('keyword')
    if not keyword:
        return redirect('user_management')
    users = query_user(id, keyword)
    print(users)
    return render_template('user_management2.html', users=users)


# 用户管理界面删除功能
@app.route('/user_delete', methods=['GET', 'POST'])
def user_delete():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
    delete_user(id)

    return redirect('user_management')


@app.route('/user_add')
def ussr_add():
    return render_template("user_add.html")


# 用户管理界面添加功能
@app.route('/do_adduser', methods=['POST'])
def do_adduser():
    if request.method == 'POST':
        print('post请求')
        username = request.json.get('username')
        print(username)
        password = request.json.get('password')
        permissions = request.json.get('permissions')
        result = add_user(username, password, permissions)
        if result == 1:
            dict1 = {"code": 200}  # 用户注册成功
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


@app.route('/user_edit')
def ussr_edit():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
        keyword = ''
        users = query_user(id, keyword)
        print(users)
        return render_template('user_edit.html', user=users, id=id)


# 用户管理界面修改功能
@app.route('/do_useredit', methods=['GET', 'POST'])
def do_useredit():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
        keyword = ''
        users = query_user(id, keyword)
        print(users)
        return render_template('user_edit.html', user=users, id=id)
    elif request.method == 'POST':
        print('post请求')
        username = request.json.get('username')
        print(username)
        password = request.json.get('password')
        permissions = request.json.get('permissions')
        id = request.json.get('id')

        result = edit_user(username, password, permissions, id)
        if result == 1:
            dict1 = {"code": 200}  # 用户注册成功
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


# 数据管理
@app.route('/data_management')
def data_management():
    page = int(request.args.get("page", 1))
    result = list_data(page)
    datas = result[0]
    total = result[1]

    paginate = Pagination(page=page, total=total)
    print(datas)
    return render_template('data_management.html', datas=datas, paginate=paginate)


@app.route('/data_search', methods=['GET', 'POST'])
def data_search():
    global gimin
    global gimax
    if request.method == 'POST':
        imin = request.form.get('imin')
        imax = request.form.get('imax')
        gimin = imin
        gimax = imax
        if not imax:
            return redirect("data_management")
    else:
        imin = gimin
        imax = gimax
    page = int(request.args.get("page", 1))
    result = search_data(page, imin, imax)
    datas = result[0]
    total = result[1]

    paginate = Pagination(page=page, total=total)
    print(datas)
    return render_template('data_management.html', datas=datas, paginate=paginate, imin=imin, imax=imax)


@app.route('/data_delete', methods=['GET', 'POST'])
def data_delete():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
    delete_data(id)

    return redirect("data_management")


@app.route('/data_add')
def data_add():
    return render_template("data_add.html")


@app.route('/do_dataadd', methods=['POST'])
def do_dataadd():
    if request.method == 'POST':
        print('post请求')
        household_head_sex = request.json.get('household_head_sex')
        household_income = int(request.json.get('household_income'))
        print(household_income)
        num_family_members = int(request.json.get('num_family_members'))
        number_of_workers = int(request.json.get('number_of_workers'))
        number_of_television = int(request.json.get('number_of_television'))
        number_of_car = int(request.json.get('number_of_car'))
        number_of_phone = int(request.json.get('number_of_phone'))
        number_of_personal_computer = int(request.json.get('number_of_personal_computer'))
        total_household_expenditure = int(request.json.get('total_household_expenditure'))
        result = add_data(household_head_sex, household_income, num_family_members, number_of_workers,
                          number_of_television, number_of_car, number_of_phone, number_of_personal_computer,
                          total_household_expenditure)
        if result == 1:
            dict1 = {"code": 200}  # 用户注册成功
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


@app.route('/data_edit')
def data_edit():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
        data = query_data(id)
        print(data)
        return render_template('data_edit.html', data=data, id=id)


@app.route('/do_dataedit', methods=['GET', 'POST'])
def do_dataedit():
    if request.method == 'POST':
        print('post请求')
        did = request.json.get('did')
        household_head_sex = request.json.get('household_head_sex')
        household_income = int(request.json.get('household_income'))
        print(household_income)
        num_family_members = int(request.json.get('num_family_members'))
        number_of_workers = int(request.json.get('number_of_workers'))
        number_of_television = int(request.json.get('number_of_television'))
        number_of_car = int(request.json.get('number_of_car'))
        number_of_phone = int(request.json.get('number_of_phone'))
        number_of_personal_computer = int(request.json.get('number_of_personal_computer'))
        total_household_expenditure = int(request.json.get('total_household_expenditure'))
        result = edit_data(did, household_head_sex, household_income, num_family_members, number_of_workers,
                           number_of_television, number_of_car, number_of_phone, number_of_personal_computer,
                           total_household_expenditure)
        if result == 1:
            dict1 = {"code": 200}  # 用户注册成功
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


# 用户数据管理
@app.route('/user_data_management')
def user_data_management():
    page = int(request.args.get("page", 1))
    result = list_user_data(page)
    datas = result[0]
    total = result[1]

    paginate = Pagination(page=page, total=total)
    print(datas)
    return render_template('user_data_management.html', datas=datas, paginate=paginate)


@app.route('/user_data_search', methods=['GET', 'POST'])
def user_data_search():
    global gimin
    global gimax
    if request.method == 'POST':
        imin = request.form.get('imin')
        imax = request.form.get('imax')
        gimin = imin
        gimax = imax
        if not imax:
            return redirect("user_data_management")
    else:
        imin = gimin
        imax = gimax
    page = int(request.args.get("page", 1))
    result = search_user_data(page, imin, imax)
    datas = result[0]
    total = result[1]

    paginate = Pagination(page=page, total=total)
    print(datas)
    return render_template('user_data_management.html', datas=datas, paginate=paginate, imin=imin, imax=imax)


@app.route('/user_data_delete', methods=['GET', 'POST'])
def user_data_delete():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
    delete_user_data(id)

    return redirect("user_data_management")


@app.route('/user_data_edit')
def user_data_edit():
    if request.method == 'GET':
        id = request.args.get('id')
        print(id)
        data = query_user_data(id)
        print(data)
        return render_template('user_data_edit.html', data=data, id=id)


@app.route('/do_user_dataedit', methods=['GET', 'POST'])
def do_user_dataedit():
    if request.method == 'POST':
        print('post请求')
        did = request.json.get('did')
        household_head_sex = request.json.get('household_head_sex')
        household_income = int(request.json.get('household_income'))
        print(household_income)
        num_family_members = int(request.json.get('num_family_members'))
        number_of_workers = int(request.json.get('number_of_workers'))
        number_of_television = int(request.json.get('number_of_television'))
        number_of_car = int(request.json.get('number_of_car'))
        number_of_phone = int(request.json.get('number_of_phone'))
        number_of_personal_computer = int(request.json.get('number_of_personal_computer'))
        total_household_expenditure = int(request.json.get('total_household_expenditure'))
        result = edit_user_data(did, household_head_sex, household_income, num_family_members, number_of_workers,
                                number_of_television, number_of_car, number_of_phone, number_of_personal_computer,
                                total_household_expenditure)
        if result == 1:
            dict1 = {"code": 200}
            return jsonify(dict1)
        elif result == 2:
            dict1 = {"code": 400,
                     'message': '用户名已存在，请更换'}
            return jsonify(dict1)
        else:
            pass
    else:
        print('get请求')
        return 'GET'


# 图表展示
@app.route('/user_data_echars')
def user_data_echars():
    return render_template("data_echarts.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
