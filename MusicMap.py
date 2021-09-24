import pandas as pd
import numpy as np
import os
import folium
import folium.plugins
from geopy.geocoders import ArcGIS
from branca.element import Template, MacroElement
from pandas.core.dtypes.missing import isnull

# Reading the data

df1 = pd.read_csv('Rock Music/MTV_RockMusic.csv')
df_booking = pd.read_csv('Rock Music/bookings.csv')

df1 = df1.merge(df_booking, on='Name', how='left')
df1.head()



# Cleaning the data

df1.drop(columns=['Index', 'twitter'], axis = 1, inplace=True)
df1 = df1.apply(lambda x: x.str.strip())
df1["Genre"] = df1["Genre"].replace("\n", ', ', regex = True)
df1["Genre"] = df1['Genre'].str.title()
df1["Genre"] = df1["Genre"].replace("-", ' ', regex = True)
df1["Genre"] = df1["Genre"].replace("Music", '', regex = True)
df1["Active"] = df1["Active"].replace("\n", ', ', regex = True)
# df1["SpotifyName"] = df1["Name"].replace(" ", '%20', regex = True)
# df1["YoutubeName"] = df1["Name"].replace(" ", '+', regex = True)
df1['Period'] = df1['Active'].str[:3] + "0s"

######## Reducing the number of genres

df2 = df1.copy(deep=True)
df2['Genre'] = df2['Genre'].str.split(',')
df2 = df2.explode('Genre').reset_index(drop=True)
df2['Genre'] = df2['Genre'].str.strip()

df_genre = pd.read_csv('Rock Music/Genre_Delete.csv')
df_genre["Replacement"] = df_genre["Replacement"].replace("Null", '', regex = True)

df3 = df2.merge(df_genre, on='Genre', how='left')
df3.drop(columns=['Genre','Location', 'Active', 'Period', 'Count', 'website', 'Booking'], inplace=True)
df3.columns = ['Name', 'Type', 'Genre']
df3['Genre'] = df3['Genre'].str.split(',')
df3 = df3.explode('Genre').reset_index(drop=True)
df3['Genre'] = df3['Genre'].str.strip()
df3.drop_duplicates(subset=['Name', 'Type', 'Genre'], keep='first', inplace=True)
df3.dropna(inplace=True)
df3 = df3[df3['Genre'] != '']
df3 = df3.groupby(['Name','Type']).agg({'Genre': lambda x: ",".join(x)})

df_final = df3.merge(df1, on='Name', how='left')
df_final.sort_values("Name", inplace = True)  #, key=lambda col: col.str.lower())
df_final.rename(columns={'Genre_y':'Genre', 'Genre_x':'Substitute', 'website':'Website'}, inplace=True)
df_final['Substitute'] = df_final['Substitute'] + ','



####### Mapping coordinates from location

arc = ArcGIS()

df_final['Coordinates'] = df_final['Location'].apply(arc.geocode)
df_final['Latitude'] = df_final['Coordinates'].apply(lambda x: x.latitude if x!= None else None)
df_final['Longitude'] = df_final['Coordinates'].apply(lambda x: x.longitude if x!= None else None)

locations = df_final[['Latitude', 'Longitude']]
locationlist = locations.values.tolist()


df_final.to_csv('Rock Music/MTV_RockMusicFinal.csv')
df_final.tail()
df_final['Active']


####### Plotting map

html_popup = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<h4> %s </h4>
<a href="https://open.spotify.com/search/%s" target="_blank"><i class="fa fa-spotify" style="font-size:35px;color:#1ed760;"></i></a>
&nbsp&nbsp
<a href="https://www.youtube.com/results?search_query=%s" target="_blank"><i class="fa fa-youtube-play" style="font-size:35px;color:red;"></i></a>
&nbsp&nbsp
<a href = "https://music.apple.com/us/search?term=%s" target="_blank"><i class="fa fa-apple" style="font-size:35px;color:black;"></i></a><br>
Genres: %s <br><br>
<b><a href = "%s" target="_blank"> Website </a>
&nbsp●&nbsp
<a href = "%s" target="_blank"> Booking </a>
&nbsp●&nbsp
<a href = "https://www.rollingstone.com/results/#?q=%s" target="_blank"> News </a></b>
"""

icon_path = r'Rock Music/Icons/%s%s.png' 
# legend = 'Rock Music/Icons/Legend.png'

map = folium.Map(location=[40.866667, 34.566667], tiles = 'CartoDB dark_matter', zoom_start=2, min_zoom=1.5, max_bounds=True)

mcg = folium.plugins.MarkerCluster(control=False)
map.add_child(mcg)


fg_altmetal = folium.plugins.FeatureGroupSubGroup(mcg, 'Alternative Metal', show=False)
map.add_child(fg_altmetal)
fg_altrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Alternative Rock', show=False)
map.add_child(fg_altrock)
fg_blues = folium.plugins.FeatureGroupSubGroup(mcg, 'Blues', show=False)
map.add_child(fg_blues)
fg_bluesrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Blues Rock', show=False)
map.add_child(fg_bluesrock)
fg_classical = folium.plugins.FeatureGroupSubGroup(mcg, 'Classical', show=False)
map.add_child(fg_classical)
fg_country = folium.plugins.FeatureGroupSubGroup(mcg, 'Country', show=False)
map.add_child(fg_country)
fg_countryrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Country Rock', show=False)
map.add_child(fg_countryrock)
fg_disco = folium.plugins.FeatureGroupSubGroup(mcg, 'Disco', show=False)
map.add_child(fg_disco)
fg_elec = folium.plugins.FeatureGroupSubGroup(mcg, 'Electronic', show=False)
map.add_child(fg_elec)
fg_exprock = folium.plugins.FeatureGroupSubGroup(mcg, 'Experimental Rock', show=False)
map.add_child(fg_exprock)
fg_folk = folium.plugins.FeatureGroupSubGroup(mcg, 'Folk', show=False)
map.add_child(fg_folk)
fg_folkrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Folk Rock', show=False)
map.add_child(fg_folkrock)
fg_funk = folium.plugins.FeatureGroupSubGroup(mcg, 'Funk', show=False)
map.add_child(fg_funk)
fg_garagerock = folium.plugins.FeatureGroupSubGroup(mcg, 'Garage Rock', show=False)
map.add_child(fg_garagerock)
fg_hardrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Hard Rock', show=False)
map.add_child(fg_hardrock)
fg_hcpunk = folium.plugins.FeatureGroupSubGroup(mcg, 'Hardcore Punk', show=False)
map.add_child(fg_hcpunk)
fg_heavymetal = folium.plugins.FeatureGroupSubGroup(mcg, 'Heavy Metal', show=False)
map.add_child(fg_heavymetal)
fg_hiphop = folium.plugins.FeatureGroupSubGroup(mcg, 'Hip Hop', show=False)
map.add_child(fg_hiphop)
fg_indiepop = folium.plugins.FeatureGroupSubGroup(mcg, 'Indie Pop', show=False)
map.add_child(fg_indiepop)
fg_indierock = folium.plugins.FeatureGroupSubGroup(mcg, 'Indie Rock', show=False)
map.add_child(fg_indierock)
fg_jazz = folium.plugins.FeatureGroupSubGroup(mcg, 'Jazz', show=False)
map.add_child(fg_jazz)
fg_metal = folium.plugins.FeatureGroupSubGroup(mcg, 'Metal', show=False)
map.add_child(fg_metal)
fg_neopsy = folium.plugins.FeatureGroupSubGroup(mcg, 'Neo Psychedelia', show=False)
map.add_child(fg_neopsy)
fg_newwave = folium.plugins.FeatureGroupSubGroup(mcg, 'New Wave', show=False)
map.add_child(fg_newwave)
fg_pop = folium.plugins.FeatureGroupSubGroup(mcg, 'Pop', show=False)
map.add_child(fg_pop)
fg_poppunk = folium.plugins.FeatureGroupSubGroup(mcg, 'Pop Punk', show=False)
map.add_child(fg_poppunk)
fg_poprock = folium.plugins.FeatureGroupSubGroup(mcg, 'Pop Rock', show=False)
map.add_child(fg_poprock)
fg_postgrunge = folium.plugins.FeatureGroupSubGroup(mcg, 'Post Grunge', show=False)
map.add_child(fg_postgrunge)
fg_postpunk = folium.plugins.FeatureGroupSubGroup(mcg, 'Post Punk', show=False)
map.add_child(fg_postpunk)
fg_postrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Post Rock', show=False)
map.add_child(fg_postrock)
fg_progrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Progressive Rock', show=False)
map.add_child(fg_progrock)
fg_psy = folium.plugins.FeatureGroupSubGroup(mcg, 'Psychedelia', show=False)
map.add_child(fg_psy)
fg_psyrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Psychedelic Rock', show=False)
map.add_child(fg_psyrock)
fg_punkrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Punk Rock', show=False)
map.add_child(fg_punkrock)
fg_rnb = folium.plugins.FeatureGroupSubGroup(mcg, 'R&B', show=False)
map.add_child(fg_rnb)
fg_reggae = folium.plugins.FeatureGroupSubGroup(mcg, 'Reggae', show=False)
map.add_child(fg_reggae)
fg_rock = folium.plugins.FeatureGroupSubGroup(mcg, 'Rock', show=False)
map.add_child(fg_rock)
fg_rnr = folium.plugins.FeatureGroupSubGroup(mcg, 'Rock And Roll', show=False)
map.add_child(fg_rnr)
fg_softrock = folium.plugins.FeatureGroupSubGroup(mcg, 'Soft Rock', show=False)
map.add_child(fg_softrock)
fg_soul = folium.plugins.FeatureGroupSubGroup(mcg, 'Soul', show=False)
map.add_child(fg_soul)


genre_check = ['Alternative Metal,', 'Alternative Rock,', 'Blues,', 'Blues Rock,', 'Classical,', 'Country,', 'Country Rock,', 'Disco,', 'Electronic,', 'Experimental Rock,', 'Folk,', 'Folk Rock,', 'Funk,', 'Garage Rock,', 'Hard Rock,', 'Hardcore Punk,', 'Heavy Metal,', 'Hip Hop,', 'Indie Pop,', 'Indie Rock,', 'Jazz,', 'Metal,', 'Neo Psychedelia,', 'New Wave,', 'Pop,', 'Pop Punk,', 'Pop Rock,', 'Post Grunge,', 'Post Punk,', 'Post Rock,', 'Progressive Rock,', 'Psychedelia,', 'Psychedelic Rock,', 'Punk Rock,', 'R&B,', 'Reggae,', 'Rock,', 'Rock And Roll,', 'Soft Rock,', 'Soul,']
variables = [fg_altmetal, fg_altrock, fg_blues, fg_bluesrock, fg_classical, fg_country, fg_countryrock, fg_disco, fg_elec, fg_exprock, fg_folk, fg_folkrock, fg_funk, fg_garagerock, fg_hardrock, fg_hcpunk, fg_heavymetal, fg_hiphop, fg_indiepop, fg_indierock, fg_jazz, fg_metal, fg_neopsy, fg_newwave, fg_pop, fg_poppunk, fg_poprock, fg_postgrunge, fg_postpunk, fg_postrock, fg_progrock, fg_psy, fg_psyrock, fg_punkrock, fg_rnb, fg_reggae, fg_rock, fg_rnr, fg_softrock, fg_soul]

for point in range(0, len(locationlist)):
    for i in range(len(genre_check), 0, -1):
        for j in range(i-1, -1, -1):
            if genre_check[j] in df_final['Substitute'][point]:
                iframe_popup = folium.IFrame(html=html_popup % (df_final['Name'][point], df_final['Name'][point].replace(" ", '%20'), df_final['Name'][point].replace(" ", '+'), df_final['Name'][point].replace(" ", '%20'), df_final['Genre'][point], df_final['website'][point], df_final['Booking'][point], df_final['Name'][point].replace(" ", '%20')), width=240, height=185)
                tool = folium.Tooltip(text= df_final['Name'][point] + ' (' + df_final['Active'][point] + ')', style=("font-family: arial; font-size: 14px; padding: 10px;"), sticky= False)
                folium.Marker(locationlist[point], tooltip=tool,  popup=folium.Popup(iframe_popup), icon=folium.features.CustomIcon(icon_image=icon_path % (df_final['Type'][point], df_final['Period'][point]), icon_size=(32, 32))).add_to(variables[j])
            break


l = folium.LayerControl().add_to(map)
mini_map = folium.plugins.MiniMap(tile_layer='CartoDB dark_matter', width=125, height=125, toggle_display = True).add_to(map)
# search = folium.plugins.Search(mcg).add_to(map)


####HTML Legend

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Music Map</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 1440px; bottom: 20px;'>
     
<div class='legend-title'>Legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:#808080;opacity:0.8;'></span>1920</li>
    <li><span style='background:#990099;opacity:0.8;'></span>1930</li>
    <li><span style='background:#99ffcc;opacity:0.8;'></span>1940</li>
    <li><span style='background:#ffa500;opacity:0.8;'></span>1950</li>
    <li><span style='background:#ffc0cb;opacity:0.8;'></span>1960</li>
    <li><span style='background:#3333ff;opacity:0.8;'></span>1970</li>
    <li><span style='background:#ff0000;opacity:0.8;'></span>1980</li>
    <li><span style='background:#ffff00;opacity:0.8;'></span>1990</li>
    <li><span style='background:#00ff00;opacity:0.8;'></span>2000</li>
    <li><span style='background:#00cccc;opacity:0.8;'></span>2010</li>
  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
map.get_root().add_child(macro)

fname = 'Rock Music/MusicMap.html'
map.save(fname)

####Image Legend
# rose = """\
#     var rose = L.control({{position: 'bottomleft'}});

#     rose.onAdd = function (map) {{
#     var div = L.DomUtil.create('div', 'info rose');
#         div.innerHTML +=
#         '<img src="https://i.ibb.co/877rKX3/Legend.png" alt="rose" width="180px" height="220px">';
#     return div;
#     }};
#     rose.addTo({});""".format(map.get_name())


    

# def inject_code(fname, text):
#     with open(fname, 'r') as f:
#         lines = f.readlines()
#     end = 0
#     for k, line in enumerate(lines):
#         if '</script>' in line:
#             end = max(end, k)
#     lines.insert(end-1, rose)
    
#     with open(fname, 'w') as f:
#         f.writelines(lines)

# inject_code(fname, rose)
# inline_map(fname)

