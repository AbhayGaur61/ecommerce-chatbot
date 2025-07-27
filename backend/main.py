import os
import uuid
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text, DateTime, text, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from urllib.parse import quote_plus
from groq import Groq
from sqlalchemy import desc
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# --- Configuration and Setup ---
load_dotenv()
# IMPORTANT: Add your credentials here
DB_USER = 'postgres'
DB_PASSWORD = os.getenv('DB_PASSWORD') 
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'chatbot_db'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# --- Initialize Clients ---

# Database Connection
encoded_password = quote_plus(DB_PASSWORD)
DATABASE_URI = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Groq LLM Client
groq_client = Groq(api_key=GROQ_API_KEY)

# --- Database Schemas ---

class ConversationHistory(Base):
    __tablename__ = 'conversation_history'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False)
    user_id = Column(String, nullable=True) # <-- THIS LINE WAS LIKELY MISSING
    message_text = Column(Text, nullable=False)
    message_source = Column(String, nullable=False) # 'user' or 'bot'
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Database Query Functions (Business Logic) ---

def db_get_top_products(db):
    query = text("SELECT name, COUNT(oi.product_id) as sales_count FROM order_items oi JOIN products p ON oi.product_id = p.id GROUP BY name ORDER BY sales_count DESC LIMIT 5;")
    result = db.execute(query)
    return [dict(row) for row in result.mappings()]

def db_get_order_status(db, order_id: int):
    query = text("SELECT status FROM orders WHERE order_id = :order_id")
    result = db.execute(query, {'order_id': order_id}).fetchone()
    return result[0] if result else None

def db_get_stock_level(db, product_name: str):
    query = text("SELECT COUNT(*) FROM inventory_items WHERE product_name ILIKE :product_name AND sold_at IS NULL")
    result = db.execute(query, {'product_name': f'%{product_name}%'}).scalar()
    return result

# --- FastAPI Application ---

app = FastAPI(title="E-Commerce Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # The origin of your React app
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

class ChatRequest(BaseModel):
    user_message: str
    session_id: str | None = None

@app.post("/api/chat")
def chat(request: ChatRequest):
    db = SessionLocal()
    session_id = request.session_id or str(uuid.uuid4())

    try:
        # 1. Persist user message
        db.add(ConversationHistory(session_id=session_id, message_text=request.user_message, message_source='user'))
        db.commit()
        
        # 2. First LLM Call: Intent Recognition
        intent_response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a function calling API. Based on the user query, determine which function to call: get_top_products, get_order_status(order_id), get_stock_level(product_name). Respond with ONLY JSON like {\"function\": \"function_name\", \"parameters\": {\"param_name\": \"value\"}}. If information is missing, use {\"function\": \"clarify\"}."},
                {"role": "user", "content": request.user_message}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        intent_data = json.loads(intent_response.choices[0].message.content)
        
        # 3. Execute Business Logic based on intent
        business_data = None
        if intent_data.get("function") == "get_top_products":
            business_data = db_get_top_products(db)
        elif intent_data.get("function") == "get_order_status" and intent_data.get("parameters", {}).get("order_id"):
            business_data = db_get_order_status(db, intent_data["parameters"]["order_id"])
        elif intent_data.get("function") == "get_stock_level" and intent_data.get("parameters", {}).get("product_name"):
            business_data = db_get_stock_level(db, intent_data["parameters"]["product_name"])
        
        # 4. Second LLM Call: Formulate Natural Response
        prompt_for_formulation = f"User query: '{request.user_message}'. Data: '{business_data}'. Formulate a friendly, natural language response."
        if business_data is None:
            prompt_for_formulation = f"User query: '{request.user_message}'. I could not find the information or need more details. Ask a clarifying question."

        final_response_completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly e-commerce customer support assistant."},
                {"role": "user", "content": prompt_for_formulation}
            ],
            temperature=0.7
        )
        final_bot_response = final_response_completion.choices[0].message.content

        # 5. Persist bot response
        db.add(ConversationHistory(session_id=session_id, message_text=final_bot_response, message_source='bot'))
        db.commit()

        return {"bot_response": final_bot_response, "session_id": session_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/sessions/{user_id}")
def get_user_sessions(user_id: str):
    """
    Retrieves a list of unique session IDs for a given user.
    """
    db = SessionLocal()
    try:
        # Query for distinct session IDs, ordered by the most recent first
        sessions = db.query(ConversationHistory.session_id)\
            .filter(ConversationHistory.user_id == user_id)\
            .distinct()\
            .order_by(desc(ConversationHistory.created_at))\
            .all()

        # The result is a list of tuples, so we extract the first element of each
        session_ids = [session[0] for session in sessions]
        return {"session_ids": session_ids}
    finally:
        db.close()

@app.get("/api/history/{session_id}")
def get_session_history(session_id: str):
    """
    Retrieves all messages for a specific session ID.
    """
    db = SessionLocal()
    try:
        history = db.query(ConversationHistory)\
            .filter(ConversationHistory.session_id == session_id)\
            .order_by(ConversationHistory.created_at)\
            .all()
        return history
    finally:
        db.close()


if __name__ == '__main__':
    print("To run this app, use the command: uvicorn main:app --reload")