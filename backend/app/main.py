from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.agents.agent import agent


app = FastAPI(title="AI Support Agent")
conversations = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatResponse(BaseModel):
    question: str
    answer: str

class ChatRequest(BaseModel):
    question: str
    conversation_id: str



@app.get("/")
def root():
    return {"message": "AI support agent is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        messages = conversations.setdefault(
            request.conversation_id,
            []
        )

        messages.append({
            "role": "user",
            "content": request.question
        })

        result = agent.invoke({
            "messages": messages
        })

        messages = result["messages"]

        conversations[request.conversation_id] = messages

        answer = messages[-1].content

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )