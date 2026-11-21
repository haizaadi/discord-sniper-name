from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="NAME LAB API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["GET", "POST"], allow_headers=["*"],
)

class CheckRequest(BaseModel):
    platform: str
    usernames: list[str]

@app.get("/")
def root():
    return {"app": "NAME LAB", "status": "ok", "note": "Availability is not queried."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate")
def validate(payload: CheckRequest):
    platform = payload.platform.lower()
    patterns = {
        "discord": re.compile(r"^[a-z0-9._]{2,32}$"),
        "tiktok": re.compile(r"^[A-Za-z0-9._]{2,24}$"),
        "generic": re.compile(r"^[A-Za-z0-9._-]{2,32}$"),
    }
    pattern = patterns.get(platform, patterns["generic"])
    return {
        "results": [
            {"username": name, "format": "VALID" if pattern.fullmatch(name) else "INVALID",
             "availability": "UNKNOWN"}
            for name in payload.usernames
        ]
    }
