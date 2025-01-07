import axios from 'axios';

export class BlockReader {
    nodeUrl: string;

    constructor(nodeUrl: string) {
        this.nodeUrl = nodeUrl;
    }

    /**
     * Calls `debug_traceTransaction` for the given transaction hash.
     * @param {string} txHash - The transaction hash to trace.
     * @returns {Promise<any>} - The trace object returned by the Ethereum node.
     */
    async traceTransaction(txHash: string): Promise<any> {
        try {
            const response = await axios.post(this.nodeUrl, {
                jsonrpc: '2.0',
                method: 'debug_traceTransaction',
                params: [txHash, {tracer: "prestateTracer"}],
                id: 1
            });
            return response.data.result;
        } catch (error) {
            console.error(`Error tracing transaction ${txHash}:`, error);
            return null;
        }
    }
    
    /**
     * Retrieves the list of transaction hashes for a given block number.
     * @param {number} blockNumber - The block number to retrieve transactions from.
     * @returns {Promise<string[]>} - A list of transaction hashes in the block.
     */
    async getBlock(blockNumber: number): Promise<any> {
        try {
            const response = await axios.post(this.nodeUrl, {
                jsonrpc: '2.0',
                method: 'eth_getBlockByNumber',
                params: [
                    `0x${blockNumber.toString(16)}`, // Convert block number to hex
                    true // Include full transaction objects
                ],
                id: 1
            });
            return response.data.result;
        } catch (error) {
            console.error(`Error fetching block ${blockNumber}:`, error);
            return [];
        }
    }

    async getTransactionReceipt(txHash: string): Promise<any> {
        try {
            const response = await axios.post(this.nodeUrl, {
                jsonrpc: '2.0',
                method: 'eth_getTransactionReceipt',
                params: [
                    txHash
                ],
                id: 1
            });
            return response.data.result;
        } catch (error) {
            console.error(`Error fetching transaction receipt ${txHash}:`, error);
            return null;
        }
    }
    
    /**
     * Logs the block number and number of storage slots for each transaction trace.
     * @param {number} startBlock - The starting block number.
     * @param {number} endBlock - The ending block number.
     */
    async processBlocks(startBlock: number, endBlock: number): Promise<{txs: {
        blockNumber: number;
        txHash: string;
        storageSlots: (string[] | null)[];
        receipt: any;
    }[], blocks: any[]}> {
        let txs: any[] = [];
        let blocks: any[] = [];
        for (let blockNumber = startBlock; blockNumber <= endBlock; blockNumber++) {
            const blockData = await this.getBlock(blockNumber);
            blocks.push(blockData);
            const transactionHashes = blockData.transactions.map((tx: any) => tx.hash);
            for (const txHash of transactionHashes) {
                const trace = await this.traceTransaction(txHash);
                const receipt = await this.getTransactionReceipt(txHash);
                if (trace) {
                    let storageSlots = [];
                    for (const key of Object.keys(trace)) {
                        // console.log("Trace:", trace);
                        const txSlots = trace[key].storage ? Object.keys(trace[key].storage) : null;
                        storageSlots.push(txSlots);
                    }
                    let data = {
                        blockNumber,
                        txHash,
                        storageSlots,
                        receipt,
                    };
                    txs.push(
                        data
                    );
                    console.log(data);
                } else {
                    console.log(`Block: ${blockNumber}, Tx: ${txHash}, Trace not available`);
                }
            }
        }
        return {blocks, txs};
    }

}

