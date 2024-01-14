from flask import Flask, request, render_template
from backend.bicre_api import execute_bicre

bicre = Flask(__name__)

# When the submit button is pressed, send a post to '/' that contains the start and end locations.
# Return a json array containing step objects (conversion from list of dict to json array of json objects 
# already handled by Flask)
@bicre.route('/', methods=['POST', 'GET'])
def retrieve_route():
    if request.method == 'POST':
        start = request.form['start_addr']
        end = request.form['end_addr']
        return execute_bicre(start, end)
    elif request.method == 'GET':
        return render_template('route_form.html')