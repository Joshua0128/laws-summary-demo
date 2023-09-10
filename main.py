from flask import Flask
from flask_cors import CORS

import api.get_result as get_result
import api.get_url as get_url

app = Flask(__name__)
CORS(app)

app.register_blueprint(get_result.bp)
app.register_blueprint(get_url.bp)

if __name__ == '__main__':
    app.run(port=80)
    