# from flask import current_app as app
#
# from langchain.agents import initialize_agent
# from langchain.llms import OpenAIChat
#
# from llama_index import GPTListIndex, GPTIndexMemory
#
# index = GPTListIndex([])
# llm = OpenAIChat(model_kwargs={"temperature": 0.5})
# memory = GPTIndexMemory(index=index, memory_key="chat_history", query_kwargs={"response_mode": "compact"})
# tools = []
# agent_chain = initialize_agent(tools, llm, agent_path="agent/chat_bot/agent.json", memory=memory)
#
# def l_chat_handler(cmd, msg, user_id, chat_id):
#     try:
#         # agent_chain = initialize_agent([], llm, agent="conversational-react-description", memory=memory)
#
#         # tools = load_tools(["python_repl"], llm=llm)
#
#         # agent_chain = initialize_agent([], llm, agent_path="lc://agents/zero-shot-react-description/agent.json", memory=memory)
#         return agent_chain.run(input=msg)
#     except Exception as e:
#         app.logger.error(e)
#         return "网络异常"
