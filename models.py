import code
from pydantic import BaseModel
from typing import List,Optional


class Transaction(BaseModel):
    id: str
    amount: float
    description: Optional[str] = ""

class TransactionPayload(BaseModel):
    transactions: List[Transaction]

class RiskFlag(BaseModel):
    code: str
    message: str

class FinancialSummary(BaseModel):
    total_inflow: float
    total_outflow: float
    net_cash_flow: float
    inflow_count: int
    outflow_count: int
    largest_inflow: float
    largest_outflow: float
    average_transaction_value: float
    risk_flags: List[RiskFlag]
    readiness: str