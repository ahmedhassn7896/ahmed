import pandas as pd
from datetime import datetime

def flatten_users_data(raw_json_list):
    """
    Transforms nested API JSON response into a flat Pandas DataFrame.
    Target Columns: external_id, full_name, email, country
    """
    df = pd.DataFrame(raw_json_list)
    
    # Assuming API gives 'name' object with 'first' and 'last'
    if 'name' in df.columns:
        df['full_name'] = df['name'].apply(lambda n: f"{n.get('first', '')} {n.get('last', '')}".strip() if isinstance(n, dict) else n)
    else:
        df['full_name'] = 'Unknown'
        
    df['external_id'] = df['login'].apply(lambda l: l.get('uuid') if isinstance(l, dict) else l)
    
    # Extract country from nested location
    df['country'] = df['location'].apply(lambda l: l.get('country') if isinstance(l, dict) else l)
    
    df['last_updated'] = datetime.utcnow()
    
    # Keep only target columns
    columns_to_keep = ['external_id', 'full_name', 'email', 'country', 'last_updated']
    return df[columns_to_keep].dropna(subset=['external_id'])
