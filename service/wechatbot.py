import io
from concurrent.futures import ThreadPoolExecutor

import itchat



import json
import logging

import requests
from itchat.content import TEXT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
thread_pool = ThreadPoolExecutor(max_workers=2)


if __name__ == '__main__':
    # login by scan QRCode
    itchat.auto_login(enableCmdQR=2)

    # start message listener
    itchat.run()


@itchat.msg_register(TEXT)
def handler_single_msg(msg):
    handle(msg)
    return None


# @itchat.msg_register(TEXT, isGroupChat=True)
# def handler_group_msg(msg):
#     handle_group(msg)
#     return None

def handle(msg):
    logging.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    from_user_id = msg['FromUserName']
    to_user_id = msg['ToUserName']              # 接收人id
    other_user_id = msg['User']['UserName']     # 对手方id
    content = msg['Text']
    if from_user_id == other_user_id:
        thread_pool.submit(_do_send, content, from_user_id)

    # elif to_user_id == other_user_id and match_prefix:
    #     # 自己给好友发送消息
    #     str_list = content.split(match_prefix, 1)
    #     if len(str_list) == 2:
    #         content = str_list[1].strip()
    #     img_match_prefix = self.check_prefix(content, conf().get('image_create_prefix'))
    #     if img_match_prefix:
    #         content = content.split(img_match_prefix, 1)[1].strip()
    #         thread_pool.submit(self._do_send_img, content, to_user_id)
    #     else:
    #         thread_pool.submit(self._do_send, content, to_user_id)


# def handle_group(self, msg):
#     logging.debug("[WX]receive group msg: " + json.dumps(msg, ensure_ascii=False))
#     group_name = msg['User'].get('NickName', None)
#     group_id = msg['User'].get('UserName', None)
#     if not group_name:
#         return ""
#     origin_content = msg['Content']
#     content = msg['Content']
#     content_list = content.split(' ', 1)
#     context_special_list = content.split('\u2005', 1)
#     if len(context_special_list) == 2:
#         content = context_special_list[1]
#     elif len(content_list) == 2:
#         content = content_list[1]
# 
#     config = conf()
#     match_prefix = (msg['IsAt'] and not config.get("group_at_off", False)) or self.check_prefix(origin_content, config.get('group_chat_prefix')) \
#                    or self.check_contain(origin_content, config.get('group_chat_keyword'))
#     if ('ALL_GROUP' in config.get('group_name_white_list') or group_name in config.get('group_name_white_list') or self.check_contain(group_name, config.get('group_name_keyword_white_list'))) and match_prefix:
#         img_match_prefix = self.check_prefix(content, conf().get('image_create_prefix'))
#         if img_match_prefix:
#             content = content.split(img_match_prefix, 1)[1].strip()
#             thread_pool.submit(self._do_send_img, content, group_id)
#         else:
#             thread_pool.submit(self._do_send_group, content, msg)

def send(msg, receiver):
    logging.info('[WX] sendMsg={}, receiver={}'.format(msg, receiver))
    itchat.send(msg, toUserName=receiver)

def _do_send(msg, reply_user_id):
    try:
        if not msg:
            return
        reply_text = build_reply_content(msg, reply_user_id)
        if reply_text:
            send(reply_text, reply_user_id)
    except Exception as e:
        logging.exception(e)

def _do_send_img(query, reply_user_id):
    try:
        if not query:
            return
        context = dict()
        context['type'] = 'IMAGE_CREATE'
        img_url = build_reply_content(query, context)
        if not img_url:
            return

        # 图片下载
        pic_res = requests.get(img_url, stream=True)
        image_storage = io.BytesIO()
        for block in pic_res.iter_content(1024):
            image_storage.write(block)
        image_storage.seek(0)

        # 图片发送
        logging.info('[WX] sendImage, receiver={}'.format(reply_user_id))
        itchat.send_image(image_storage, reply_user_id)
    except Exception as e:
        logging.exception(e)

# def _do_send_group(self, query, msg):
#     if not query:
#         return
#     context = dict()
#     context['from_user_id'] = msg['ActualUserName']
#     reply_text = super().build_reply_content(query, context)
#     if reply_text:
#         reply_text = '@' + msg['ActualNickName'] + ' ' + reply_text.strip()
#         self.send(conf().get("group_chat_reply_prefix", "") + reply_text, msg['User']['UserName'])

def build_reply_content(msg,chat_id):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "msg": msg,
        "token": "wechat_bjkfhebxogdb",
        "chat_id": chat_id,
    }

    response = requests.post("http://127.0.0.1:12380/chat", headers=headers, data=json.dumps(data))

    result = response.text
    logging.info(result)
    return result
