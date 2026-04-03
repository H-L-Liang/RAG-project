import time
import streamlit as st
from rag import RagService
import config_data as config

#用户聊天页面创建  终端运行： cd C:\Users\LHL\Desktop\RAG_prompt    streamlit run app_qa.py

#标题
st.title("智能客服")
st.divider()   #分隔符



if "message" not in st.session_state:  #字典里面没有代表第一次跑
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])  #不断将历史记录for循环出来

#在页面最下方提供用户输入蓝
prompt = st.chat_input()


if prompt:
    #在页面输入用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list = []
    with st.chat_message("assistant"):
        res_stream = st.session_state["rag"].chain.stream({"input":prompt},config.session_config)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.write_stream(capture(res_stream,ai_res_list))
    st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})
#["a","b","c"]  "".join(list)  ->abc  LHL
#["a","b","c"]  ",".join(list)  ->a,b,b
