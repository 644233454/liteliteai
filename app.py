import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sse import sse

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # 设置日志级别为INFO
    # app.logger.setLevel('INFO')
    app.logger.setLevel('DEBUG')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                        datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')
    # 创建RotatingFileHandler，将日志写入文件
    log_file = os.path.join(app.root_path, 'logs', 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 1024, backupCount=1, encoding="utf-8")
    file_handler.setLevel('INFO')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    app.config['SECRET_KEY'] = 'sadgnfysrtujfgjxbfgdgd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REDIS_URL'] = 'redis://192.167.2.176:6379'

    db.init_app(app)
    migrate.init_app(app, db)

    from service.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp)

    from index import index_bp
    app.register_blueprint(index_bp)

    app.app_context().push()

    app.register_blueprint(sse, url_prefix='/stream')

    return app


app = create_app()

# @app.route('/subscribe')
# def stream():
#     if "user_id" not in session:
#         return "用户未登录"
#     user_id = session['user_id']
#
#     chat_id = f"chat_user_{user_id}"
#     if 'chat_id' in request.json:
#         chat_id = request.json['chat_id']
#     # def event_stream():
#     #     # 消息生成函数
#     #     yield 'data: {"message": "Hello world"}\n\n'
#     # # 设置响应头
#     # return Response(event_stream(), mimetype='text/event-stream')
#     return sse.stream('hello', channel=chat_id)


if __name__ == '__main__':
    app.run()
