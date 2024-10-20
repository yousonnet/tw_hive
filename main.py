import uvicorn

if __name__ == "__main__":
    uvicorn.run("a_hive_router:app", host="0.0.0.0", port=7666, reload=False)