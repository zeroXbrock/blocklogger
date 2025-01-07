import fs from 'fs/promises';

// lib
import { BlockReader } from './lib/getData';

const datafile = 'storageData.json';

// Define the URL and block range
const [nodeUrl, startBlockStr, endBlockStr] = process.argv.slice(2);
const startBlock = parseInt(startBlockStr, 10);
const endBlock = parseInt(endBlockStr, 10);

if (!nodeUrl || isNaN(startBlock) || isNaN(endBlock)) {
    console.error('Usage: bun run index.ts <nodeUrl> <startBlock> <endBlock>');
    process.exit(1);
}

/** Process blocks and write the result to the given file. */
async function saveBlocks(blockReader: &BlockReader, filepath: string) {
    await blockReader.processBlocks(startBlock, endBlock).then(async (data) => {
        await fs.writeFile(filepath, JSON.stringify(data, null, 2));
        console.log('Finished processing blocks.');
    }).catch((error) => {
        console.error('Error processing blocks:', error);
    });
}

async function main() {
    const blockReader = new BlockReader(nodeUrl);
    await saveBlocks(blockReader, datafile);
}

main()

