from fastapi import FastAPI

app = FastAPI(title="Sql Test")

@app.get('/')
async def root():
    return "SWL"