#fungsi yang digunakan pada Project.ipynb dideklarasikan ulang pada file ini
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Keperluan Pertumbuhan Level Polutan
def pollution_level(df,pos):
    return  df[df['station'] == pos]

def resample_df(df, rule):
    new_df = df.resample(rule = rule, on = 'date').agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'SO2': 'mean',
    'NO2': 'mean',
    'CO': 'mean',
    'O3': 'mean'
    }).reset_index()
    return new_df

def graph(df, rule, substance, station, color = 'red'):
    df = pollution_level(df,station)
    df = resample_df(df,rule)
    fig,ax = plt.subplots(figsize=(8,4))
    ax.plot(df.date, df[substance], color = color)
    ax.set_title('{} loc: {}'.format(substance,station))
    ax.grid()
    ax.tick_params(axis='x', labelrotation=17)
    return fig,ax

#Keperluan Tingkat Polutan per Wilayah
def pollution_region(df):
    df = df.groupby(by = 'station').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    }).reset_index()
    return df

colors = ['#8C000F']
for x in range(0,11):
    colors.append('#D3D3D3')

def bar(df, substance):
    df = pollution_region(df)
    fig,ax = plt.subplots(figsize=(8,4))

    sns.barplot(x="station", y=substance, data=df.sort_values(by = substance, ascending = False), 
            hue = "station", palette=colors, ax=ax)
    ax.set_title('Perbandingan Angka Polutan {}'.format(substance))
    ax.tick_params(axis='x', labelrotation=20)
    ax.set_xlabel('')
    return fig, ax

#Keperluan AQI
def pollution_part(df):
    data = {}
    for column in df.columns.tolist()[2:]:
        data[column] = [df[column].mean()]
    data = pd.DataFrame(data)
    return data

aqi_index = {
    'index': [0,50,100,150,200,300,500],
    'category': ['Good', 'Moderate', 'Quite Unhealthy', 'Unhealthy',
                 'Very Unhealthy', 'Hazardous', 'Hazardous'],
    'PM2.5': [0,12,35.4,55.4,150.4,250.4,500.4],
    'PM10': [0,54,154,254,354,424,604],
    'SO2': [0,35,75,185,304,604,1004],
    'NO2': [0,53,100,360,649,1249,2049],
    'CO': [0,440,940,1240,1540,3040,5040],
    'O3': [0,54,70,85,105,200]
}

def aqi_index_calc(df, index = aqi_index):
    aqi_df = {}
    for substance in df.columns.tolist():
        value = df[substance][0]
        aqi_list = aqi_index[substance]
        for i in range(len(aqi_list)):

            if value < aqi_list[i]:
                aqi_value = ((aqi_index['index'][i]-aqi_index['index'][i-1])/
                         (aqi_list[i]-aqi_list[i-1])*(value-aqi_list[i-1]) +
                         aqi_index['index'][i-1])
                
                aqi_df[substance] = [aqi_value, aqi_index['category'][i-1]]
                break
    aqi_df = pd.DataFrame(aqi_df)
    df = pd.concat([df/df.sum().sum()*100,aqi_df], ignore_index = True)
    df[''] = ['Percent%', 'AQI index', 'Category']
    df.set_index('', inplace=True)
    df.sort_values(by='AQI index', axis=1, inplace=True)
    return df

color_dict = {'good': '#008000', 'moderate': '#FFA500', 'quite unhealthy': '#F97306',
            'unhealthy': '#EF4026', 'very unhealthy': '#800000', 'hazardous': 'black'}

def colors_part(df, dict = color_dict):
    colors_aqi = []
    for category in df.iloc[2]:
        colors_aqi.append(color_dict[category.lower()])
    return colors_aqi

def aqi_bar(df):
    df = aqi_index_calc(pollution_part(df))
    color = colors_part(df)
    fig,ax = plt.subplots(figsize=(8,4))
    sns.barplot(y=df.iloc[1].index, x=df.iloc[1], 
            ax = ax, hue = df.iloc[1].sort_values().index, palette = color)
    ax.set_ylabel('')
    plt.legend(labels=color_dict.keys(),
           handles=[plt.Line2D([0], [0], color=value, lw=2) 
                    for value in color_dict.values()], fontsize = 7.5)
    return fig,ax

def pie_graph(df):
    df = aqi_index_calc(pollution_part(df))
    fig,ax = plt.subplots(figsize=(5,5))
    ax.pie(
        labels=df.iloc[0].sort_values(ascending = False).index.tolist(),
        x = df.iloc[0].sort_values(ascending = False).tolist(),
        autopct='%1.1f%%',
        colors = ['maroon', 'red', 'orangered',
                  'salmon', 'green', 'blue',],
        explode = [0.1,0,0,0,0,0],
        wedgeprops = {'width': 0.65,"edgecolor":"black", 
                     'linewidth': 1.2, 
                     'antialiased': True})
    return fig,ax
    
