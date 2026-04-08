from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.community.router import router as community_router
from app.comments.router import router as comments_router
from app.config import FRONTEND_URL

app = FastAPI(title="Dive-In API")

allow_origins = [origin.strip() for origin in FRONTEND_URL.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(community_router, prefix="/community", tags=["community"])
app.include_router(comments_router, prefix="/community", tags=["comments"])


@app.get("/")
def root():
    return {"message": "Dive-In API"}
