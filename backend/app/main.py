from fastapi import FastAPI
app=FastAPI(title="AI Support agent")

@app.get('/')
def root():
    return{"message":"AI support agent is running"}