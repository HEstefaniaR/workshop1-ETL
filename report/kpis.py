import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../etl'))
from connection import get_conn

# Contrataciones por tecnología
def hires_by_technology():
    conn = get_conn()
    query = """
    SELECT t.technology, COUNT(f.application_id) AS hires
    FROM fact_application f
    JOIN dim_technology t ON f.technology_id = t.technology_id
    WHERE f.hired_flag = 1
    GROUP BY t.technology
    ORDER BY hires DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Contrataciones por año
def hires_by_year():
    conn = get_conn()
    query = """
    SELECT d.year, COUNT(f.application_id) AS hires
    FROM fact_application f
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE f.hired_flag = 1
    GROUP BY d.year
    ORDER BY d.year
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Contrataciones por seniority
def hires_by_seniority():
    conn = get_conn()
    query = """
    SELECT s.seniority, COUNT(f.application_id) AS hires
    FROM fact_application f
    JOIN dim_seniority s ON f.seniority_id = s.seniority_id
    WHERE f.hired_flag = 1
    GROUP BY s.seniority
    ORDER BY hires DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Contrataciones por país sobre los años (USA, Brasil, Colombia, Ecuador)
def hires_by_country_year():
    conn = get_conn()
    query = """
    SELECT d.year, c.country, COUNT(f.application_id) AS hires
    FROM fact_application f
    JOIN dim_country c ON f.country_id = c.country_id
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE f.hired_flag = 1
      AND c.country IN ('USA', 'Brazil', 'Colombia', 'Ecuador')
    GROUP BY d.year, c.country
    ORDER BY d.year, c.country
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Tasa de contratación total
def hire_rate():
    conn = get_conn()
    query = """
    SELECT 
        ROUND(SUM(f.hired_flag)/COUNT(f.application_id) * 100, 2) AS hire_rate_percent
    FROM fact_application f
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Proporción de candidatos por tecnología vs contratados
def tech_candidate_ratio():
    conn = get_conn()
    query = """
    SELECT t.technology,
           COUNT(f.application_id) AS total_candidates,
           SUM(f.hired_flag) AS hired,
           ROUND(SUM(f.hired_flag)/COUNT(f.application_id) * 100,2) AS hire_rate_percent
    FROM fact_application f
    JOIN dim_technology t ON f.technology_id = t.technology_id
    GROUP BY t.technology
    ORDER BY hire_rate_percent DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df