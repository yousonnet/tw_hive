import uvicorn
from dotenv import load_dotenv
import os

port = os.getenv('host_port')

if __name__ == "__main__":
    uvicorn.run("a_hive_router:app", host="0.0.0.0", port=int(port), reload=False)