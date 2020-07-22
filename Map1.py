import folium
import pandas

data = pandas.read_csv("original.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
myhtml = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_prod(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 < elevation < 3000:
        return 'orange'
    else:
        return 'red'    

map = folium.Map(location=[45.950014, -66.642673], zoom_start=10, tiles="Stamen Terrain")

featureGroupVol = folium.FeatureGroup(name="Volcanos")
for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=myhtml % (nm, nm, el), width=250, height=135)
    featureGroupVol.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe),
     fill_color=color_prod(el),color='grey', fill_opacity=0.7))
    
featureGroupPop = folium.FeatureGroup(name="Population")   
featureGroupPop.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda parameter_list: {'fillColor':'green' if parameter_list['properties']['POP2005']<10000000 
else 'orange' if 10000000 <= parameter_list['properties']['POP2005'] <20000000 else 'red'}))

    
map.add_child(featureGroupVol)
map.add_child(featureGroupPop)
map.add_child(folium.LayerControl())

map.save("Map1.html")