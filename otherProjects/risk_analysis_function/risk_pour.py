def risk_pour_function(df_filtered,list_of_risks,risk_pour):
    for i in df_filtered["FID"]:
        for j, k in list_of_risks:
            if i == j:
                risk_pour.append(k)
    df_filtered["risk_pour"] = risk_pour
def fid_function(fid,df_filtered,df_pour):
    for j in df_filtered["FlowLengthDam"]:
        for i in range(len(df_pour)):
            if abs(j - df_pour.iloc[i][2]) < 0.01:
                fid.append(df_pour.iloc[i][1])
    df_filtered["FID"] = fid
