import uuid

import markdown
from flask import request, render_template, session, Blueprint, flash, redirect, url_for

import common
from app import db
from dbcommon.model import User, Message, ChatRoom

index_bp = Blueprint('index', __name__)


@index_bp.route('/', endpoint='index')
def index():
    return redirect(url_for('index.chatroom'))


@index_bp.route('/fotuo', endpoint='fotuo')
def fotuo():
    return render_template("fotuo.html")

@index_bp.route('/chatroom', endpoint='chatroom')
def chatroom():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        chat_id = request.args.get("chat_id")
        if chat_id is None:
            chat_id = f"chat_user_{user_id}"
            chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(1).first()
            if chat_room is None:
                chat_room = ChatRoom(user_id=user_id, chat_id=chat_id)
                db.session.add(chat_room)
                db.session.commit()
        else:
            chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(1).first()
            if chat_room is None:
                flash('AI应用不存在')
                return redirect(url_for('index.chat_rooms'))

        messages = Message.query.filter_by(user_id=user_id, chat_id=chat_id).order_by(Message.created_at.desc()).limit(
            20).all()
        if len(messages) == 0:
            messages.append(Message(role="assistant", content=common.help_msg,
                                    user_id=user_id, chat_id=chat_id))
        messages_data = [{'content': message.content, 'role': message.role} for message in
                         messages]
        messages_data = messages_data[::-1]

        return render_template("chat_room.html", user=user, chat_room=chat_room, messages=messages_data)
    else:
        return redirect(url_for('index.login'))


@index_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "":
            flash('用户名不能为空')
            return render_template('login.html', form=request.form)
        user = User.query.filter_by(username=username, password=password).first()
        # 开放注册
        # if user is None:
        #     user = User(username=username, password=password)
        #     dbcommon.session.add(user)
        #     dbcommon.session.commit()
        #     user = User.query.filter_by(username=username, password=password).first()

        if user is None:
            flash('用户名密码错误')
            return render_template('login.html', form=request.form)
        else:
            session['user_id'] = user.id
            return redirect(url_for('index.chat_rooms'))
    else:
        if 'user_id' in session:
            return redirect(url_for('index.chat_rooms'))
        else:
            return render_template("login.html")


@index_bp.route('/chat_rooms', endpoint='chat_rooms')
def chat_rooms():
    if "user_id" not in session:
        flash('用户未登录')
        return redirect(url_for('index.login'))
    user_id = session['user_id']
    chat_rooms = ChatRoom.query.filter_by(user_id=user_id).all()
    if len(chat_rooms) == 0:
        chatroom = ChatRoom(chat_id=f"chat_user_{user_id}", user_id=user_id)
        db.session.add(chatroom)
        db.session.commit()
        chat_rooms.append(chatroom)
    return render_template('chat_rooms.html', chat_rooms=chat_rooms)


@index_bp.route('/create_chatroom', methods=['GET'])
def create_chatroom():
    return render_template('create_chatroom.html')


@index_bp.route('/add_chatroom', methods=['POST'])
def add_chatroom():
    user_id = session['user_id']
    if user_id is None:
        flash('用户未登录')
        return redirect(url_for('index.login'))
    chat_title = request.form.get('chat_title')
    chat_id = f"chat_{str(uuid.uuid4())}"
    setting = request.form.get('setting')
    chatroom = ChatRoom(chat_title=chat_title, chat_id=chat_id, setting=setting, user_id=user_id)
    db.session.add(chatroom)
    db.session.commit()
    flash('AI应用已创建')
    return redirect(url_for('index.chat_rooms'))


@index_bp.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        # email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # 校验两次密码是否一致
        if password != confirm_password:
            flash('两次密码不匹配')
            return render_template('register.html', title='Register', form=request.form)
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            flash('用户已存在，请登录')
            return redirect(url_for('index.login'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        chat_id = f"chat_user_{user.id}"

        chat_setting = ChatRoom(user_id=user.id, chat_id=chat_id, chat_title="默认AI应用")
        db.session.add(chat_setting)

        db.session.commit()

        flash('注册成功')
        return redirect(url_for('index.login'))
    else:
        if 'user_id' in session:
            return redirect(url_for('index.chat_rooms'))
        else:
            return render_template("register.html")


@index_bp.route('/logout', endpoint='logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index.login'))
