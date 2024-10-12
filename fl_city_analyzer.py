import pandas as pd 

cities_FL = ['APALACHICOLA.csv',
             'ARCADIA.csv',
             'ARCHBOLD.csv',
             'AVON PARK.csv',
             'BARTOW.csv']

def raincatcher():
    city_list = []
    for city in cities_FL:
        df = pd.read_csv(city)
        # remove outliers
        df = df[df[' precipitation'] >= 0]
        rainfall_per_hour = round(df[' precipitation'].mean(),2)
        city_list.append((city[0:-4],rainfall_per_hour))
    
    return city_list

city_list = raincatcher()
print(city_list)