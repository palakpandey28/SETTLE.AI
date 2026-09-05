import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agent import run_agent
from transaction_parser import extract_transaction_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuestion(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

@app.get("/")
def home():
    return {
        "message": "Payment Settlement AI Agent is running!"
    }

@app.post("/ask")
def ask_agent(request: UserQuestion):
    transaction_id = extract_transaction_id(
        request.question
    )
    if transaction_id is None:
        logger.info("No transaction ID found in question.")
        return {
            "status": "MISSING_TRANSACTION_ID",
            "message": (
                "Please provide a transaction ID, "
                "for example TX0096."
            )
        }
    try:
        result = run_agent(
            request.question,
            transaction_id
        )
        logger.info(f"Successfully analyzed transaction {transaction_id}.")
        return result
    except Exception as e:
        logger.error(f"Agent failed for transaction {transaction_id}: {e}")
        return {
            "status": "ERROR",
            "message": "Something went wrong while analyzing this transaction. Please try again."
        }