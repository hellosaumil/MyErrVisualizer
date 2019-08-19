import requests,json, os
from flask import Flask, request, render_template, send_file, make_response, jsonify

from myErrVisualizer import MyErrVisualizer

app = Flask(__name__)
headers = {'Content-Type' : 'application/json'}

# @app.errorhandler(403)
# @app.errorhandler(404)
# @app.errorhandler(410)
# @app.errorhandler(500)
# def MyErrVisualizerErr(e):
#     return "\nDon't TRY AGAIN or else you will be BLOCKED!!!\n"

@app.route('/life', methods=["GET"])
def LiveGET():
    return json.dumps('I\'m Alive!')

@app.route('/', methods=["GET"])
def MyErrVisualizerGET():

    # return json.dumps("Welcome to MyErrVisualizer!")
    return render_template('index.html', name='13')


@app.route('/MyErrVisualizer', methods=["POST"])
def MyErrVisualizerPOST():

    os.system('clear')

    if request.method == "POST":
        json_dict = request.get_json()

        Traces, TracesLines = {}, []

        try:
            Traces = json_dict['Traces']

            print("="*10)
            print("Found Traces as follows: \n\n{}\n".format(Traces))
            print("="*10)


            TracesLines = Traces.split('\n')
            print("\nTracesLines: {}".format(TracesLines))


            myEV = MyErrVisualizer(TracesLines, cloud_mode=True)
            print("\nMyEV.Cloud_Output: {}".format(myEV.cloud_output))

            return jsonify(myEV.cloud_output)

        except:
            print("*** NO Traces could be Found, Aborting...")

            return """<html><body>
            Cannot Find 'Traces' field
            </body></html>"""

        return jsonify('correctData')

    else:
        return """<html><body>
        Invalid JSON Data
        </body></html>"""


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port,threaded=True,debug=True)
