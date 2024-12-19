import axios from 'axios';
import fs from 'fs';

// Define the URL and block range
const nodeUrl = 'https://sepolia.unichain.org'; // Replace with your Ethereum node URL
const startBlock = 7638184; // Starting block number
const endBlock = 7638199; // Ending block number

/**
 * Calls `debug_traceTransaction` for the given transaction hash.
 * @param {string} txHash - The transaction hash to trace.
 * @returns {Promise<any>} - The trace object returned by the Ethereum node.
 */
async function traceTransaction(txHash: string): Promise<any> {
    try {
        const response = await axios.post(nodeUrl, {
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
async function getBlockTransactions(blockNumber: number): Promise<string[]> {
    try {
        const response = await axios.post(nodeUrl, {
            jsonrpc: '2.0',
            method: 'eth_getBlockByNumber',
            params: [
                `0x${blockNumber.toString(16)}`, // Convert block number to hex
                true // Include full transaction objects
            ],
            id: 1
        });
        const blockData = response.data.result;
        return blockData.transactions.map((tx: any) => tx.hash);
    } catch (error) {
        console.error(`Error fetching block ${blockNumber}:`, error);
        return [];
    }
}

/**
 * Logs the block number and number of storage slots for each transaction trace.
 * @param {number} startBlock - The starting block number.
 * @param {number} endBlock - The ending block number.
 */
async function processBlocks(startBlock: number, endBlock: number): Promise<{
    blockNumber: number;
    txHash: string;
    storageSlots: (string[] | null)[];
}[]> {
    let blockData = [];
    for (let blockNumber = startBlock; blockNumber <= endBlock; blockNumber++) {
        const transactionHashes = await getBlockTransactions(blockNumber);
        for (const txHash of transactionHashes) {
            const trace = await traceTransaction(txHash);
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
                };
                blockData.push(
                    data
                );
                console.log(data);
            } else {
                console.log(`Block: ${blockNumber}, Tx: ${txHash}, Trace not available`);
            }
        }
    }
    return blockData;
}

// Start processing the blocks
processBlocks(startBlock, endBlock).then((data) => {
    fs.writeFileSync('pubUni.json', JSON.stringify(data, null, 2));
    console.log('Finished processing blocks.');
}).catch((error) => {
    console.error('Error processing blocks:', error);
});
