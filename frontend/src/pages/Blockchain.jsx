import React, { useState } from 'react';
import {
  Blocks,
  Search,
  TrendingUp,
  Activity,
  Wallet,
  FileText,
  Loader,
} from 'lucide-react';
import {
  analyzeBlockchainAddress,
  getTransaction,
  getBlock,
  getGasPrices,
  analyzeContract,
} from '../services/api';
import toast from 'react-hot-toast';

const Blockchain = () => {
  const [activeTab, setActiveTab] = useState('address');
  const [address, setAddress] = useState('');
  const [txHash, setTxHash] = useState('');
  const [blockNumber, setBlockNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [gasPrices, setGasPrices] = useState(null);

  const handleAnalyzeAddress = async () => {
    if (!address) {
      toast.error('Please enter an Ethereum address');
      return;
    }

    if (!/^0x[a-fA-F0-9]{40}$/.test(address)) {
      toast.error('Invalid Ethereum address format');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await analyzeBlockchainAddress(address);
      setResult(response.data);
      toast.success('Address analyzed successfully!');
    } catch (error) {
      console.error('Analysis failed:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGetTransaction = async () => {
    if (!txHash) {
      toast.error('Please enter a transaction hash');
      return;
    }

    if (!/^0x[a-fA-F0-9]{64}$/.test(txHash)) {
      toast.error('Invalid transaction hash format');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await getTransaction(txHash);
      setResult(response.data);
      toast.success('Transaction retrieved successfully!');
    } catch (error) {
      console.error('Failed to get transaction:', error);
      toast.error(error.response?.data?.detail || 'Failed to get transaction');
    } finally {
      setLoading(false);
    }
  };

  const handleGetBlock = async () => {
    if (!blockNumber) {
      toast.error('Please enter a block number');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await getBlock(parseInt(blockNumber));
      setResult(response.data);
      toast.success('Block information retrieved!');
    } catch (error) {
      console.error('Failed to get block:', error);
      toast.error(error.response?.data?.detail || 'Failed to get block');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeContract = async () => {
    if (!address) {
      toast.error('Please enter a contract address');
      return;
    }

    if (!/^0x[a-fA-F0-9]{40}$/.test(address)) {
      toast.error('Invalid contract address format');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await analyzeContract(address);
      setResult(response.data);
      toast.success('Contract analyzed successfully!');
    } catch (error) {
      console.error('Contract analysis failed:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const loadGasPrices = async () => {
    try {
      const response = await getGasPrices();
      setGasPrices(response.data);
    } catch (error) {
      console.error('Failed to load gas prices:', error);
    }
  };

  React.useEffect(() => {
    loadGasPrices();
    const interval = setInterval(loadGasPrices, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const tabs = [
    { id: 'address', name: 'Address Analysis', icon: Wallet },
    { id: 'transaction', name: 'Transaction', icon: Activity },
    { id: 'block', name: 'Block Info', icon: Blocks },
    { id: 'contract', name: 'Smart Contract', icon: FileText },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Blockchain Analysis</h1>
        <p className="text-gray-600 mt-1">
          Analyze Ethereum addresses, transactions, and smart contracts
        </p>
      </div>

      {/* Gas Prices Card */}
      {gasPrices && (
        <div className="card bg-gradient-to-r from-primary-500 to-secondary-500 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold mb-2">Current Gas Prices</h3>
              <div className="flex space-x-6">
                <div>
                  <p className="text-sm opacity-90">Low</p>
                  <p className="text-2xl font-bold">{gasPrices.low || 'N/A'} Gwei</p>
                </div>
                <div>
                  <p className="text-sm opacity-90">Medium</p>
                  <p className="text-2xl font-bold">{gasPrices.medium || 'N/A'} Gwei</p>
                </div>
                <div>
                  <p className="text-sm opacity-90">High</p>
                  <p className="text-2xl font-bold">{gasPrices.high || 'N/A'} Gwei</p>
                </div>
              </div>
            </div>
            <TrendingUp className="h-12 w-12 opacity-75" />
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="card">
        <div className="flex space-x-2 border-b border-gray-200 pb-4 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-primary-500 text-white shadow-lg'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.name}</span>
            </button>
          ))}
        </div>

        {/* Address Analysis Tab */}
        {activeTab === 'address' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ethereum Address
              </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                className="input-primary font-mono"
              />
              <p className="text-xs text-gray-500 mt-1">
                Enter a valid Ethereum address (0x...)
              </p>
            </div>

            <button
              onClick={handleAnalyzeAddress}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Search className="h-4 w-4" />
                  <span>Analyze Address</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Transaction Tab */}
        {activeTab === 'transaction' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Transaction Hash
              </label>
              <input
                type="text"
                value={txHash}
                onChange={(e) => setTxHash(e.target.value)}
                placeholder="0x..."
                className="input-primary font-mono"
              />
              <p className="text-xs text-gray-500 mt-1">
                Enter a valid transaction hash (0x... 64 characters)
              </p>
            </div>

            <button
              onClick={handleGetTransaction}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <Activity className="h-4 w-4" />
                  <span>Get Transaction</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Block Info Tab */}
        {activeTab === 'block' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Block Number
              </label>
              <input
                type="number"
                value={blockNumber}
                onChange={(e) => setBlockNumber(e.target.value)}
                placeholder="18500000"
                className="input-primary"
              />
              <p className="text-xs text-gray-500 mt-1">
                Enter a block number to view its information
              </p>
            </div>

            <button
              onClick={handleGetBlock}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <Blocks className="h-4 w-4" />
                  <span>Get Block Info</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Smart Contract Tab */}
        {activeTab === 'contract' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contract Address
              </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="0x..."
                className="input-primary font-mono"
              />
              <p className="text-xs text-gray-500 mt-1">
                Enter a smart contract address to analyze
              </p>
            </div>

            <button
              onClick={handleAnalyzeContract}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4" />
                  <span>Analyze Contract</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Results</h3>
            <span className="badge badge-success">Success</span>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 overflow-auto max-h-96">
            <pre className="text-sm text-gray-800">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Wallet className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Address Analysis</h4>
              <p className="text-sm text-gray-600">
                View balance, transaction history, and token holdings for any address.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-purple-100 p-2 rounded-lg">
              <Activity className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Transaction Tracking</h4>
              <p className="text-sm text-gray-600">
                Get detailed information about any Ethereum transaction.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-green-100 p-2 rounded-lg">
              <FileText className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Smart Contracts</h4>
              <p className="text-sm text-gray-600">
                Analyze smart contract code, functions, and interactions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Blockchain;

// Location: datanex-frontend/src/pages/Blockchain.jsx
