'''配置文件'''

#文本转32位十六进制字符串
md5_path = "./md5.text"


#Chroma存储，存入向量数据库
collection_name = "rag"
persist_directory = "./chroma_db"


#spliter 文本分割，以下定义格式
chunk_size  = 1000
chunk_overlap = 100
separators = ["\n\n" , "\n" , "." , "!" , "?" , "。" , "，" , "！" , "？" , " " , ""]
max_split_char_number = 1000  #文本分割阈值，超过这个阈值才进行分割


#相似度检索
similarity_threshold = 1  #检索返回匹配文档的数量


#嵌入模型的名称
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"



#用户id LHL
session_config = {
        "configurable":{
            "session_id":"user_001",
        }
    }