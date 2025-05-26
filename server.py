# server.py

from dotenv import load_dotenv
import os
import uvicorn


def run_server():
    load_dotenv()

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

    print(f"🚀 Starting FastAPI server on http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    run_server()
