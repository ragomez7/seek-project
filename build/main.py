# main.py
from mangum import Mangum
from fastapi import FastAPI
from dotenv import load_dotenv
from tasks.router.task_routes import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware
from auth.router.auth_routes import router as auth_router

# Load local overrides first, then defaults (override ensures .env.local > existing env)
load_dotenv(dotenv_path=".env.local", override=True)
load_dotenv(override=True)

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations with tasks — create, update, delete, and fetch."
    }
]

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with support for status updates, soft deletes, and more.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <- You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# register_routes()
app.include_router(tasks_router)

app.include_router(auth_router)

# AWS Lambda handler
handler = Mangum(app)
