import matplotlib.pyplot as plt
import pandas as pd
import scipy

input_data = 'data/cleaned_opendoar_data.csv'

# Helper functions

def get_dataframe(file, sort_key) -> pd.DataFrame:
    ''' Load csv into dataframe'''

    df_all_data = pd.read_csv(file, header=0, index_col=sort_key)

    return df_all_data

def pie_RIS_types(df_base:pd.DataFrame):
    ''' Pie chart of RIS types'''
    vals = df_base.groupby("repository_metadata.software.name").size().sort_values()
    print(vals)
    explode = [0.2, 0, 0]
    labels = [
        "Contains software",
        "Does not\ncontain software",
        "No direct software\n search capability",
    ]
    plt.pie(vals, labels=labels, autopct="%1.1f%%", explode=explode)
    plt.title("Software contained in \nUK Academic Institutional Repositories")
    plt.axis("equal")
    plt.show()
    
df = get_dataframe(input_data, sort_key='system_metadata.id')

pie_RIS_types(df)