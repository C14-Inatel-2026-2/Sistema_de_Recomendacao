import uvicorn

from recsys.api.app import criar_app

app = criar_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
