import sqlite3
import sqlalchemy as db
from sqlalchemy.sql.functions import current_timestamp, func


def get_user(username, pswd):
    # connect the database
    # connection = sqlite3.connect('wlcnursing.db')
    # cursor = connection.cursor()
    engine = db.create_engine("sqlite:///wlcnursing.db")
    conn = engine.connect()
    metadata = db.MetaData()
    user = db.Table('user', metadata, autoload_with=engine)

    # grab the tuple matching with given username and password
    # cursor.execute(
    #     """SELECT ID, username, password, inserted_on, last_login
    #        FROM user
    #        WHERE username = ?
    #          and password = ?""", (username, pswd)
    # )
    #
    # user_info = cursor.fetchone()
    # connection.close()
    query = (
        db.select(
            user
        )
        .where(
            user.c.username == username,
            user.c.password == pswd
        )
    )

    result_proxy = conn.execute(query)
    result_set = result_proxy.fetchone()

    # if there is no tuple with matching username and password, return none
    # if user_info is None:
    #     return None
    if result_set is None:
        return None

    # return tuple data
    # ID, username, password, inserted_on, last_login = user_info
    ID, username, password, inserted_on, last_login = result_set

    return {
        "ID": ID,
        "username": username,
        "password": password,
        "inserted_on": inserted_on,
        "last_login": last_login
    }

def database_get_patient(username):
    # connect the database
    # connection = sqlite3.connect('wlcnursing.db')
    # cursor = connection.cursor()
    engine = db.create_engine("sqlite:///wlcnursing.db")
    conn = engine.connect()
    metadata = db.MetaData()
    patient = db.Table('patient', metadata, autoload_with=engine)
    user_patient = db.Table('user_patient', metadata, autoload_with=engine)
    user = db.Table('user', metadata, autoload_with=engine)

    # cursor.execute(
    #     """SELECT *
    #     FROM patient p
    #     JOIN user_patient u_p on p.ID = u_p.patient_id
    #     JOIN user u on u_p.user_id = u.ID
    #     WHERE u.username = ?
    #     """, (username,)
    # )

    # patient_info = cursor.fetchall()
    # connection.close()

    query = (
        db.select(
            patient
        )
        .where(
            user.c.username == username,
            patient.c.ID == user_patient.c.patient_id,
            user_patient.c.user_id == user.c.ID,
        )
    )

    result_proxy = conn.execute(query)
    result_set = result_proxy.fetchall()

    patients = [
        {
            "ID": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "date_of_birth": row[3]
        }
        # for row in patient_info
        for row in result_set
    ]

    return patients

def database_get_drug(patient_name):
    # connect the database
    connection = sqlite3.connect('wlcnursing.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT d.name, d.drawer_num
        FROM drug d
        JOIN patient_drug p_d on d.ID = p_d.drug_id
        JOIN patient p on p.ID = p_d.patient_id
        WHERE p.first_name = ?
        """, (patient_name,)
    )

    drug_info = cursor.fetchall()
    connection.close()

    drugs = [
        {
            "name": row[0],
            "drawer_num": row[1],
        }
        for row in drug_info
    ]

    return drugs

def database_update_last_login(username):
    # connect the database
    engine = db.create_engine("sqlite:///wlcnursing.db")
    metadata = db.MetaData()
    user = db.Table('user', metadata, autoload_with=engine)

    query = (
        db.update(user)
        .where(user.c.username == username)
        # .values(last_login = func.current_timestamp())
        .values(last_login=func.datetime('now', 'localtime'))
    )

    with engine.begin() as conn:
        conn.execute(query)
        conn.commit()

def database_update_drug_count(drug_name):
    # connect the database
    engine = db.create_engine("sqlite:///wlcnursing.db")
    metadata = db.MetaData()
    drug = db.Table('drug', metadata, autoload_with=engine)

    query = (
        db.update(drug)
        .where(drug.c.name == drug_name)
        .values(drug_count = drug.c.drug_count + 1)
    )

    with engine.begin() as conn:
        conn.execute(query)
        conn.commit()
