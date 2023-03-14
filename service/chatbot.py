import json
import os
import platform
from concurrent.futures import ThreadPoolExecutor

import nltk
import openai
from flask import current_app as app
from flask import request, session, Blueprint
from flask_sse import sse
from openai import InvalidRequestError

import common
from app import db
from dbcommon import Message, ChatRoom

openai.organization = "org-hlaTEbggCCVQCzEteX8SI3NE"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_chat_model = "gpt-3.5-turbo"

if platform.system() != 'Linux':
    openai.proxy = common.proxies
    nltk.set_proxy(f'socks5://{common.proxy_host}:{common.proxy_port}')

chatbot_bp = Blueprint('chatbot', __name__)


executor = ThreadPoolExecutor(max_workers=2)


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    msg = request.json['msg']

    if 'token' in request.json:
        if request.json['token'] == "telegram_bjkfhebxogdb":
            session['user_id'] = 0
        if request.json['token'] == "asdfhgdsfnsdb":
            session['user_id'] = -1

    if "user_id" not in session:
        return "用户未登录"
    user_id = session['user_id']

    chat_id = f"chat_user_{user_id}"
    if 'chat_id' in request.json:
        chat_id = request.json['chat_id']

    parts = msg.split(" ", 1)
    cmd = parts[0]
    msg = parts[1] if len(parts) > 1 else ""
    result = handle_command(cmd, msg, user_id, chat_id)
    return result


def handle_command(cmd, msg, user_id, chat_id):
    commands = {
        "设置风格": setting_handler,
        "图片": image_handler,
        "关机": stop_handler,
        "开机": start_handler,
        # "网页": web_handler,
        # "聊天": l_chat_handler,
        "帮助": help_handler,
        "菜单": help_handler
    }

    handler = commands.get(cmd, chat_handler)
    return handler(cmd, msg, user_id, chat_id)


def chat_handler(cmd, msg, user_id, chat_id):
    chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(
        1).first()
    if chat_room is None:
        chat_room = ChatRoom(user_id=user_id, chat_id=chat_id)
        db.session.add(chat_room)
    if chat_room.status == 0:
        return ""

    msg = cmd + msg
    try:
        send_msg = Message(role="user", content=msg, user_id=user_id, chat_id=chat_id)
        db.session.add(send_msg)
        system_prompt = ""
        if chat_room.setting is not None:
            system_prompt = chat_room.setting
        messages = loadMessage(user_id, chat_id, 80, system_prompt)

        # result = generate_text(messages)
        if user_id == 0:
            result = generate_text(messages)
        else:
            result = generate_text_stream(messages)
        db.session.commit()
        return result
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        return "网络异常"
    finally:
        db.session.close()


def image_handler(cmd, msg, user_id, chat_id):
    result = "网络异常"
    image_chat_id = f"image_{chat_id}"
    try:
        # 翻译文本
        trans_msg = Message(role="user", content=f"Translate the text into English：{msg}",
                            user_id=user_id, chat_id=image_chat_id)
        messages = [
            trans_msg
        ]
        db.session.add(trans_msg)
        trans_result = generate_text(messages)

        # 用于生成提示词的消息
        prompt_msg = Message(role="user", content=f"{trans_result}",
                             user_id=user_id, chat_id=image_chat_id)
        db.session.add(prompt_msg)
        messages = [
            Message(role="system",
                    content="You are a prompt generation assistant that extends received text to 50 words, "
                            "extracts adjectives and nouns, and expands them into multiple prompts separated "
                            "by spaces before sending them to me. Your replies only contain processed "
                            "prompts without any additional explanations.",
                    user_id=user_id, chat_id=image_chat_id),
            prompt_msg
        ]
        result = generate_text(messages)
        # 用于生成图片的消息
        img_msg = Message(role="user", content=result, user_id=user_id, chat_id=image_chat_id)
        db.session.add(img_msg)
        result = generate_image(img_msg)
        db.session.commit()
        return f"![]({result})"
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        return result
    finally:
        db.session.close()


#
@chatbot_bp.route('/image', methods=['POST'])
def image():
    msg = request.json['msg']

    if 'token' in request.json:
        if request.json['token'] == "telegram_bjkfhebxogdb":
            session['user_id'] = 0
        if request.json['token'] == "asdfhgdsfnsdb":
            session['user_id'] = -1
    if "user_id" not in session:
        return "用户未登录"
    user_id = session['user_id']

    try:
        with db.session.no_autoflush:
            image_chat_id = f"image_chat_user_{user_id}"
            img_msg = Message(role="user", content=msg, user_id=user_id, chat_id=image_chat_id)
            db.session.add(img_msg)
            result = generate_image(img_msg)
        db.session.commit()
        return result
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


# @chatbot_bp.route('/voice', methods=['POST'])
# def voice():
# if 'file' not in request.files:
#     return 'No file uploaded', 400
# file = request.files['file']
# file.save('/path/to/save/file.mp3')
# return 'File uploaded successfully'
# file_path = request.json['file_path']
#
# if 'token' in request.json and request.json['token'] == "asdfhgdsfnsdb":
#     session['user_id'] = 0
# if "user_id" not in session:
#     return "用户未登录"
# user_id = session['user_id']
#
# return audio_parser(file_path)


def loadMessage(user_id, chat_id, limit, system_prompt):
    messages = Message.query.filter_by(user_id=user_id, chat_id=chat_id).order_by(Message.created_at.desc()).limit(
        limit).all()
    messages = messages[::-1]
    prompts = system_prompt.split("|||")
    for prompt in prompts:
        system_msg = Message(role="system", content=prompt, user_id=user_id, chat_id=chat_id)
        messages.insert(-1, system_msg)
    messages_data = [{'role': message.role, 'content': message.content} for message in messages]

    message_lengths = common.num_tokens_from_messages(messages_data)
    app.logger.info(f"消息长度 {message_lengths}  limit:{limit}")
    if message_lengths > 3596:
        return loadMessage(user_id, chat_id, limit - 2, system_prompt)
    return messages


def generate_text(messages):
    messages_data = [{'role': message.role, 'content': message.content} for message in messages]

    app.logger.info(json.dumps(messages_data, ensure_ascii=False))

    user_id = messages[0].user_id
    chat_id = messages[0].chat_id
    try:
        responses = openai.ChatCompletion.create(
            model=openai_chat_model,
            messages=messages_data,
            user=f"{chat_id}",
            temperature=0.5
        )
    except InvalidRequestError as e:
        app.logger.error(e)
        if e.http_status != 200:
            if e.code == "context_length_exceeded":
                return generate_text(messages[1:])
            responses = openai.ChatCompletion.create(
                model=openai_chat_model,
                messages=messages_data,
                user=f"{chat_id}",
                temperature=0.5
            )
        pass
    except Exception as e:
        app.logger.error(e)
        return "网络异常，请重试"

    assistant = responses.choices[0]['message']
    message = Message(role="assistant", content=assistant['content'], user_id=user_id, chat_id=chat_id)
    db.session.add(message)
    return assistant['content'].strip()


def generate_text_stream(messages):
    messages_data = [{'role': message.role, 'content': message.content} for message in messages]

    app.logger.info(json.dumps(messages_data, ensure_ascii=False))

    user_id = messages[0].user_id
    chat_id = messages[0].chat_id
    executor.submit(long_running_task, app.app_context(), messages_data, user_id, chat_id)
    # pool = ThreadPool(processes=1)
    # pool.apply_async(long_running_task, args=(app.app_context(), messages_data, user_id, chat_id))
    return ''


def long_running_task(app_context, messages_data, user_id, chat_id):
    with app_context:
        try:
            responses = openai.ChatCompletion.create(
                model=openai_chat_model,
                messages=messages_data,
                user=f"{chat_id}",
                temperature=0.5,
                stream=True
            )
            response_str = ''
            for response_json in responses:
                choice = response_json['choices'][0]
                if choice['finish_reason'] == 'stop':
                    break
                # error handling
                if choice['finish_reason'] == 'length':
                    # sse.publish(chat_id, data='内容过长', event='user_' + user_id)
                    # sse.publish({"message": "内容过长"}, type='chat', channel=chat_id)
                    break

                if 'gpt-3.5-turbo' in openai_chat_model:
                    delta = choice['delta']
                    if "role" in delta or delta == {}:
                        char = ''
                    else:
                        char = delta['content']
                else:
                    char = choice['text']

                sse.publish({"message": char}, type='chat', channel=chat_id)
                app.logger.info(char)

                response_str += char
            message = Message(role="assistant", content=response_str, user_id=user_id, chat_id=chat_id)
            db.session.add(message)
            db.session.commit()
        except InvalidRequestError as e:
            app.logger.error(e)
            pass
        except Exception as e:
            app.logger.error(e)
        pass


def generate_image(msg):
    app.logger.info(json.dumps(msg.content, ensure_ascii=False))
    try:
        responses = openai.Image.create(
            prompt=msg.content,
            n=1,
            size="512x512"
        )
    except InvalidRequestError as e:
        app.logger.error(e)
        if 'safety system' in e.user_message:
            return "敏感词警告！！！"
        return "网络异常，请重试"
    except Exception as e:
        app.logger.error(e)
        return "网络异常，请重试"

    result = responses.data[0].url
    db.session.add(Message(role="assistant", content=result, user_id=msg.user_id, chat_id=msg.chat_id))
    app.logger.info(responses)
    return result


def read_voice(file_path):
    app.logger.info(file_path)
    try:
        result = openai.Audio.transcribe(
            file=open(file_path, 'r', errors='ignore'),
            model='whisper-1',  # 使用的模型，可选参数
        )
    except Exception as e:
        app.logger.error(e)
        return "网络异常，请重试"

    return result.data[0].text


def help_handler(cmd, msg, user_id, chat_id):
    return common.help_msg


def setting_handler(cmd, msg, user_id, chat_id):
    try:
        chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(
            1).first()
        if chat_room is None:
            chat_room = ChatRoom(user_id=user_id, chat_id=chat_id)
            db.session.add(chat_room)

        chat_room.setting = msg
        db.session.commit()
        return f"好的，已设置风格为：{msg}" if len(msg) > 0 else "好的，已取消风格设置"
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        return "网络异常"
    finally:
        db.session.close()


def stop_handler(cmd, msg, user_id, chat_id):
    try:
        chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(
            1).first()
        if chat_room is None:
            chat_room = ChatRoom(user_id=user_id, chat_id=chat_id)
            db.session.add(chat_room)

        chat_room.status = 0
        db.session.commit()
        return "已关机"
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        return "网络异常"
    finally:
        db.session.close()


def start_handler(cmd, msg, user_id, chat_id):
    try:
        chat_room = ChatRoom.query.filter_by(user_id=user_id, chat_id=chat_id).limit(
            1).first()
        if chat_room is None:
            chat_room = ChatRoom(user_id=user_id, chat_id=chat_id)
            db.session.add(chat_room)

        chat_room.status = 1
        db.session.commit()
        return "已开机"
    except Exception as e:
        db.session.rollback()
        app.logger.error(e)
        return "网络异常"
    finally:
        db.session.close()
