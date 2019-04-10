from flask import Flask, make_response, send_file, request
import os
import sys

app=Flask(__name__)

@app.route('/getfile/', defaults={'filename': ''})
@app.route("/getfile/<filename>")
def getfile(filename):
    """only suppprt file which in current work directory"""
    
    filename = filename or request.args.get('filename')  # get filename
    if len(filename) > 2 and filename[0] == '"' and filename[-1] == '"':
        filename = filename[1:-1]
        
    # check
    if not filename:
        # filename could be '',but should not be NoneType
        return 'file not specify', 403
    if not os.path.isfile(filename):
        return "file:<{}> not exist".format(filename), 404
    if not os.path.abspath(os.path.dirname(filename)).startswith(os.getcwd()):
        return "file:<{}> not exist".format(filename), 403

    # serve
    response = make_response(send_file(filename))
    basename = os.path.basename(filename)
    response.headers["Content-Disposition"] = "attachment;filename={};".format(basename.encode('utf8').decode('latin-1'))
    return response

if __name__ == "__main__":
    print('work on {}'.format(os.getcwd()))
    app.run(host="0.0.0.0", port=8008)
