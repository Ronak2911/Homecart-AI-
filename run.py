from dotenv import load_dotenv
import os

# Load backend/.env explicitly (local only)
ENV_PATH = os.path.join(os.path.dirname(__file__), "backend", ".env")
load_dotenv(ENV_PATH)

print("RUN ENV TEST:", os.getenv("MONGO_URI"))

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
