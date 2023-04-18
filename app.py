from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 개별 모듈에서 블루프린트 등록하는 곳
    from moviehome import mhcontroller
    app.register_blueprint(mhcontroller.mh)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080)