from fastapi import FastAPI
import uvicorn
from routers.portfolio import router as portfolio_router
from routers.delete import router as delete_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(portfolio_router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(delete_router, prefix="/portfolio/delete", tags=["Delete"])

@app.get("/",tags=['Welcome'])
def read_root():
    return {"message": "Welcome to my portfolio backend!"}


