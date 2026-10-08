import json
from app.agents.validator import agent_validator
from app.agents.risk_analyst import agent_risk_analyst
from app.agents.decision_maker import agent_decision_maker
from app.core.logger import logger

def run_pipeline(raw_payload: dict):
    logger.info("=== FINGUARD PIPELINE STARTED ===")
    
    try:
        transaction = agent_validator(raw_payload)
        risk_analysis = agent_risk_analyst(transaction)
        final_decision = agent_decision_maker(transaction, risk_analysis)
        
        logger.info("=== PIPELINE COMPLETED SUCCESSFULLY ===")
        print("\n" + json.dumps(final_decision.model_dump(), indent=2, ensure_ascii=False) + "\n")
        
    except Exception as e:
        logger.critical(f"Pipeline crashed during execution: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        with open("data/payload.json", "r", encoding="utf-8") as f:
            payload = json.load(f)
        run_pipeline(payload)
    except Exception as e:
        logger.error(f"Failed to load payload file: {e}")