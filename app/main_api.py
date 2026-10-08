from fastapi import FastAPI, HTTPException, status
from app.schemas.transaction import TransactionPayload, FinalDecision
from app.agents.validator import agent_validator
from app.agents.risk_analyst import agent_risk_analyst
from app.agents.decision_maker import agent_decision_maker
from app.core.logger import logger

app = FastAPI(
    title="FinGuard Agentic API",
    description="Enterprise Anti-Fraud Pipeline powered by Local LLM Agents",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Endpoint de verificação de saúde da API (Health Check)"""
    return {"status": "healthy", "service": "FinGuard Engine"}

@app.post(
    "/api/v1/analyze", 
    response_model=FinalDecision, 
    status_code=status.HTTP_200_OK,
    summary="Analisa risco de fraude em transação financeira"
)
async def analyze_transaction(payload: TransactionPayload):
    """
    Recebe um payload validado via Pydantic, executa a análise de risco 
    com o LLM local (Ollama) e retorna a ação de compliance final.
    """
    logger.info(f"API Request Received for TX: {payload.transaction_id}")
    
    try:
        # Step 1: Validação de Schema (Já realizada automaticamente pelo FastAPI via Pydantic)
        # Step 2: Análise pelo Agente LLM
        risk_analysis = agent_risk_analyst(payload)
        
        # Step 3: Decisão do Agente Compliance
        final_decision = agent_decision_maker(payload, risk_analysis)
        
        return final_decision

    except Exception as e:
        logger.error(f"Error processing transaction {payload.transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal fraud engine error: {str(e)}"
        )