import markdown
import tiktoken


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise


# import os
# os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'

# from llama_index import GPTSimpleVectorIndex, StringIterableReader
# messages = Message.query.filter_by(user_id=2, chat_id="chat_user_2").order_by(Message.created_at.desc()).limit(
#         100).all()
#
# data = [message.content for message in messages]
# documents = StringIterableReader().load_data(data)
# # documents = SimpleDirectoryReader('data').load_data()
# index = GPTSimpleVectorIndex(documents)
#
# # save to disk
# index.save_to_disk('index.json')
# # load from disk
# index = GPTSimpleVectorIndex.load_from_disk('index.json')
#
# index.query("你好?")
