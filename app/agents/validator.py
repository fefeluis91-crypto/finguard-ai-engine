from app.schemas.transaction import TransactionPayload
from app.core.logger import logger
from pydantic import ValidationError

def agent_validator(raw_payload: dict) -> TransactionPayload:
    logger.info("Validating transaction payload schema with Pydantic...")
    try:
        validated_transaction = TransactionPayload(**raw_payload)
        logger.info(f"Payload successfully validated for Transaction ID: {validated_transaction.transaction_id}")
        return validated_transaction
    except ValidationError as e:
        logger.error(f"Schema validation failed: {e}")
        raise ValueError(f"Invalid transaction payload: {e}")