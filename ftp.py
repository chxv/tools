"""
run
    $ pip install flask
    $ python ftp.py
"""

from flask import Flask, make_response, send_file, request, current_app
import os
import sys
import getopt

app = Flask(__name__)


@app.route('/', defaults={'filename': ''})
@app.route("/<filename>")
def index(filename):
    filename = filename or request.args.get('filename')  # get filename
    if filename and len(filename) > 2 and filename[0] == '"' and filename[-1] == '"':
        filename = filename[1:-1]
    filename = xss_filter(filename)
    return getfile(filename)


@app.errorhandler(404)
def not_found(e):
    """find file in sub dir"""
    filename = request.path.strip('/')
    filename = xss_filter(filename)
    return getfile(filename)


def getfile(filename):
    """only support file which in current work directory"""
    # check filename type
    if not filename or not isinstance(filename, str):
        # filename could be '',but should not be NoneType
        return 'File Not Specify', 403
    if os.path.isabs(filename):
        return 'File " {} " Not Exist'.format(filename), 403

    # check permission
    # forbidden first to avoid file existence exposed
    # convert filename to abspath, because access file relative to . by default
    work_dir = current_app.config.setdefault('work_dir', os.getcwd())
    abs_file = os.path.join(work_dir, filename)
    abs_file = os.path.join(
        os.path.abspath(os.path.dirname(abs_file)),
        os.path.basename(filename)
    )
    if not abs_file.startswith(work_dir):
        return 'File " {} " Not Exist'.format(filename), 403

    # check existence: file is exist
    if not os.path.isfile(abs_file):
        return 'File " {} " Not Found'.format(filename), 404

    # serve
    response = make_response(send_file(abs_file))
    basename = os.path.basename(abs_file)
    response.headers["Content-Disposition"] = "attachment;filename={};".format(
        basename.encode('utf8').decode('latin-1')
    )
    return response


def xss_filter(filename: str):
    if not isinstance(filename, str):
        return ""
    filename = filename.replace('<', '&lt;')
    filename = filename.replace('>', '&gt;')
    return filename


def check_args(_work_dir, _host, _port):
    """ check args """
    # check work dir
    if not os.path.isdir(_work_dir):
        return False

    # check port
    if not isinstance(_port, int) or _port > 65535 or _port < 0:
        return False

    # check host
    h = _host.split('.')
    if len(h) != 4:
        return False
    for i in h:
        if not i.isdigit() or int(i) > 255:
            return False

    # all args are valid
    return True


def print_help():
    if sys.version_info.major >= 3:
        print("""
    ftp based on flask.
    ----
    example:
        python ftp.py --host=0.0.0.0 --port=80 .
        """)
    else:
        eval('print "please upgrade to python 3"')


def main():
    work_dir, host, port = '.', '0.0.0.0', 5000
    if len(sys.argv) == 1:
        pass
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["host=", "port="])
        # dir
        if len(args) == 0:
            pass
        elif len(args) == 1:
            work_dir = args[0]
        else:
            print('[-] too much work dir specified, please check it')
            print_help()
            exit(0)
        # host, port
        for o, a in opts:
            if o == '--host':
                host = a
            elif o == '--port':
                port = int(a)
    except getopt.GetoptError:
        print('[-] argv error, please check it')
        print_help()
        exit(0)
    if not check_args(work_dir, host, port):
        print('[-] invalid argv, please check it')
        print_help()
        exit(0)
    work_dir = os.path.abspath(work_dir)
    app.config.update({'work_dir': work_dir})
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
