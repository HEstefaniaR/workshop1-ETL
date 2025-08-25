import pandas as pd

def transform(df):
    # Normalize
    df = df.rename(columns={"First Name": "first_name",
        "Last Name": "last_name",
        "Email": "email",
        "Country": "country",
        "Application Date": "application_date",
        "YOE": "yoe",
        "Seniority": "seniority",
        "Technology": "technology",
        "Code Challenge Score": "code_challenge_score",
        "Technical Interview Score": "technical_interview_score"})
    
    df['application_date'] = pd.to_datetime(df['application_date'])


    # Hired flag
    df['hired_flag'] = ((df['code_challenge_score'] >= 7) & (df['technical_interview_score'] >= 7)).astype(int)


    # Dimensions
    dim_candidate = df[['first_name', 'last_name', 'email']].drop_duplicates().reset_index(drop=True)
    dim_country = df[['country']].drop_duplicates().reset_index(drop=True)
    dim_technology = df[['technology']].drop_duplicates().reset_index(drop=True)
    dim_seniority = df[['seniority']].drop_duplicates().reset_index(drop=True)

    dim_date = df[['application_date']].drop_duplicates().reset_index(drop=True)
    dim_date['date_id'] = dim_date['application_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['application_date'].dt.year
    dim_date['month'] = dim_date['application_date'].dt.month
    dim_date['day'] = dim_date['application_date'].dt.day
    

    # Fact table
    fact_application = df[[
        'first_name','last_name','email','country','technology','seniority',
        'application_date','yoe','code_challenge_score','technical_interview_score','hired_flag'
    ]]

    return {
        'dim_candidate': dim_candidate,
        'dim_country': dim_country, 
        'dim_technology': dim_technology, 
        'dim_seniority': dim_seniority,
        'dim_date': dim_date, 
        'fact_application': fact_application
    }