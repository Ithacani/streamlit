from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from calculator import calculate

class User_Input(BaseModel):
    operation: str
    x : float
    y : float

app = FastAPI()

@app.post("/calculate")
def operate(input:User_Input):
    result = calculate(input.operation, input.x, input.y)
    return result


if __name__ == '__main__':
    uvicorn.run("fast_api:app", reload=True)


