import os
import uvicorn
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
PORT = int(os.environ.get("PORT"))
if __name__ == "__main__":
    uvicorn.run(
        reload=True,
        app="app:app",
        port=PORT
    )
