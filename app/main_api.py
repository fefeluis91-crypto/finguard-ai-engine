from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from app.schemas.transaction import TransactionPayload, FinalDecision
from app.agents.validator import agent_validator
from app.agents.risk_analyst import agent_risk_analyst
from app.agents.decision_maker import agent_decision_maker
from app.agents.report_generator import generate_audit_report
from app.core.logger import logger

app = FastAPI(
    title="FinGuard Agentic API",
    description="Enterprise Anti-Fraud Pipeline powered by Local LLM Agents",
    version="1.1.0"
)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Endpoint de verificação de saúde da API (Health Check)"""
    return {"status": "healthy", "service": "FinGuard Engine"}

@app.post(
    "/api/v1/analyze", 
    response_model=FinalDecision, 
    status_code=status.HTTP_200_OK,
    summary="Analisa risco de fraude e gera relatório de auditoria"
)
async def analyze_transaction(payload: TransactionPayload):
    """
    Recebe o payload da transação, executa a análise via LLM local (Ollama),
    gera o relatório de auditoria em disco e retorna a decisão final.
    """
    logger.info(f"API Request Received for TX: {payload.transaction_id}")
    try:
        risk_analysis = agent_risk_analyst(payload)
        final_decision = agent_decision_maker(payload, risk_analysis)
        
        # Gera automaticamente o relatório .md na pasta /reports
        generate_audit_report(payload, final_decision)
        
        return final_decision

    except Exception as e:
        logger.error(f"Error processing transaction {payload.transaction_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal fraud engine error: {str(e)}"
        )

@app.get("/api/v1/reports/{transaction_id}", summary="Baixa o relatório de auditoria em Markdown")
async def get_report(transaction_id: str):
    """Endpoint para baixar o relatório de auditoria gerado para uma transação específica."""
    file_path = Path(f"reports/audit_{transaction_id}.md")
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Relatório não encontrado para esta transação."
        )
    return FileResponse(path=file_path, filename=file_path.name, media_type="text/markdown")