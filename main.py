from flask import Flask
from flask_cors import CORS

import api.get_result as get_result

app = Flask(__name__)
CORS(app)
app.register_blueprint(get_result.bp)

if __name__ == '__main__':
    app.run()