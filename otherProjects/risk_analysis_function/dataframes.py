import pandas as pd
df_dams_paraopeba = pd.read_excel("relatorio_risco_barragens.xls", sheet_name="Dams")
df_all_dams_volume = pd.read_excel("relatorio_risco_barragens.xls", sheet_name="Report")
df_pour = pd.read_excel("relatorio_risco_barragens.xls", sheet_name="Pour")
df_distances = pd.read_excel("relatorio_risco_barragens.xls", sheet_name="Distances")
df_municipalities = pd.read_excel("relatorio_risco_barragens.xls", sheet_name="Municipalities")
# print(df_pour)
