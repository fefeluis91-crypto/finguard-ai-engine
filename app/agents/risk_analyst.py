from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.transaction import TransactionPayload, RiskAnalysisOutput
from app.core.logger import logger

base_llm = ChatOllama(model="qwen2.5:1.5b", temperature=0.0)
structured_llm = base_llm.with_structured_output(RiskAnalysisOutput)

def agent_risk_analyst(transaction: TransactionPayload) -> RiskAnalysisOutput:
    logger.info(f"Dispatching risk evaluation query to local LLM for TX: {transaction.transaction_id}")

    system_message = SystemMessage(content="""
    You are a Senior Financial Fraud Detection Agent at FinGuard.
    Analyze the transaction by comparing it against the customer profile.
    
    CRITERIA:
    - Set risk_level to 'HIGH' if amount is significantly higher than avg_monthly_transfer, or if location differs suspiciously.
    - Set risk_level to 'LOW' if amount and location match normal customer behavior.
    - Provide a concise 1-sentence explanation.
    """)

    human_message = HumanMessage(content=f"""
    Analyze Transaction:
    - ID: {transaction.transaction_id}
    - Amount: ${transaction.amount}
    - Location: {transaction.location}
    - Customer Usual Avg: ${transaction.customer_profile.avg_monthly_transfer}
    - Customer Usual Location: {transaction.customer_profile.usual_location}
    """)

    analysis_result: RiskAnalysisOutput = structured_llm.invoke([system_message, human_message])
    
    logger.info(f"LLM evaluation completed. Risk Level: {analysis_result.risk_level}")
    logger.debug(f"LLM Explanation: {analysis_result.explanation}")
    
    return analysis_result