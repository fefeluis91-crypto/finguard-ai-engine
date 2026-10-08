from pydantic import BaseModel, Field
from typing import Literal

# --- Payload de Entrada ---
class CustomerProfile(BaseModel):
    avg_monthly_transfer: float = Field(..., description="Customer average monthly transfer amount")
    usual_location: str = Field(..., description="Customer primary location")

class TransactionPayload(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    account_id: str = Field(..., description="Account identification number")
    amount: float = Field(..., gt=0, description="Transaction amount in USD/BRL")
    location: str = Field(..., description="City and state of transaction origin")
    customer_profile: CustomerProfile


# --- Saída Estruturada do LLM (Olama/Risk Analyst) ---
class RiskAnalysisOutput(BaseModel):
    risk_level: Literal["HIGH", "LOW"] = Field(
        ..., 
        description="HIGH if the transaction is suspicious based on amount or location; otherwise LOW."
    )
    explanation: str = Field(
        ..., 
        description="One clear, concise sentence justifying the assigned risk level."
    )


# --- Decisão Final da FinGuard ---
class FinalDecision(BaseModel):
    transaction_id: str
    action: Literal["APPROVED", "FLAGGED_FOR_HUMAN_REVIEW"]
    risk_level: str
    llm_explanation: str
    timestamp: str