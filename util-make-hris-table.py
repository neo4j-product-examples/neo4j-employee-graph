import os
from person import get_short_id
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('input-hris-data/project-assignments.csv')
    df['person_id'] = df['resume_file'].apply(lambda x: get_short_id(x))
    df.drop(columns=['resume_file', 'assignment_id', 'employee_id'], inplace=True)

    os.makedirs("hris-tables", exist_ok=True)

    df.to_csv("hris-tables/project-assignments.csv", index=False)