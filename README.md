# blocklogger

*thank ChatGPT for this absolute abomination.*

scans blocks for storage access and generates graphs:

- storage slot heatmap
- gas-per-block chart
- time-to-inclusion histogram
- tx gas usage histogram

then compile that business into a markdown file.

---

To install dependencies:

```bash
bun install
pip install -r requirements.txt
```

> 🐍 tested with python `3.9.18`, may work on others.

To run:

```bash
./run-report.sh
```

---

> 🤦 author's note: This is a pile of garbage. This functionality will most likely be migrated to [contender](https://github.com/flashbots/contender) and this repo will be deprecated.
