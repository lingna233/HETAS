# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, and_, ForeignKey
from sqlalchemy.orm import sessionmaker

Base = sqlalchemy.orm.declarative_base()  # 通过继承 Base 类来创建表模型类，可以使得这些类具有在数据库中映射成表的能力。


def connect_database():
    # 创建数据库连接
    engine = create_engine('mysql+pymysql://root:ciOGrBs4p6_-@localhost:3306/hetas_data', echo=True)
    return engine


Session = sessionmaker(bind=connect_database())  # sessionmaker()函数通过引擎对象 engine 来创建一个 Session 类，该类具有将来用于执行数据库操作的所有功能


# 用户表模型
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    permissions = Column(Integer)
    username = Column(String(50), unique=True)
    password = Column(String(50))


class User_household_data(Base):
    __tablename__ = 'user_household_data'

    data_id = Column(Integer, primary_key=True, autoincrement=True)
    household_income = Column(Integer)
    household_head_sex = Column(Integer)
    num_family_members = Column(Integer)
    number_of_workers = Column(Integer)
    number_of_television = Column(Integer)
    number_of_car = Column(Integer)
    number_of_phone = Column(Integer)
    number_of_personal_computer = Column(Integer)
    total_household_expenditure = Column(Integer)
    username = Column(String(50), unique=True)


class Household_data(Base):
    __tablename__ = 'household_data'

    data_id = Column(Integer, primary_key=True, autoincrement=True)
    household_income = Column(Integer)
    household_head_sex = Column(Integer)
    num_family_members = Column(Integer)
    number_of_workers = Column(Integer)
    number_of_television = Column(Integer)
    number_of_car = Column(Integer)
    number_of_phone = Column(Integer)
    number_of_personal_computer = Column(Integer)
    total_household_expenditure = Column(Integer)


# 检查给定用户名是否存在于user表中
def check_username(username):
    session = Session()
    result = session.query(User).filter_by(username=username).count()  # 查询方法（query()）和过滤器（filter_by()）来实现数据查询、插入和更新等操作
    session.close()
    if result == 0:
        return 0
    else:
        return 1


# 检查给定用户名和密码是否匹配
def check_password(username, password):
    session = Session()
    result = session.query(User).filter_by(username=username, password=password).count()
    session.close()
    if result != 0:
        return 1
    else:
        return 0


def check_permissions(username):
    session = Session()
    result = session.query(User).filter_by(username=username, permissions=0).count()
    print(result)
    session.close()
    if result == 0:
        return 1
    else:
        return 0


# 添加给定用户名和密码到user表中
def add_user(username, password, permissions):
    session = Session()
    if check_username(username):
        session.close()
        return 2
    else:
        if not permissions:
            permissions = 1
        user = User(permissions=permissions, username=username, password=password)
        session.add(user)
        session.commit()
        result = session.query(User).filter_by(username=username).count()
        session.close()
        if result != 0:
            return 1
        else:
            return 0


# 编辑用户
def edit_user(username, password, permissions, id):
    session = Session()
    uid = session.query(User).filter(User.username == username).first().id
    if check_username(username) and uid != int(id):
        session.close()
        return 2
    else:
        session.query(User).filter(User.id == id).update(
            {"permissions": permissions, "username": username, "password": password})
        session.commit()
        result = session.query(User).filter_by(username=username).count()
        session.close()
        if result != 0:
            return 1
        else:
            return 0


def delete_user(id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return 1
    else:
        session.close()
        return 0


def query_user(id, keyword):
    session = Session()
    if id:
        users = session.query(User).filter_by(id=id).first()
    elif keyword:
        users = session.query(User).filter(User.username == keyword)
    else:
        users = session.query(User).all()

    session.close()
    return users


def list_user(page):
    session = Session()
    limit = 10
    total = session.query(User).count()
    print(total)
    start = (page - 1) * limit
    end = page * limit if total > page * limit else total
    ret = session.query(User).slice(start, end)

    session.close()
    return [ret, total]


# 数据管理
def query_data(id):
    session = Session()
    datas = session.query(Household_data).filter_by(data_id=id).first()
    session.close()
    return datas


def list_data(page):
    session = Session()
    limit = 10
    total = session.query(Household_data).count()
    start = (page - 1) * limit
    end = page * limit if total > page * limit else total
    # paginate = Pagination(page=page, total=len(datas))
    ret = session.query(Household_data).slice(start, end)

    session.close()
    return [ret, total]


def search_data(page, imin, imax):
    session = Session()
    limit = 10
    total = session.query(Household_data).filter(
        and_(Household_data.household_income >= imin, Household_data.household_income <= imax)).count()
    start = (page - 1) * limit
    end = page * limit if total > page * limit else total
    # paginate = Pagination(page=page, total=len(datas))
    ret = session.query(Household_data).filter(
        and_(Household_data.household_income >= imin, Household_data.household_income <= imax)).slice(start, end)

    session.close()
    return [ret, total]


def delete_data(id):
    session = Session()
    household_data = session.query(Household_data).filter_by(data_id=id).first()
    if household_data:
        session.delete(household_data)
        session.commit()
        session.close()
        return 1
    else:
        session.close()
        return 0


# 添加数据
def add_data(household_head_sex, household_income, num_family_members, number_of_workers, number_of_television,
             number_of_car, number_of_phone, number_of_personal_computer, total_household_expenditure):
    session = Session()
    household_data = Household_data(household_head_sex=household_head_sex, household_income=household_income,
                                    num_family_members=num_family_members, number_of_workers=number_of_workers,
                                    number_of_television=number_of_television, number_of_car=number_of_car,
                                    number_of_phone=number_of_phone,
                                    number_of_personal_computer=number_of_personal_computer,
                                    total_household_expenditure=total_household_expenditure)
    session.add(household_data)
    session.commit()
    result = session.query(Household_data).filter_by(household_income=household_income).count()
    session.close()
    if result != 0:
        return 1
    else:
        return 0


# 编辑数据
# 添加数据
def edit_data(did, household_head_sex, household_income, num_family_members, number_of_workers, number_of_television,
              number_of_car, number_of_phone, number_of_personal_computer, total_household_expenditure):
    session = Session()
    session.query(Household_data).filter(Household_data.data_id == did).update(
        {"household_head_sex": household_head_sex, "household_income": household_income,
         "num_family_members": num_family_members, "number_of_workers": number_of_workers,
         "number_of_television": number_of_television, "number_of_car": number_of_car,
         "number_of_phone": number_of_phone, "number_of_personal_computer": number_of_personal_computer,
         "total_household_expenditure": total_household_expenditure})
    session.commit()
    result = session.query(Household_data).filter_by(data_id=did).count()
    session.close()
    if result != 0:
        return 1
    else:
        return 0


##########################################
# 用户预测数据表管理
# 数据管理
def query_user_data(id):
    session = Session()
    datas = session.query(User_household_data).filter_by(data_id=id).first()
    session.close()
    return datas


def query_user_data2(username):
    session = Session()
    datas = session.query(User_household_data).filter_by(username=username)

    session.close()
    return datas


def list_user_data(page):
    session = Session()
    limit = 10
    total = session.query(User_household_data).count()
    start = (page - 1) * limit
    end = page * limit if total > page * limit else total
    # paginate = Pagination(page=page, total=len(datas))
    ret = session.query(User_household_data).slice(start, end)

    session.close()
    return [ret, total]


def search_user_data(page, imin, imax):
    session = Session()
    limit = 10
    total = session.query(User_household_data).filter(
        and_(User_household_data.household_income >= imin, User_household_data.household_income <= imax)).count()
    start = (page - 1) * limit
    end = page * limit if total > page * limit else total
    # paginate = Pagination(page=page, total=len(datas))
    ret = session.query(User_household_data).filter(
        and_(User_household_data.household_income >= imin, User_household_data.household_income <= imax)).slice(start,
                                                                                                                end)

    session.close()
    return [ret, total]


def delete_user_data(id):
    session = Session()
    household_data = session.query(User_household_data).filter_by(data_id=id).first()
    if household_data:
        session.delete(household_data)
        session.commit()
        session.close()
        return 1
    else:
        session.close()
        return 0


# 编辑数据
# 添加数据
def edit_user_data(did, household_head_sex, household_income, num_family_members, number_of_workers,
                   number_of_television,
                   number_of_car, number_of_phone, number_of_personal_computer, total_household_expenditure):
    session = Session()
    session.query(User_household_data).filter(User_household_data.data_id == did).update(
        {"household_head_sex": household_head_sex, "household_income": household_income,
         "num_family_members": num_family_members, "number_of_workers": number_of_workers,
         "number_of_television": number_of_television, "number_of_car": number_of_car,
         "number_of_phone": number_of_phone, "number_of_personal_computer": number_of_personal_computer,
         "total_household_expenditure": total_household_expenditure})
    session.commit()
    result = session.query(User_household_data).filter_by(data_id=did).count()
    session.close()
    if result != 0:
        return 1
    else:
        return 0


# 添加用户家庭数据
def add_user_data(income, household_head_sex,
                  num_family_members, number_of_television,
                  number_of_workers, number_of_car, number_of_phone,
                  number_of_personal_computer, output_household_expenditure, username):
    session = Session()
    user_household_data = User_household_data(household_income=income, household_head_sex=household_head_sex,
                                              num_family_members=num_family_members,
                                              number_of_television=number_of_television,
                                              number_of_workers=number_of_workers, number_of_car=number_of_car,
                                              number_of_phone=number_of_phone,
                                              number_of_personal_computer=number_of_personal_computer,
                                              total_household_expenditure=output_household_expenditure,
                                              username=username)
    result = session.query(User_household_data).filter_by(
        total_household_expenditure=output_household_expenditure).count()
    print(result)
    if result == 0:
        session.add(user_household_data)
        session.commit()
        session.close()
        return 1
    else:
        session.close()
        return 0

# if __name__ == '__main__':
#     engine = create_engine('mysql+pymysql://root:123456@localhost:3306/hetas_data', echo=True)
#     Base.metadata.create_all(engine)
