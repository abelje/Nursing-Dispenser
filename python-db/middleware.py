from sqlite_code import get_user, database_update_drug_count
from sqlite_code import database_get_patient
from sqlite_code import database_get_drug
from sqlite_code import database_update_last_login

def authenticate(username, pswd):
    # grab the user info if it exists in the user table
    user = get_user(username, pswd)

    # check if the table contains the user associated with the pass
    if user is None:
        return False

    return True

def get_patient(username):
    # grab the patient info if it exists in the patient table
    patient = database_get_patient(username)

    # check if the table contains the patient(s) associated with the user
    if patient is None:
        return False

    return patient

def get_drug(patient_name):
    # grab the drug info if it exists in the drug table
    drug = database_get_drug(patient_name)

    # check if the table contains the drug(s) associated with the patient
    if drug is None:
        return False

    return drug

def update_last_login(username):
    database_update_last_login(username)

def amount_given(drug_name):
    # renaming drug to drug_name for clarity
    database_update_drug_count(drug_name)

# def drug_to_dispense(drug, drugs, dispense_table):
#     # switch from drug table to dispense table
#     # you have the drug, and then you look at the spot in the table that aligns with that drug
#     # you then remove that at that position and then insert that value into the other table
#     dispense_table.append(drug)

