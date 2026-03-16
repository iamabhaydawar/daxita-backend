from models import Transaction, FinancialSummary, RiskFlag
from typing import List

def analyze_transactions(transactions: List[Transaction]) -> FinancialSummary:
    inflows = [t.amount for t in transactions if t.amount > 0]
    outflows = [t.amount for t in transactions if t.amount < 0]

    total_inflow = sum(inflows)
    total_outflow = sum(outflows)
    net_cash_flow = total_inflow + total_outflow

    largest_inflow = max(inflows, default=0.0)
    largest_outflow = min(outflows, default=0.0)

    avg_value=(
        sum(abs(t.amount) for t in transactions) / len(transactions)
        if transactions else 0.0
    )

    #-- Risk Flags --#
    flags:List[RiskFlag] = []

    #Rule1: Negative net cash flow
    if net_cash_flow < 0:
        flags.append(RiskFlag(
            code="NEGATIVE_NET_CASH_FLOW",
            message="Outflows exceed inflows -- Net cash flow is negative"
        ))

    #Rule2: Large single outflow(>50% of total inflow)
    if total_inflow > 0 and abs(largest_outflow) > total_inflow * 0.5:
        flags.append(RiskFlag(
            code="LARGE_SINGLE_OUTFLOW",
            message="A single outflow exceeds 50% of total inflow"
        ))


    #Rule3: NSF risk - any outflow that exceeds running balance
    balance = 0.0
    for t in transactions:
        balance += t.amount
        if balance <0:
            flags.append(RiskFlag(
                code="NSF_RISK",
                message="Potential insufficent detected based on funds available - Outflow exceeds running balance"
            ))
            break
    
    #Rule4: Low inflow frequency - (<20% of transactions are inflows)
    if len(transactions) > 0 and len(inflows) / len(transactions) < 0.2:
        flags.append(RiskFlag(
            code="LOW_INFLOW_FREQUENCY",
            message="Less than 20% of transactions are inflows -- Potential liquidity risk"
        ))
    
    #Readiness Classification--
    if len(flags) == 0 and net_cash_flow > 0:
        readiness = "strong"
    elif len(flags) <= 1:
        readiness = "structured"
    else:
        readiness = "requires_clarification"
    return FinancialSummary(
        total_inflow=round(total_inflow, 2),
        total_outflow=round(total_outflow, 2),
        net_cash_flow=round(net_cash_flow, 2),
        inflow_count=len(inflows),
        outflow_count=len(outflows),
        largest_inflow=round(largest_inflow, 2),
        largest_outflow=round(largest_outflow, 2),
        average_transaction_value=round(avg_value, 2),
        risk_flags=flags,
        readiness=readiness
    )