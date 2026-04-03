================================================================
              RAG 智能客服系统 - 项目说明
================================================================

【项目简介】
基于 LangChain + ChromaDB + 阿里云通义千问 构建的本地 RAG（检索增强生成）
智能客服系统，支持自定义知识库上传，并通过向量检索实现精准问答。
#LHL
----------------------------------------------------------------
【项目结构】
----------------------------------------------------------------

RAG_prompt/
├── config_data.py          # 全局配置（模型名、分割参数、路径等）
├── knowledge_base.py       # 知识库管理（文本向量化入库，MD5去重）
├── vector_stores.py        # 向量数据库封装（ChromaDB 检索器）
├── file_history_store.py   # 对话历史持久化（按 session_id 存为 JSON 文件）
├── rag.py                  # RAG 核心链（向量检索 + 对话历史 + 模型生成）
├── app_qa.py               # Streamlit 前端：智能客服问答页面
├── app_file_uploader.py    # Streamlit 前端：知识库文件上传页面
├── data/                   # 原始知识文档（TXT 格式）
│   ├── 颜色选择.txt
│   ├── 洗涤养护.txt
│   └── 尺码推荐.txt
├── chroma_db/              # ChromaDB 向量数据库持久化文件（自动生成）
├── chat_history/           # 对话历史记录文件（自动生成）
├── md5.text                # 已入库文件的 MD5 记录，用于去重（自动生成）
├── requirements.txt        # 项目依赖库
└── README.txt              # 项目说明文件

----------------------------------------------------------------
【各模块职责】
----------------------------------------------------------------

config_data.py
  - 统一管理所有配置参数，避免硬编码
  - 包含：模型名称、ChromaDB路径、文本分割参数、会话配置等

knowledge_base.py
  - 接收文本内容 → MD5去重检查 → 文本分割 → 向量化 → 存入 ChromaDB
  - MD5去重：防止相同文档被重复入库，节省空间

vector_stores.py
  - 封装 ChromaDB 向量数据库
  - 提供 get_retriever() 方法，返回可插入 LangChain 链的检索器

file_history_store.py
  - 将对话历史以 JSON 格式持久化到本地文件
  - 支持多用户多 session，每个 session_id 对应一个历史文件

rag.py
  - 构建完整 RAG 链：
      用户输入 → 向量检索相关文档 → 注入对话历史 → 组装 Prompt → 模型生成
  - 使用 RunnableWithMessageHistory 实现多轮对话记忆

app_file_uploader.py
  - Streamlit 页面，上传 TXT 文件并写入知识库
  - 显示文件名、格式、大小，并提示入库结果

app_qa.py
  - Streamlit 页面，用户聊天问答界面
  - 支持流式输出（逐字显示），保存完整对话历史

----------------------------------------------------------------
【数据流说明】
----------------------------------------------------------------

  [知识库录入]
  用户上传 TXT → app_file_uploader → KnowledgeBaseService
              → 文本分割 → DashScope 向量化 → 存入 ChromaDB

  [用户问答]
  用户提问 → app_qa → RagService.chain
                    ├── 从 ChromaDB 检索相关文档片段
                    ├── 从 file_history_store 读取历史对话
                    ├── 组装 Prompt → ChatTongyi (qwen3-max)
                    └── 流式返回回答，保存到历史记录

----------------------------------------------------------------
【使用的关键技术】
----------------------------------------------------------------

  - LangChain       链式调用、Prompt 模板、历史记忆管理
  - ChromaDB        本地向量数据库，持久化存储向量数据
  - DashScope       阿里云嵌入模型 text-embedding-v4
  - ChatTongyi      阿里云对话模型 qwen3-max
  - Streamlit       快速构建 Web 交互界面
  - MD5 去重        防止相同文档重复入库

----------------------------------------------------------------
【运行方式】
----------------------------------------------------------------

1. 安装依赖：
   pip install -r requirements.txt

2. 配置阿里云 API Key（环境变量）：
   Windows:  set DASHSCOPE_API_KEY=你的APIKey

3. 启动知识库上传页面：
   cd C:\Users\LHL\Desktop\RAG_prompt
   streamlit run app_file_uploader.py

4. 启动智能客服问答页面：
   cd C:\Users\LHL\Desktop\RAG_prompt
   streamlit run app_qa.py


#LHL
================================================================
