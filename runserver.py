import os
from angular_flask import app


def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    runserver()
