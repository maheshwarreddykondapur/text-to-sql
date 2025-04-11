import pandas as pd
from sqlalchemy import create_engine

column_name_mapping = {"Claim Number": "insurance_claim_number", "Policy Number": "insurance_policy_number", "Date of Loss": "date_of_incident", "Time of Loss": "time_of_incident", "Loss Location": "incident_address", "Claimant Name": "insurance_claimant_name", "Vehicle Make": "insured_vehicle_make", "Vehicle Model": "insured_vehicle_model", "Vehicle Year": "insured_vehicle_manufacture_year", "Damage Description": "insured_vehicle_damage_type", "Reported By": "incident_reporter_name" , "Claim Status": "insurance_claim_status", "Police Report": "police_report_flag", "Photos/Videos": "photo_video_submission_flag", "Repair Estimate": "repair_estimate_submission_flag", "Towing Receipt": "towing_receipt_submission_flag", "Rental Receipt": "rental_receipt_submission_flag", "Medical & Injury Documentation": "medical_document_submission_flag", "Medical Reports": "medical_report_type", "Hospital Records": "hospital_diagnosis_type", "Third-Party Information": "third_party_insurance_flag", "Third-Party Insurance": "third_party_insurance_name", "Third-Party Claim Form": "third_party_claim_form_submission_flag", "Repair Estimate Cost": "vehicle_repair_cost_estimated_amount", "Hospital Cost": "hospital_cost_amount"}

def excel_to_sqlite(excel_path, sheet_name, sqlite_db, table_name):

    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    df.rename(columns = column_name_mapping, inplace = True)

    # Extracting City and Zip Codes from address
    df[['incident_city', 'incident_zipcode']] = df['incident_address'].str.split().apply(lambda x: pd.Series(x[-2:]))
    
    # Create an SQLAlchemy engine for the SQLite database.
    engine = create_engine(f'sqlite:///{sqlite_db}', echo=True)
    
    df.to_csv("test.csv", index=False)
    # Dump the DataFrame to the specified SQLite table. 
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    print(f"Data dumped to SQLite database '{sqlite_db}' in table '{table_name}' successfully!")

if __name__ == '__main__':
    # Path to the Claims data file
    excel_file = r"D:\Downloads\Worksheet in Excercise_Data Science IV.xlsx"
    
    # Name of the sheet in the Claims data file to load data from
    sheet = 'Sheet1'
    
    # SQLite database file
    sqlite_database = 'insurance.db'
    
    # Name of the table to store the Claims data in
    table = 'claims_table'
    
    excel_to_sqlite(excel_file, sheet, sqlite_database, table)
