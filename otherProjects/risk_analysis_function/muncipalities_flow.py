from pythonProjects.risk_analysis_function.dataframes import *
from pythonProjects.risk_analysis_function.risk_pour import *
from pythonProjects.risk_analysis_function.distances import *
import numpy as np

municipalities = []
municipalities_different = []
municipal(df_municipalities,df_pour,municipalities,municipalities_different)

# NORMAL CITIES
# NumPy conversion
np_municipalities = np.array(municipalities)
np_municipalities_reshape = np_municipalities.reshape(51,3)
df_municipalities_reshape = pd.DataFrame({'Municipality': np_municipalities_reshape[:, 1], 'FlowLengthDam': np_municipalities_reshape[:, 0], 'FlowDifference': np_municipalities_reshape[:, 2]})
# Filtering by query
df_filtered = df_municipalities_reshape.query('Municipality !="Moeda" and Municipality !="Brumadinho"')
fid = []
df_filtered["FlowLengthDam"] = df_filtered["FlowLengthDam"].astype(float)
fid_function(fid,df_filtered,df_pour)
# print(df_filtered)
# NORMAL CITIES END

# SPECIAL CITIES
np_municipalities_different = np.array(municipalities_different)
np_municipalities_different_new = np_municipalities_different.reshape(3, 3)
df_filtered_special = pd.DataFrame({'Municipality': np_municipalities_different_new[:, 1], 'FlowLengthDam': np_municipalities_different_new[:, 0], 'FlowDifference': np_municipalities_different_new[:, 2]})
df_filtered_special["FlowLengthDam"] = df_filtered_special["FlowLengthDam"].astype(float)
fid_special = []
fid_function(fid_special,df_filtered_special,df_pour)
# print(df_filtered_special)
