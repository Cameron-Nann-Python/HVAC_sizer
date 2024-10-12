import pandas as pd
from matplotlib import pyplot as plt

rain_values = []
rain_value = 6
for x in range(0,51):
    rain_values.append(rain_value)
    rain_value = round(rain_value - 0.1,1) 

GPH_values = [3.740, 3.678, 3.615, 3.553, 3.491, 3.428, 3.366, 3.304, 3.241, 3.179,
              3.117, 3.054, 2.992, 2.930, 2.867, 2.805, 2.743, 2.680, 2.618, 2.556, 
              2.493, 2.431, 2.369, 2.306, 2.244, 2.182, 2.119, 2.057, 1.995, 1.932, 
              1.870, 1.808, 1.745, 1.683, 1.621, 1.558, 1.496, 1.434, 1.371, 1.309, 
              1.247, 1.184, 1.122, 1.060, 0.997, 0.935, 0.873, 0.810, 0.748, 0.686, 
              0.623
]

GPM_per_sf_values = [0.0624, 0.0614, 0.0603, 0.0593, 0.0582, 0.0572, 0.0562, 0.0551, 0.0541, 0.0530, 
              0.0520, 0.0510, 0.0499, 0.0489, 0.0478, 0.0468, 0.0458, 0.0447, 0.0437, 0.0426, 
              0.0416, 0.0406, 0.0395, 0.0385, 0.0374, 0.0364, 0.0354, 0.0343, 0.0332, 0.0322,
              0.0312, 0.0302, 0.0291, 0.0281, 0.0270, 0.0260, 0.0250, 0.0239, 0.0229, 0.0218, 
              0.0208, 0.0198, 0.0187, 0.0177, 0.0166, 0.0156, 0.0146, 0.0135, 0.0125, 0.0114, 0.0104
]

rainfall = {'Rainfall in Inches/Hr':rain_values,
            'G.P.H./sf': GPH_values,
            'GPM/sf Values': GPM_per_sf_values}

rainfall_df = pd.DataFrame(rainfall)

pipe_diameters = [2, 2.5, 3, 4, 5, 6, 8]
GPM_values = [30, 54, 92, 192, 360, 563, 1208]
flow_capacity = {'Pipe Diameter': pipe_diameters,
                 'GPM': GPM_values
}

rainfall_df[['G.P.H./sf']].mean()

nplot = rainfall_df.plot(kind = 'scatter', x = 'G.P.H./sf', y = 'Rainfall in Inches/Hr')

plt.show()
