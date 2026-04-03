'''
知识库
对于md5来说，不管多大的东西都能得到固定的32位的十六进制字符串，节省空间效率高
'''
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime



'''检查传入的md5字符串是否已经被处理过了'''
def cheke_md5(md5_str:str):
    '''检查传入的md5字符串是否已经被处理过
       return False(md5)未处理过, True(已经处理过,有记录)
    '''
    if not os.path.exists(config.md5_path):
        #if进入表示文件不存在，就是没处理过这个md5
        open(config.md5_path,'w',encoding='utf-8').close()  #open函数，用‘w’模式打开，如果文件不存在会自动创建，创建后clsoe
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()   #处理字符串前后的空格和回车
            if line == md5_str:
                return True      #已处理过
            
        return False



'''将传入的md5字符串，记录到文件内保存'''
def save_md5(md5_str : str):
    with open(config.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_str + '\n')



'''将传入的字符串转化为md5字符串'''
def get_string_md5(input_str : str,enconding="utf-8"):

    #将字符串转换为bytes字节数据（还原二进制）
    str_bytes = input_str.encode(encoding=enconding)

    #创建md5对象
    md5_obj = hashlib.md5()   #得到md5对象
    md5_obj.update(str_bytes)  #更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()  #得到md5的十六进制字符串

    return md5_hex



class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory,exist_ok=True)

        self.chroma = Chroma(
            collection_name = config.collection_name,     #数据库的表名
            embedding_function = DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory,   #数据库本地存储文件夹
        )   #向量存储的实例Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,    #分割后的文本段最大长度
            chunk_overlap = config.chunk_overlap,  #连续文本段之间的字符重叠数量
            separators=config.separators,      #自然段落划分的符号
            length_function = len,              #使用ppython自带len函数做长度统计的依据
        )   #文本分割器的对象



    def upload_by_str(self,data: str ,filename):
        '''将传入的字符串，进行向量化，存入向量数据库中'''
        #先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if cheke_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        
        if len(data) > config.max_split_char_number:    #超过阈值才做分割max_split_char_number 
            Knowledge_chunks : list[str] = self.spliter.split_text(data)
        else:
            Knowledge_chunks = [data]

        metadata = {
            "soure":filename,
            "create_time":datetime.now().strftime("%Y - %m - %d %H:%M:%S"),  #将时间转为日常格式 20xx-xx-xx  17:51:00
            "operator":"浩蓝",
        }

        self.chroma.add_texts(   #内容加载到向量库中
            #iterable -> list \ tuple
            Knowledge_chunks,
            metadatas=[metadata for _ in Knowledge_chunks]
        )

        
        save_md5(md5_hex)   #表明数据已处理
        return "[成功]内容已经成功载入向量库"



if __name__ == '__main__':

    service = KnowledgeBaseService()
    r = service.upload_by_str("梁浩蓝111","testfile")
    print(r)

#2.测试md5转换后是否存入text中
#    save_md5("ceb05b2c53c354b80e5c95a08ad36413")
#    print(cheke_md5("d98a24ae77af82819b4671c03d7ba769"))
#1/以下代码利用md5函数，将字符串转为32为十六进制字符串
#    r1 = get_string_md5("梁浩蓝")
#    r2 = get_string_md5("梁浩蓝")
#    r3 = get_string_md5("梁浩蓝111")
#
#    print(r1)
#    print(r2)
#    print(r3)
