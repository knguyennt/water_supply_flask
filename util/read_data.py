import pandas as pd

def read_vault_detail(path):
    df = pd.read_excel(path)
    return df

def lst_unique_value(df, name):
    return df[name].unique()


# if __name__ == "__main__":
#     df = read_vault_detail('data/vault_detail.xlsx')
#     print(lst_unique_value(df, 'Đơn vị phối hợp'))