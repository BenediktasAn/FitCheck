from fastapi import FastAPI

app = FastAPI(title="FitCheck ML Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ml-service"}
