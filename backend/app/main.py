from fastapi import FastAPI

app=FastAPI(
        title="TripMind AI",
        version="1.0.0"

)

@app.get("/")
def root():
    return{"message":"Welcome to TripMind AI"}

@app.get("/health")
def health():
    return{"status":"ok"}

