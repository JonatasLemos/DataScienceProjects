def volume(df_dams, df_volumes, vol_array):
    for i in range(len(df_dams)):
        for j in range(len(df_volumes)):
            if df_dams.iloc[i][1].replace(" ", "") == df_volumes.iloc[j][0].replace(" ", ""):
                vol_array.append(df_volumes.iloc[j][1])

