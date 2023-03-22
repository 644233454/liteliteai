import json
import logging
import os
import re

import markdown
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

token = os.getenv("TEL_TOKEN")

md = markdown.Markdown(
    extensions=[
        'fenced_code',
        'abbr',
        'def_list',
        'footnotes',
        'tables'
    ],
    extension_configs={
        'fenced_code': {},
        'abbr': {},
        'def_list': {},
        'footnotes': {},
        'tables': {},
    }
)


def is_markdown(text):
    try:
        html = markdown.markdown(text)
        return True
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "msg": '帮助',
        "token": "telegram_bjkfhebxogdb",
        "chat_id": f"image_{update.effective_chat.id}",
        "user_id": update.message.from_user.id
    }

    response = requests.post("http://127.0.0.1:5000/chat", headers=headers, data=json.dumps(data))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text,
                                   reply_to_message_id=update.message.message_id)


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "msg": update.message.text,
        "token": "telegram_bjkfhebxogdb",
        "chat_id": f"image_{update.effective_chat.id}",
    }

    response = requests.post("http://127.0.0.1:5000/image", headers=headers, data=json.dumps(data))

    result = response.text
    logging.info(result)
    if result.startswith("![]("):
        pattern = r'!\[.*?\]\((.*?)\)'
        # 使用正则表达式模块re匹配链接URL
        urls = re.findall(pattern, result)
        logging.info(urls)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=urls[0],
                                     reply_to_message_id=update.message.message_id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result,
                                       reply_to_message_id=update.message.message_id)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "msg": update.message.text,
        "token": "telegram_bjkfhebxogdb",
        "chat_id": update.effective_chat.id,
        "user_id": update.message.from_user.id
    }

    response = requests.post("http://127.0.0.1:5000/chat", headers=headers, data=json.dumps(data))

    result = response.text
    logging.info(result)
    if result.startswith("![]("):
        pattern = r'!\[.*?\]\((.*?)\)'
        # 使用正则表达式模块re匹配链接URL
        urls = re.findall(pattern, result)
        logging.info(urls)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=urls[0],
                                     reply_to_message_id=update.message.message_id)
    else:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=re.escape(result).replace("\\ ", " ")
                                           .replace("\\\n", "\n").replace("!", "\!").replace("=", "\="),
                                           reply_to_message_id=update.message.message_id,
                                           parse_mode=ParseMode.MARKDOWN_V2)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=result,
                                           reply_to_message_id=update.message.message_id)
            pass


#
# async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     voice_file = await update.message.voice.get_file()
#
#     # 获取文件信息并下载文件
#     # file_path = voice_file.file_path
#     # print(file_path)
#     # urllib.request.urlretrieve(file_path, 'voice.mp3')
#
#     # 下载语音文件到本地
#     file_path = os.path.join(os.getcwd(), 'voice.oga')
#
#     await voice_file.download_to_drive(custom_path=file_path)
#
#
#     # 读取 OGA 文件
#     # sound = AudioSegment.from_file(file_path, format="ogg")
#     #
#     # file_path = os.path.join(os.getcwd(), 'voice.mp3')
#
#     # 将 OGA 文件转换为 MP3 格式
#     # sound.export(file_path, format="mp3")
#
#     # 发送回复消息
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     data = {
#         "file_path": file_path,
#         "token": "asdfhgdsfnsdb",
#         "chat_id": update.effective_chat.id
#     }
#
#     response = requests.post("http://127.0.0.1:12380/voice", headers=headers, data=json.dumps(data))
#
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text,
#                                    reply_to_message_id=update.message.message_id)


if __name__ == '__main__':
    # result = " ![](https://oaidalleapiprodscus.blob.core.windows.net/private/org-hlaTEbggCCVQCzEteX8SI3NE/user-fG0kMwZgi71Y3W9GqC3F6EAs/img-VvQMTM0HBJZ7auSGcgNGc48k.png?st=2023-03-05T10%3A11%3A29Z&se=2023-03-05T12%3A11%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-03-05T02%3A37%3A46Z&ske=2023-03-06T02%3A37%3A46Z&sks=b&skv=2021-08-06&sig=rBVLGpcwaMRtR9Vc5dvRbHidgxCE7xFDadOvkjk4xPE%3D)"
    # pattern = r'!\[.*?\]\((.*?)\)'
    # # 使用正则表达式模块re匹配链接URL
    # urls = re.findall(pattern, result)
    # print(urls[0])
    # result = "\n1. 句号 (.) \n2. 逗号 (,) \n3. 分号 (;) \n4. 冒号 (:) \n5. 感叹号 (!) \n6. 问号 (?) \n7. 引号 (\") \n8. 括号 () \n9. 方括号 [] \n10. 大括号 {} \n11. 连接号 (-) \n12. 下划线 (_) \n13. 斜杠 (/) \n14. 反斜杠 (\) \n15. 百分号 (%) \n16. 等于号 (=) \n17. 加号 (+) \n18. 减号 (-) \n19. 乘号 (*) \n20. 除号 (/)\n\n"
    # result = re.escape(result)
    # print(result)
    # result = result.replace("\\ ", " ").replace("\\\n", "\n").replace("!", "\!").replace("=", "\=")
    # # text_with_newlines = re.sub("\\", "", result)
    # print(result)

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    image_handler = CommandHandler('image', image)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # voice_handler = MessageHandler(filters.VOICE & (~filters.COMMAND), voice)

    application.add_handler(start_handler)
    application.add_handler(image_handler)
    application.add_handler(echo_handler)
    # application.add_handler(voice_handler)

    application.run_polling()
