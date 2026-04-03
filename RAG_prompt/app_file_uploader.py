'''
基于streamlit完成WEB网页上传服务

streamlit:当WEB页面元素发生变化（每次刷新），则代码重新执行一遍；要用st.session_state进行存储,不会随着页面的刷新而重置
'''
import streamlit as st     
from knowledge_base import KnowledgeBaseService
import time

#添加网页标题
st.title("知识库更新服务")

#file_uploader  文件上传框
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,              #false表示仅接受一个文件上传，多文件上传用True
)



#session_state就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()     #类对象只创建一次，不会随页面刷新频繁创建


if uploader_file is not None:
    #提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024      #提取KB的单位

    st.subheader(f"文件名：{file_name}")       #subheader为子标题 
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")  #在web网页显示普通文本，文字大小为正常大小
    
    #get_value -> bytes-> decode('utf-8')  转为字符串
    text = uploader_file.getvalue().decode("utf-8")  #获取文件的值


    with st.spinner("载入知识库中。。。。"):   #在spinner内的代码执行过程中，会有一个转圈动画（用于优化用户体验）
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)

# 测试代码  LHL
#     st.write(text)
#     st.session_state["counter"] +=1
# print(f'上传了{st.session_state["counter"]}个文件')

