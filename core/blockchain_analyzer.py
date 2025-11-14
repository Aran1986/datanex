# Location: datanex/core/blockchain_analyzer.py

from typing import List, Dict, Any, Optional
from web3 import Web3
from web3.exceptions import Web3Exception
import pandas as pd
from utils.logger import log
from utils.config import get_settings
import asyncio
from datetime import datetime

settings = get_settings()

class BlockchainAnalyzer:
    """ماژول آنالیز داده‌های بلاکچین"""
    
    def __init__(self):
        self.w3: Optional[Web3] = None
        self._initialize_web3()
    
    def _initialize_web3(self):
        """اتصال به شبکه Ethereum"""
        try:
            if settings.INFURA_API_KEY:
                infura_url = f"{settings.ETHEREUM_RPC}{settings.INFURA_API_KEY}"
                self.w3 = Web3(Web3.HTTPProvider(infura_url))
                
                if self.w3.is_connected():
                    log.info("Connected to Ethereum network")
                else:
                    log.warning("Failed to connect to Ethereum network")
        except Exception as e:
            log.error(f"Error initializing Web3: {e}")
    
    async def analyze_address(self, address: str) -> Dict[str, Any]:
        """آنالیز یک آدرس"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            # Checksum address
            address = Web3.to_checksum_address(address)
            
            # دریافت balance
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            # دریافت transaction count
            tx_count = self.w3.eth.get_transaction_count(address)
            
            # بررسی آیا contract است
            code = self.w3.eth.get_code(address)
            is_contract = len(code) > 0
            
            result = {
                'address': address,
                'balance_eth': float(balance_eth),
                'balance_wei': int(balance_wei),
                'transaction_count': tx_count,
                'is_contract': is_contract,
                'type': 'contract' if is_contract else 'wallet'
            }
            
            log.info(f"Analyzed address {address}")
            return result
            
        except Exception as e:
            log.error(f"Error analyzing address {address}: {e}")
            return {'address': address, 'error': str(e)}
    
    async def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """دریافت اطلاعات یک تراکنش"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            result = {
                'hash': tx_hash,
                'from': tx['from'],
                'to': tx['to'],
                'value_eth': float(self.w3.from_wei(tx['value'], 'ether')),
                'gas': tx['gas'],
                'gas_price': tx['gasPrice'],
                'nonce': tx['nonce'],
                'block_number': tx['blockNumber'],
                'status': receipt['status'],
                'gas_used': receipt['gasUsed']
            }
            
            log.info(f"Retrieved transaction {tx_hash}")
            return result
            
        except Exception as e:
            log.error(f"Error getting transaction {tx_hash}: {e}")
            return {'hash': tx_hash, 'error': str(e)}
    
    async def get_block(self, block_number: int) -> Dict[str, Any]:
        """دریافت اطلاعات یک بلاک"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            
            result = {
                'number': block['number'],
                'hash': block['hash'].hex(),
                'parent_hash': block['parentHash'].hex(),
                'timestamp': block['timestamp'],
                'miner': block['miner'],
                'difficulty': block['difficulty'],
                'total_difficulty': block['totalDifficulty'],
                'size': block['size'],
                'gas_used': block['gasUsed'],
                'gas_limit': block['gasLimit'],
                'transaction_count': len(block['transactions'])
            }
            
            log.info(f"Retrieved block {block_number}")
            return result
            
        except Exception as e:
            log.error(f"Error getting block {block_number}: {e}")
            return {'block_number': block_number, 'error': str(e)}
    
    async def analyze_transactions(self, address: str, limit: int = 100) -> Dict[str, Any]:
        """آنالیز تراکنش‌های یک آدرس"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            address = Web3.to_checksum_address(address)
            
            # دریافت آخرین بلاک
            latest_block = self.w3.eth.block_number
            
            transactions = []
            incoming_value = 0
            outgoing_value = 0
            
            # اسکن بلاک‌های اخیر (محدود شده برای عملکرد)
            scan_range = min(limit, 1000)
            
            for block_num in range(latest_block, latest_block - scan_range, -1):
                try:
                    block = self.w3.eth.get_block(block_num, full_transactions=True)
                    
                    for tx in block['transactions']:
                        if tx['from'] == address or tx['to'] == address:
                            value_eth = float(self.w3.from_wei(tx['value'], 'ether'))
                            
                            tx_data = {
                                'hash': tx['hash'].hex(),
                                'from': tx['from'],
                                'to': tx['to'],
                                'value_eth': value_eth,
                                'block_number': block_num,
                                'timestamp': block['timestamp'],
                                'direction': 'outgoing' if tx['from'] == address else 'incoming'
                            }
                            
                            transactions.append(tx_data)
                            
                            if tx['from'] == address:
                                outgoing_value += value_eth
                            else:
                                incoming_value += value_eth
                            
                            if len(transactions) >= limit:
                                break
                    
                    if len(transactions) >= limit:
                        break
                
                except Exception as e:
                    log.debug(f"Error scanning block {block_num}: {e}")
                    continue
            
            result = {
                'address': address,
                'transaction_count': len(transactions),
                'incoming_total': incoming_value,
                'outgoing_total': outgoing_value,
                'net_flow': incoming_value - outgoing_value,
                'transactions': transactions
            }
            
            log.info(f"Analyzed {len(transactions)} transactions for {address}")
            return result
            
        except Exception as e:
            log.error(f"Error analyzing transactions for {address}: {e}")
            return {'address': address, 'error': str(e)}
    
    async def analyze_token_transfers(self, token_address: str, limit: int = 100) -> Dict[str, Any]:
        """آنالیز انتقال‌های یک توکن"""
        # برای آنالیز کامل توکن، نیاز به Contract ABI است
        # اینجا یک نسخه ساده ارائه می‌شود
        
        result = {
            'token_address': token_address,
            'note': 'Full token analysis requires Contract ABI',
            'recommendation': 'Use Etherscan API or The Graph for detailed token analytics'
        }
        
        return result
    
    async def get_gas_prices(self) -> Dict[str, Any]:
        """دریافت قیمت‌های gas فعلی"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            gas_price = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price, 'gwei')
            
            result = {
                'gas_price_wei': int(gas_price),
                'gas_price_gwei': float(gas_price_gwei),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            log.error(f"Error getting gas prices: {e}")
            return {'error': str(e)}
    
    async def analyze_contract(self, contract_address: str) -> Dict[str, Any]:
        """آنالیز اولیه یک smart contract"""
        if not self.w3 or not self.w3.is_connected():
            return {'error': 'Not connected to blockchain'}
        
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            
            # دریافت bytecode
            code = self.w3.eth.get_code(contract_address)
            
            if len(code) == 0:
                return {'error': 'Not a contract address'}
            
            # آنالیز اولیه
            result = {
                'address': contract_address,
                'bytecode_size': len(code),
                'is_contract': True,
                'balance_eth': float(self.w3.from_wei(
                    self.w3.eth.get_balance(contract_address), 'ether'
                )),
                'note': 'Full contract analysis requires ABI'
            }
            
            return result
            
        except Exception as e:
            log.error(f"Error analyzing contract {contract_address}: {e}")
            return {'address': contract_address, 'error': str(e)}
    
    async def track_address(self, address: str, callback=None) -> None:
        """ردیابی real-time یک آدرس"""
        if not self.w3 or not self.w3.is_connected():
            log.error("Cannot track: not connected to blockchain")
            return
        
        address = Web3.to_checksum_address(address)
        previous_balance = self.w3.eth.get_balance(address)
        
        log.info(f"Started tracking address {address}")
        
        while True:
            try:
                current_balance = self.w3.eth.get_balance(address)
                
                if current_balance != previous_balance:
                    change = current_balance - previous_balance
                    
                    event = {
                        'address': address,
                        'previous_balance': float(self.w3.from_wei(previous_balance, 'ether')),
                        'current_balance': float(self.w3.from_wei(current_balance, 'ether')),
                        'change': float(self.w3.from_wei(change, 'ether')),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    
                    log.info(f"Balance change detected for {address}")
                    
                    if callback:
                        await callback(event)
                    
                    previous_balance = current_balance
                
                await asyncio.sleep(15)  # بررسی هر 15 ثانیه
                
            except Exception as e:
                log.error(f"Error tracking address {address}: {e}")
                await asyncio.sleep(60)
    
    async def batch_analyze_addresses(self, addresses: List[str]) -> List[Dict[str, Any]]:
        """آنالیز دسته‌ای آدرس‌ها"""
        tasks = [self.analyze_address(addr) for addr in addresses]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        clean_results = []
        for result in results:
            if isinstance(result, Exception):
                log.error(f"Error in batch analysis: {result}")
            else:
                clean_results.append(result)
        
        return clean_results
    
    def export_to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """تبدیل داده‌های blockchain به DataFrame"""
        try:
            df = pd.DataFrame(data)
            log.info(f"Exported {len(df)} blockchain records to DataFrame")
            return df
        except Exception as e:
            log.error(f"Error exporting to DataFrame: {e}")
            return pd.DataFrame()

blockchain_analyzer = BlockchainAnalyzer()