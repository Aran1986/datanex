# Location: datanex/api/routes/blockchain.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from workers.tasks import analyze_blockchain_address_task
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/blockchain", tags=["blockchain"])

class AnalyzeAddressRequest(BaseModel):
    address: str

class AnalyzeBatchRequest(BaseModel):
    addresses: List[str]

class GetTransactionRequest(BaseModel):
    tx_hash: str

class GetBlockRequest(BaseModel):
    block_number: int

@router.post("/analyze-address")
async def analyze_address(
    request: AnalyzeAddressRequest,
    db: AsyncSession = Depends(get_db)
):
    """آنالیز یک آدرس blockchain"""
    try:
        task = analyze_blockchain_address_task.delay(request.address)
        
        return {
            "message": "Address analysis started",
            "address": request.address,
            "task_id": task.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-batch")
async def analyze_batch_addresses(
    request: AnalyzeBatchRequest,
    db: AsyncSession = Depends(get_db)
):
    """آنالیز دسته‌ای آدرس‌ها"""
    try:
        if len(request.addresses) > 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum 50 addresses allowed per request"
            )
        
        from core.blockchain_analyzer import blockchain_analyzer
        
        results = await blockchain_analyzer.batch_analyze_addresses(request.addresses)
        
        return {
            "message": "Batch analysis completed",
            "analyzed_count": len(results),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transaction")
async def get_transaction(
    request: GetTransactionRequest,
    db: AsyncSession = Depends(get_db)
):
    """دریافت اطلاعات تراکنش"""
    try:
        from core.blockchain_analyzer import blockchain_analyzer
        
        result = await blockchain_analyzer.get_transaction(request.tx_hash)
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return {
            "message": "Transaction retrieved",
            "transaction": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/block")
async def get_block(
    request: GetBlockRequest,
    db: AsyncSession = Depends(get_db)
):
    """دریافت اطلاعات بلاک"""
    try:
        from core.blockchain_analyzer import blockchain_analyzer
        
        result = await blockchain_analyzer.get_block(request.block_number)
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return {
            "message": "Block retrieved",
            "block": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gas-prices")
async def get_gas_prices(db: AsyncSession = Depends(get_db)):
    """دریافت قیمت‌های gas"""
    try:
        from core.blockchain_analyzer import blockchain_analyzer
        
        result = await blockchain_analyzer.get_gas_prices()
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return {
            "message": "Gas prices retrieved",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-contract")
async def analyze_contract(
    request: AnalyzeAddressRequest,
    db: AsyncSession = Depends(get_db)
):
    """آنالیز smart contract"""
    try:
        from core.blockchain_analyzer import blockchain_analyzer
        
        result = await blockchain_analyzer.analyze_contract(request.address)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return {
            "message": "Contract analyzed",
            "contract": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))