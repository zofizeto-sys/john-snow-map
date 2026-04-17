#developed by Fouad Zablith

import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image

#load the data from excel in a dateframe
#a similar (with cleaner ) dataset is accessible online at https://docs.google.com/file/d/0B1k6zmQ4NXQlZ0dBcjFrNWhUSTA/edit
data = pd.read_excel(r'CholeraPumps_Deaths.xls')
df = pd.DataFrame(data, columns=['count','geometry'])

#clean and replace the coordinates data to fit the PyDeck map 
df = df.replace({'<Point><coordinates>': ''},regex=True )
df = df.replace({'</coordinates></Point>': ''},regex=True )

#create new longitude and latitude columns in dataframe
split = df['geometry'].str.split(',',n=1, expand=True)
df['lon'] = split[0].astype(float)
df['lat'] = split[1].astype(float)

df.drop(columns=['geometry'], inplace = True)


#st.write(df)

st.header('John Snow\'s 1854 Cholera Deaths Map in London')
st.subheader('Adjust the slider to 9 number of deaths and you will realize that the only big red dot left in the map represents the only area with the most number of deaths due to its high proximity to the water pump where the water is infected by the cholera disease')

# Get dynamic max value from actual data (excluding pumps marked as -999)
deaths_df = df[df['count'] != -999]
max_deaths = int(deaths_df['count'].max())
min_deaths = int(deaths_df['count'].min())

# Use range slider instead of single slider
death_range = st.slider('Number of Deaths Range', min_deaths, max_deaths, (min_deaths, max_deaths))
filtered_df = df[(df['count'] >= death_range[0]) & (df['count'] <= death_range[1]) & (df['count'] != -999)]
st.subheader(f'Map of deaths between {death_range[0]} and {death_range[1]}')

#get the pumps location from the last 8 entries in the data (in the original data source, pumps were noted as having -999 death as a differentiator)
pumps_df = df[df['count'] == -999]


#checkbox to enable seeing the location of pumps
if(st.checkbox('Show pumps',value=True)):
    pump_radius = 5
else:
    pump_radius = 0

col1, col2 = st.columns([3, 1])

with col1:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=51.5134,
            longitude=-0.1365,
            zoom=15.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered_df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius='[count]',
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=pumps_df,
                get_position='[lon, lat]',
                get_color='[0, 0, 255, 160]',
                get_radius=pump_radius,
            ),
         ],
    ))

with col2:
    st.write("")
    st.markdown("**Legend**")
    st.markdown("🔴 Red dots show death locations")
    st.markdown("Size reflects number of deaths")
    st.markdown("")
    st.markdown("🔵 Blue dots show water pump locations")



image = Image.open('Snow-cholera-map-1.jpg')

st.subheader('Original map of John Snow')
st.image(image,caption='Original map by John Snow showing the clusters of cholera cases in the London epidemic of 1854, drawn and lithographed by Charles Cheffins',use_column_width=True)

st.markdown('The source of the above map and more details on John Snow\'s work can be found here: [https://en.wikipedia.org/wiki/John_Snow](https://en.wikipedia.org/wiki/John_Snow)')

st.markdown("Developed by [Fouad Zablith](http://fouad.zablith.org). If you have any question about this simple app, you can reach me through: [@fzablith](https://twitter.com/fzablith)")