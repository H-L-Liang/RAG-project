from xml.dom.minidom import Document
from vector_stores import VectorStoreServices
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough,RunnableWithMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

# 在线检索功能。把向量解锁的对象、提示词模板、模型三者组装在一快，
# 通过私有的__get_chain方法把向量检索的检索器封装到链（chain）里面去，
# 用户的提问既能够想模型提问还能够带有参考资料，
# 拿到参考资料再组装成新的提示词再去喂模型获得模型结果，实现在线结果功能

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)

    return prompt


class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreServices(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name )
        )  #向量服务类的实例对象
        
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已参考资料为主，" 
                "简洁和专业的回答用户问题。参考资料：{context}。"),
                ("system","并且我提供用户的对话历史记录如下"),
                MessagesPlaceholder("history"),  #注入的history 的key
                ("user","请回答用户问题：{input}")
            ]
        ) #提示词模板
        
        self.chat_model = ChatTongyi(model=config.chat_model_name)
        
        self.chain = self.__get_chain()        

    def __get_chain(self):
        '''获取最终的执行链'''
        retriever = self.vector_service.get_retriever()    #获取检索器对象


        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str
        def format_for_retriever(value : dict) -> str:
            return value["input"]
            
        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"] 
            new_value["history"] = value["input"]["history"]
            return new_value


        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(     #增强的对话链，通过新的链调用invoke可以得到历史记忆增强功能
            chain,
            get_history,
            input_messages_key="input",  #用户输入，注入的变量
            history_messages_key="history"  #历史消息的占位
        )
        return conversation_chain
    
if __name__ == '__main__':
    #session_id 配置
    session_config = {
        "configurable":{
            "session_id":"user_001",
        }
    }
    res = RagService().chain.invoke({"input":"春天穿什么颜色的衣服"},session_config)
    print(res)

