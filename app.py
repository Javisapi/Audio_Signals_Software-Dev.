#! /usr/local/bin/python3
"""Main Flask app."""
import os
from flask import Flask, render_template, request
import pandas as pd 
from bokeh.embed import components


# Import auxiliary functions from aux.py
import aux

app = Flask(__name__)

""" Import some global variables """
dir_path = os.getcwd()  # Current path to work dir
file_names = ['Channel_1', 'Channel_2', 'Channel_3'] # Channels to rename the three input .wav files
num_channels = len(file_names) # Number of channels, corresponding to the number of input .wav files


@app.route("/", methods=['GET'])
def index():
    """Home page."""
    current_feature_name = request.args.get('feature_name')

    # If no Channel is passed on the http: address, 
    # then Channel_1 will be plotted by default.
    # That is by accessing: http://0.0.0.0:5090/
    # To pass a Channel in http, use the format: 
    # http://0.0.0.0:5090/?feature_name=Channel_2 to plot Channel_2
    if current_feature_name == None:
        current_feature_name = 'Channel_1'

    # Read json values converted to DataFrame style
    df_json = aux.read_json('data.json')

    # Generate dataframes from json file
    df_peaks = aux.generate_df_json_peaks(num_channels, df_json)
    df_rms = aux.generate_df_json_rms(num_channels, df_json)

    # Test the format of the two dataframes: df_peaks, df_rms
    assert type(df_peaks) == pd.core.frame.DataFrame, 'df_peaks must be a Pandas DataFrame'
    assert type(df_rms) == pd.core.frame.DataFrame, 'df_rms must be a Pandas DataFrame'


    ########## FIXME: TO BE OPTIMIZED! #########################
    ####### Hardcoded ... ######################################
    signal_1 = aux.get_data(dir_path, 'ch-1l.wav')
    signal_2 = aux.get_data(dir_path, 'ch-2l.wav')
    signal_3 = aux.get_data(dir_path, 'ch-3l.wav')

    df_signal_1 = pd.DataFrame(signal_1)
    df_signal_1.columns = ['Channel_1']

    df_signal_2 = pd.DataFrame(signal_2)
    df_signal_2.columns = ['Channel_2']

    df_signal_3 = pd.DataFrame(signal_3)
    df_signal_3.columns = ['Channel_3']

    df_signals = pd.concat([df_signal_1, df_signal_2, df_signal_3], axis=1, sort=False)
    ############################################################

    # Generate figure to be displayed
    audio_fig = aux.plot_signal(df_signals, df_rms, df_peaks, current_feature_name)

    # Embed the plot in the html
    script, div = components(audio_fig)

    # Test the format of the embeded plot components and other features
    # that will be passed to the html file
    assert type(div) == str, 'div must be a str'
    assert type(script) == str, 'script must be a str'
    assert type(file_names) == list, 'file_names must be a list'
    assert type(current_feature_name) == str, 'current_feature_name must be a str'
        
    # Return template and pass it to index.html 
    return render_template('index.html',
                             script = script, 
                             div = div, 
                             feature_names = file_names, 
                             current_feature_name=current_feature_name)
    


if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5090, debug=True)
