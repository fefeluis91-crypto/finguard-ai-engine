from datetime import datetime, timezone
from app.schemas.transaction import TransactionPayload, RiskAnalysisOutput, FinalDecision
from app.core.logger import logger

def agent_decision_maker(transaction: TransactionPayload, analysis: RiskAnalysisOutput) -> FinalDecision:
    logger.info("Finalizing compliance decision based on risk assessment...")
    
    action = "FLAGGED_FOR_HUMAN_REVIEW" if analysis.risk_level == "HIGH" else "APPROVED"

    decision = FinalDecision(
        transaction_id=transaction.transaction_id,
        action=action,
        risk_level=analysis.risk_level,
        llm_explanation=analysis.explanation,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    logger.warning(f"ACTION TAKEN: [{decision.action}] for TX: {decision.transaction_id}") if action == "FLAGGED_FOR_HUMAN_REVIEW" else logger.info(f"ACTION TAKEN: [{decision.action}] for TX: {decision.transaction_id}")
    
    return decision