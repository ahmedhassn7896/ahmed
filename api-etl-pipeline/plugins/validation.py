def validate_user_data(df):
    """
    Checks for critical data quality issues before loading to DB.
    """
    if df.empty:
        raise ValueError("Transformed DataFrame is empty. Pipeline halted.")
    
    if df['external_id'].duplicated().any():
        raise ValueError("Primary Key violation: Duplicates found in external_id.")
        
    if df['email'].isnull().any():
        print("Warning: Missing emails detected. Imputing with default.")
        df['email'].fillna('no-reply@missing.com', inplace=True)
        
    return df
