def straight_distance(n,df_distances,dams_array,dams_min_array):
    interval = n-1
    for i in range(len(df_distances)):
        dams_array.append(df_distances.iloc[i][3])
        if i % n == n-1:
            dams_min_array.append(min(dams_array[i-interval:i+1]))
# interval = 3
# j = interval - 1
# for i in range(len(df_distances)):
#     dams_set.append(df_distances.iloc[i][3])
#     # print(dams_set, "oi")
#     if(i == j):
#         j += interval
#         dams_min_dist.append(min(dams_set))
#         dams_set.clear()
def municipal(df_municipalities, df_pour, municipalities, municipalities_different):
    for i in range(len(df_municipalities)):
        for j in df_pour["flow_length"]:
            if j > df_municipalities.iloc[i][3] and j < df_municipalities.iloc[i][4]:
                municipalities_different.append(j)
                municipalities_different.append(df_municipalities.iloc[i][1])
                municipalities_different.append(abs((df_municipalities.iloc[i][3] - j) / 2))
            elif j > df_municipalities.iloc[i][4]:
                municipalities.append(j)
                municipalities.append(df_municipalities.iloc[i][1])
                municipalities.append(abs(df_municipalities.iloc[i][6]-j))