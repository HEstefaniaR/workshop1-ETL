from extract import extract
from transform import transform
from load import create_tables, load_dimension, load_fact

def main():
    file_path = 'data/candidates.csv'
    df = extract(file_path)
    print(df.info())

    tables = transform(df)
    
    create_tables()

    dim_candidate = load_dimension(tables["dim_candidate"], "dim_candidate", "candidate_id")
    dim_country = load_dimension(tables["dim_country"], "dim_country", "country_id")
    dim_technology = load_dimension(tables["dim_technology"], "dim_technology", "technology_id")
    dim_seniority = load_dimension(tables["dim_seniority"], "dim_seniority", "seniority_id")
    dim_date = load_dimension(tables["dim_date"], "dim_date", "date_id")

    dim_dfs = {
        "dim_candidate": dim_candidate,
        "dim_country": dim_country,
        "dim_technology": dim_technology,
        "dim_seniority": dim_seniority,
        "dim_date": dim_date,
    }

    load_fact(tables["fact_application"], dim_dfs)

if __name__ == '__main__':
    main()