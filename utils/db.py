"""
utils/db.py
MongoDB integration for persistent chat sessions.
"""
from pymongo import MongoClient
from datetime import datetime
from config import Config
import uuid

# Connect to MongoDB
MONGO_URI = Config.MONGO_URI
client = MongoClient(MONGO_URI)
db = client.shop_agent
sessions_col = db.sessions

def get_or_create_session_id(session_id: str = None) -> str:
    """Generate a new UUID if none is provided."""
    return session_id if session_id else str(uuid.uuid4())

def save_session(session_id: str, messages: list, input_tokens: int = 0, output_tokens: int = 0) -> str:
    """
    将对话数据更新插入 MongoDB。
    动态保存当前状态（每次生成后调用）。
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # 提取对话标题
    title = "新的对话"
    for msg in messages:
        if msg.get("role") == "user":
            title = msg.get("content", "")[:20]
            if len(msg.get("content", "")) > 20:
                title += "..."
            break

    now = datetime.now()
    
    # 更新插入文档
    sessions_col.update_one(
        {"session_id": session_id},
        {"$set": {
            "title": title,
            "messages": messages,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "updated_at": now
        }},
        upsert=True
    )
    
    # 仅在插入时设置 created_at
    sessions_col.update_one(
        {"session_id": session_id},
        {"$setOnInsert": {"created_at": now}},
        upsert=True
    )
    
    return session_id

def load_session(session_id: str) -> dict:
    """
    根据 ID 从 MongoDB 加载会话。
    返回一个包含 'messages', 'input_tokens', 'output_tokens' 的字典，否则返回空默认值。
    """
    doc = sessions_col.find_one({"session_id": session_id})
    if doc:
        return {
            "messages": doc.get("messages", []),
            "input_tokens": doc.get("input_tokens", 0),
            "output_tokens": doc.get("output_tokens", 0)
        }
    return {"messages": [], "input_tokens": 0, "output_tokens": 0}

def get_all_sessions() -> list:
    """
    获取所有会话的轻量级信息，用于在历史记录中显示。
    按 updated_at 降序排列。
    """
    cursor = sessions_col.find(
        {}, 
        {"session_id": 1, "title": 1, "updated_at": 1, "created_at": 1}
    ).sort("updated_at", -1)
    
    return list(cursor)

def delete_session(session_id: str) -> bool:
    """
    根据 ID 删除 MongoDB 中的特定会话。
    """
    result = sessions_col.delete_one({"session_id": session_id})
    return result.deleted_count > 0
