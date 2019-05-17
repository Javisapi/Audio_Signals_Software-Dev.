import pandas as pd 
import librosa 
import numpy as np

import bokeh
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure, show


def read_json(json_data) -> pd.DataFrame:
    """
    Loads .json file and returns a pandas DataFrame
    Arguments:
        json_data: .json file
    Returns:
        df: pandas DataFrame
    """
    df = pd.read_json(json_data)

    # Test the format of the loaded .json file
    assert type(df) == pd.core.frame.DataFrame, 'The .json file must be loaded as a Pandas DataFrame'

    return df

def get_data(dir_path, filename) -> np.ndarray:
    """
    Loads .wav files and returns a numpy ndarray
    Arguments:
        dir_path: directory from where to load the .wav files
        filename: name of the .wav file to be loaded
    Returns:
        y: np.ndarray loaded with librosa
    """
    y, _ = librosa.core.load(dir_path + '/{}'.format(filename),
                            mono=True)

    # Test the format of the loaded .wav files
    assert type(y) == np.ndarray, 'The .wav files must be loaded as numpy ndarray'

    return y

#FIXME: threshold is manually passed. This can be automated by selecting the desired 
# number of peaks that the function must found in the signal. FFT can help in here. To be done.
def find_first_peak(df_rms, feat_value, feat_time, threshold = 0.02) -> np.float64:
    '''
    Threshold: value that determines the value of the first peak.
    Returns the time that corresponds to the first peak position.
    Arguments:
        df_rms: pd.DataFrame containing rms data from .json values
        feat_value: feature value
        feat_time: feature time
        threshold: float to indicate the threshold that detects peak value in signal.
    Returns:
        time at which the first peak appears
    '''
    series_values = df_rms[feat_value]

    # Test the type of the list_values
    assert type(series_values) == pd.core.series.Series, 'series_values Should be a Pandas Series'

    # Find values higher than threshold = 0.02 and select first of them
    idx = [ n for n, i in enumerate(series_values) if i> threshold ][0]

    # Test the type of the idx
    assert type(idx) == int, 'idx should be int'

    # Test the type of the output value    
    assert type(df_rms[feat_time][idx]) == np.float64, 'output must be numpy float64'
    

    return df_rms[feat_time][idx]


def plot_signal(df, df_rms, df_peaks, current_feature_name):
    """
    Generate the plot of one audio signal that will be passed to html
    Arguments:
        df: pandas DataFrame containing .wav channels values
        df_rms: pandas DataFrame containing rms values
        df_peaks: pandas DataFrame containing peaks values
        current_feature_name: str indicating the feature [Channel_1, Channel_2, Channel_3] to be plotted
    Returns:
        fig: bokeh figure
    """
    # Extract the number of the Channel
    channel_number = current_feature_name.split("_")[1]

    # Test the type and value of the channel_number
    assert type(channel_number) == str, 'Should be str'
    assert channel_number in ['1', '2', '3'], 'channel_number should be within 1 and 3, both included'

    # Select the time and value associated to the channel 
    # (as specified by current_feature_name) that will be plotted.
    feat_time = 'time_channel_{}'.format(channel_number)
    feat_value = 'value_channel_{}'.format(channel_number)

    # Define figure properties
    fig = figure(plot_width=800, plot_height=500, title= 'Audio file: ch-{}l.wav'.format(channel_number))

    # Plot .wav audio signal
    fig.line(list(df.index.values*2),
             list(df[current_feature_name].values),
             line_width = 1, 
             alpha = 1, 
             color = '#BE9300') 
    
    # Plot rms information of the audio Channel
    fig.line(list(df_rms[feat_time]*df.index.values.max()*2/df_rms[feat_time].max()),
             list(df_rms[feat_value])/df_rms[feat_value].max(),
             line_width = 2,
             alpha = 0.5, 
             color = 'black')

    # Add vertical lines
    feat_peak = 'peaks_channel_{}'.format(channel_number)
    peak_pos = df_peaks[feat_peak]  # Peaks position values as extracted from the JSON file.

    # Find first peak (time) position
    first_peak_pos = find_first_peak(df_rms, feat_value, feat_time, threshold=0.02)

    # Renormalize to the right scale the data
    refactor = first_peak_pos*1e-3*df.index.values.max()*2/(1.005*df_rms[feat_time].max())

    # Normalize peak positions
    norm_peak_pos = peak_pos*df.index.values.max()*refactor/peak_pos.max()

    # Top value of the vertical lines.
    bar_lengths= [1]*len(norm_peak_pos)  

    # Render the vertical bars, with bars at the specified x values
    fig.vbar(norm_peak_pos, bottom=-1, top=bar_lengths, width=15, color= '#00A9ED')

    # Background and grid lines colors
    fig.background_fill_color = '#E1E1E1'
    fig.xgrid.grid_line_color = 'white'
    fig.ygrid.grid_line_color = 'white'


    return fig

def generate_df_json_peaks(num_channels, df_json) -> pd.DataFrame:
    """
    Extract peak values from the given json data.
    Arguments:
        num_channels: number of channels == number of .wav files available
        df_json: pandas DataFrame containing .json data
    Return:
        df_peaks: pandas DataFrame containing the peaks values for 
                  each audio Channel.     
    """

    df_peaks = pd.DataFrame()
    for i in range(num_channels):
        column_peak = 'peaks_channel_{}'.format(i+1)
        data = pd.DataFrame({column_peak: df_json.peaks[i]})
        if df_peaks.empty:
            df_peaks = df_peaks.append(data, ignore_index= True)
        else:
            df_peaks = df_peaks.join(data)

    # Test output format of the generated df_peak
    assert type(df_peaks) == pd.DataFrame, 'df_peaks must be a pandas DataFrame'
    
    return df_peaks

def generate_df_json_rms(num_channels, df_json) -> pd.DataFrame:
    """
    Extract rms information (time and value) from the given json data.
    Arguments:
        num_channels: number of channels == number of .wav files available
        df_json: pandas DataFrame containing .json data
    Return:
        df_rms: pandas DataFrame containing the time and values for 
                each audio Channel.     
    """
    df_rms = pd.DataFrame()
    for i in range(num_channels):
        for column in ['time', 'value']:
            column_time = '{}_channel_{}'.format(column, i+1)
            data_time = pd.DataFrame({column_time: list(map(lambda x : x[column], df_json.rms[i]))})

            if df_rms.empty:
                df_rms = df_rms.append(data_time, ignore_index= True)
            else:
                df_rms = df_rms.join(data_time)
    
    # Test output format of the generated df_peak
    assert type(df_rms) == pd.DataFrame, 'df_rms must be a pandas DataFrame'
    
    return df_rms