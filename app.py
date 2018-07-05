from flask import Flask, render_template
# import os

app = Flask(__name__)


@app.route('/plot/')
def plot():
    from IPython.core.display import display, HTML
    from string import Template
    import pandas as pd
    import json

    # d3js = HTML('<script src="d3_jupyter/lib/d3/d3.min.js"></script>')

    worldmap_data = json.loads(open('data/worldmap.json', 'r').read())
    sites_data_stations = pd.read_csv('data/stations.csv')
    sites_data_temps = pd.read_csv('data/monthly_temps.csv')
    sites_data_temps = sites_data_temps.sort_values(by='ID')

    temps_by_ID = []
    previous_ID = -1
    collected_temps = {}
    for i,row in sites_data_temps.iterrows():
        if (row['ID'] != previous_ID) and (previous_ID != -1):
            temps_by_ID.append(collected_temps)
            collected_temps = {}
        collected_temps[row['month']] = {'ave': row['ave'], 
                                        'max': row['max'], 
                                        'min': row['min']}
        previous_ID = row['ID']
    temps_by_ID.append(collected_temps)
    site_data_temps_2 = pd.DataFrame({'ID': sites_data_temps['ID'].unique(), 
                                    'temps': temps_by_ID})
    # site_data_temps_2.head()
    
    sites_data = pd.merge(sites_data_stations, site_data_temps_2, on='ID')
    sites_data_dict = sites_data.to_dict(orient='records')

    # html_template = Template('''
    # <style> $css_text </style>
    # <div><svg width="700" height="500px" id="graph-svg"></svg></div>
    # <script> $js_text </script>
    # ''')

    css_text = open('static/temperature_histories.css','r').read()
    js_text_template = Template(open('static/temperature_histories.js','r').read())
    js_text = js_text_template.safe_substitute({'worldmapdata': json.dumps(worldmap_data), 
                                            'sitesdata': json.dumps(sites_data_dict) })
    # display(HTML(html_template.substitute({'css_text': css_text, 'js_text': js_text})))
    return render_template("plot.html", 
    css_text=css_text,
    js_text=js_text)

if __name__ == '__main__':
    app.run(debug=True)
