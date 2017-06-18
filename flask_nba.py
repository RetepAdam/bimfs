
# import Flask
from flask import Flask, render_template, flash, request, session
from flask_appconfig import AppConfig
import webbrowser, threading, os
from flask_bootstrap import Bootstrap
import pandas as pd

# initialize the Flask app, note that all routing blocks use @app
app = Flask(__name__)  # instantiate a flask app object

Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
    '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

df = pd.read_csv('data/nba_inputs.csv')

@app.route('/', methods = ['GET', 'POST'])  # GET is the default, more about GET and POST below
def index():
    return render_template('index.html', options=list(df['Tm'].unique()))

@app.route('/players', methods=['GET', 'POST']) # if no methods specified, default is 'GET'
def players():
    team1 = request.values.get('sel_team')
    return render_template('players.html', selected=team1, options=list(df[df['Tm'] == team1]['Player']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# @app.route('/input')
# def results():
#     file_arr = data_names(data_path, data_type)
#     return render_template( 'input.html', count_file = file_arr,
#                             p_file = file_arr, plot_type = avail_figure,
#                             p_value = p_possible)
#
# @app.route("/visualize", methods=['POST'])
# def visualize():
#     graph = request.form['graph_type']
#     highest_p = float(request.form['p_return'])
#     img_arr = image_names(image_path)
#     #only special graph
#
#     if graph == avail_figure[-1]:
#         df, sample_lst, gene_lst, df2 = get_dataframe_and_axes( os.path.join('data',request.form['file_1']),
#                                                                 os.path.join('data',request.form['file_2']), 'Gene ID',
#                                                                 highest_p)
#         heatmap = make_heatmap_object(  df, sample_lst,
#                                         gene_lst,df2)
#     else:
#         print('Unable to plot Volcano')
#     js_resources = INLINE.render_js()
#     css_resources = INLINE.render_css()
#     # note that heapmap below is defined under if-name-main block
#     script, div = components(heatmap)
#
#     html = render_template(
#         'visualize.html',
#         plot_script=script,
#         plot_div=div,
#         js_resources=js_resources,
#         css_resources=css_resources,
#         img_list = img_arr,
#         img_path = image_path
#         )
#     return encode_utf8(html)
#
# # maybe make a landing page with redirect to data enter page.
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
# # about page
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# # contact page
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')
#
# if __name__ == '__main__':
#     #configs
#     avail_figure = [ 'Volcano','Heatmap']
#     data_path ='data'
#     data_type = '.csv'
#     image_path = 'static/fig'
#     max_num = 200
#     p_possible = [.05, .04, .03, .02, .01]
#     # threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
#     app.run('0.0.0.0', port=8000)
