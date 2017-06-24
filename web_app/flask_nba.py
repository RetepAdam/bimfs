
# import Flask
from flask import Flask, render_template, flash, request, session
from flask_appconfig import AppConfig
import webbrowser, threading, os
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
import scipy.stats as scs

# initialize the Flask app, note that all routing blocks use @app
app = Flask(__name__)  # instantiate a flask app object

Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
    '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

df_inputs = pd.read_csv('data/nba_inputs.csv')
df_comp = pd.read_csv('data/cbb_comp_list.csv')

df_comp = df_comp[df_comp['MP'] >= 500]
df_comp = df_comp[df_comp['To'] == 2017]

df_comp.reset_index(drop=True, inplace=True)

@app.route('/', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
def index():
    return render_template('index.html', options=list(df_inputs['Tm'].unique()))

@app.route('/players', methods=['GET', 'POST']) # if no methods specified, default is 'GET'
def players():
    team1 = request.values.get('sel_team')
    return render_template('players.html', selected=team1, options=list(df_inputs[df_inputs['Tm'] == team1]['Player']))

@app.route('/results', methods=['GET', 'POST']) # if no methods specified, default is 'GET'
def results():
    player1 = request.values.get('sel_player')
    nba_stats = np.array(df_inputs[df_inputs['Player'] == player1][df_inputs.columns[2:]])[0]

    probabilities = []

    for i in range(len(nba_stats)):
        comp_pred = np.load('numpy/2017_{0}_preds.npy'.format(i))
        comp_err = np.load('numpy/2017_{0}_yerr.npy'.format(i))
        comp_err = np.nan_to_num(comp_err)
        if i in [19, 20]:
            comp_proba = 1 - scs.norm.cdf((comp_pred - nba_stats[i]) / (.5 * comp_err))
        else:
            comp_proba = scs.norm.cdf((comp_pred - nba_stats[i]) / (.5 * comp_err))
        probabilities.append(comp_proba)

    for i in range(len(probabilities)):
        for j in range(len(probabilities[i])):
            probabilities[i][j] = round(probabilities[i][j], 2)

    labels = pd.DataFrame(np.array(df_comp['Player'].values), columns=['Player'])
    proba = pd.DataFrame(np.array(probabilities).T, columns=df_inputs.columns[2:])
    proba = proba.fillna(0)
    df_output = labels.merge(proba, left_index=True, right_index=True)
    sums = []
    for i in range(len(df_output)):
        sums.append(sum(df_output.iloc[i][1:]))

    df_output['Sum'] = sums
    df_output.sort_values('Sum', ascending=False, inplace=True)
    df_output.reset_index(drop=True, inplace=True)
    df_output.drop('Sum', axis=1, inplace=True)
    return render_template('results.html', selected_player=player1, to_replicate=nba_stats, ncaa_comps=df_output.to_html(index=False, classes='male'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
