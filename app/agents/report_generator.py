from pathlib import Path
from app.schemas.transaction import TransactionPayload, FinalDecision
from app.core.logger import logger

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def generate_audit_report(transaction: TransactionPayload, decision: FinalDecision) -> Path:
    """Gera um relatório de auditoria formal em formato Markdown para conformidade bancária."""
    logger.info(f"Generating audit report for TX: {decision.transaction_id}")
    
    file_path = REPORTS_DIR / f"audit_{decision.transaction_id}.md"
    
    report_content = f"""# 🛡️ RELATÓRIO DE AUDITORIA E COMPLIANCE - FINGUARD

**ID da Transação:** `{decision.transaction_id}`  
**Data/Hora UTC:** `{decision.timestamp}`  
**Status do Pipeline:** `CONCLUÍDO`

---

## 1. Dados da Transação
- **Conta de Origem:** `{transaction.account_id}`
- **Valor Solicitado:** `${transaction.amount:,.2f}`
- **Localização da Operação:** `{transaction.location}`

## 2. Perfil de Comportamento do Cliente
- **Média Mensal do Cliente:** `${transaction.customer_profile.avg_monthly_transfer:,.2f}`
- **Localização Habitual:** `{transaction.customer_profile.usual_location}`

---

## 3. Avaliação de Risco (Agente LLM - Qwen 2.5)
- **Nível de Risco Identificado:** **{decision.risk_level}**
- **Parecer Técnico da IA:**  
  > "{decision.llm_explanation}"

---

## 4. Ação Recomendada de Compliance
- **Decisão Final:** `{decision.action}`

---
*Relatório gerado automaticamente pelo motor de IA FinGuard Engine.*
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    logger.info(f"Audit report successfully saved to: {file_path}")
    return file_path