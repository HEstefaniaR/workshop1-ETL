import pandas as pd
import numpy as np
from connection import get_conn

def create_tables():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_candidate (
        candidate_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(100)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_country (
        country_id INT AUTO_INCREMENT PRIMARY KEY,
        country VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_technology (
        technology_id INT AUTO_INCREMENT PRIMARY KEY,
        technology VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_seniority (
        seniority_id INT AUTO_INCREMENT PRIMARY KEY,
        seniority VARCHAR(50)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_date (
        date_id INT PRIMARY KEY,
        application_date DATE,
        year INT,
        month INT,
        day INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_application (
        application_id INT AUTO_INCREMENT PRIMARY KEY,
        candidate_id INT,
        country_id INT,
        technology_id INT,
        seniority_id INT,
        date_id INT,
        yoe INT,
        code_challenge_score INT,
        technical_interview_score INT,
        hired_flag TINYINT,
        FOREIGN KEY (candidate_id) REFERENCES dim_candidate(candidate_id),
        FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
        FOREIGN KEY (technology_id) REFERENCES dim_technology(technology_id),
        FOREIGN KEY (seniority_id) REFERENCES dim_seniority(seniority_id),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print('Tablas creadas correctamente')


def load_dimension(df: pd.DataFrame, table: str, key_col: str):
    conn = get_conn()
    cursor = conn.cursor()

    cols = ', '.join(df.columns)  
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    cursor.executemany(insert_sql, df.values.tolist())
    conn.commit()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    dim_db = pd.DataFrame(rows, columns=colnames)

    cursor.close()
    conn.close()

    return dim_db


def load_fact(fact_df: pd.DataFrame, dim_dfs: dict):
    # Normalize
    fact_df['application_date'] = pd.to_datetime(fact_df['application_date']).dt.date
    dim_dfs['dim_date']['application_date'] = pd.to_datetime(dim_dfs['dim_date']['application_date']).dt.date

    
    fact = fact_df \
        .merge(dim_dfs['dim_candidate'], on=['first_name','last_name','email'], how='left') \
        .merge(dim_dfs['dim_country'], on='country', how='left') \
        .merge(dim_dfs['dim_technology'], on='technology', how='left') \
        .merge(dim_dfs['dim_seniority'], on='seniority', how='left') \
        .merge(dim_dfs['dim_date'][['date_id','application_date']], 
               on='application_date', how='left')

    fact = fact[[
        'candidate_id','country_id','technology_id','seniority_id',
        'date_id','yoe','code_challenge_score','technical_interview_score','hired_flag'
    ]]

    fact = fact.replace({pd.NA: None, np.nan: None, "nan": None})

    conn = get_conn()
    cursor = conn.cursor()
    cols = ', '.join(fact.columns)
    placeholders = ', '.join(['%s'] * len(fact.columns))
    insert_sql = f"INSERT INTO fact_application ({cols}) VALUES ({placeholders})"

    cursor.executemany(insert_sql, fact.values.tolist())
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Cargados {len(fact)} registros en fact_application")