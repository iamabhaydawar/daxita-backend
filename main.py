from fastapi import FastAPI
from models import TransactionPayload,FinancialSummary
from analyzer import analyze_transactions

app = FastAPI(title="Daxita Financial Transaction Analyzer")

@app.post("/analyse-file",response_model=FinancialSummary)

def analyse_file(payload:TransactionPayload):
    return analyze_transactions(payload.transactions)

@app.get("/")
def root():
    return {"status":"ok", "service":"Daxita Financial Transaction Analyzer"}