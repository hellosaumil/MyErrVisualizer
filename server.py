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


def extra():
        try:
            os.system('clear')
            data = request.stream.read()
            print(data)

            print("\n***********")
            dataX = data.split("\r\n--------------------------")

            sharingType = dataX[0].split("name=\"")[1].split("\"")[1].split('\r\n\r\n')[1]
            fileName = dataX[1].split("name=\"")[1].split("\"")[1].split('\r\n\r\n')[1]

            print('\n**********')
            print("\n ",sharingType, "\n ",fileName)

            if sharingType == "download":
                Files = os.listdir(cloud_path)

                if fileName in Files:
                    print('\nSending File ' + fileName  + '...!')
                    print('\nFile Downloaded...!')
                    return send_file(cloud_path+fileName)
                else:
                    print('\nFile Not Found...!')
                    return json.dumps('INFC!!!')
                    # return send_file('')

            elif sharingType == "upload":
                data = dataX[2].split("name=\"")[2].split('\r\n\r\n')[1].split('\r\n\r\n')[0]
                print("\n ",data)

                print("\nFile Name : ",fileName)
                f = open(cloud_path+fileName, "w+")
                f.write(data)
                f.close()
                print("\nFile Written as ",fileName)
                return 'File Uploaded...!!!'

            elif sharingType == "remove":
                Files = os.listdir(cloud_path)

                print(Files)
                print(fileName, type(fileName))
                print(fileName in Files)

                if fileName in Files:
                    print('\nRemoving ' + fileName  + '...!')
                    os.remove(cloud_path+fileName)
                    print('\nFile Removed...!')
                    return json.dumps('File Removed...!')
                else:
                    print('\nFile Not Found...!')
                    return json.dumps('INFC!!!')
                    # return send_file('')

            elif sharingType == "removePaste":
                Files = os.listdir(cloud_path+'TextSharing/')

                print(Files)
                print(fileName, type(fileName))
                print(fileName in Files)

                if fileName in Files:
                    print('\nRemoving ' + fileName  + '...!')
                    os.remove(cloud_path+'TextSharing/'+fileName)
                    print('\nPaste Token File Removed...!')
                    return json.dumps('Paste Token Removed...')
                else:
                    print('\nFile Not Found...!')
                    return json.dumps('INFC!!!')
                    # return send_file('')

            elif sharingType == "copy":

                data = dataX[2].split("name=\"")[1].split('\r\n\r\n')[1]
                print("\n D :",data)

                print("\nFile Name : ",fileName)
                f = open(cloud_path+'TextSharing/'+fileName, "w+")
                f.write(data)
                f.close()

                print("\nSharing Text Written as ",fileName)
                return 'Sharing Text is Live...!!!'

            elif sharingType == "paste":
                Files = os.listdir(cloud_path+'TextSharing/')
                print(Files)

                if fileName in Files:
                    print('\nSending File ' + fileName  + '...!')
                    print('\nSharing Text Found...!')
                    return send_file(cloud_path+'TextSharing/'+fileName)
                else:
                    print('\nPasteToken Not Found...!')
                    return json.dumps('INFC!!!')
                    # return send_file('')

            else:
                return json.dumps("Couldn't Process your Request !!!")

        except:
            return json.dumps("Don't try to mess with me!!!\n")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090,threaded=True,debug=True)
