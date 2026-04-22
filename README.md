# Contract Inspector

Small CLI tool using Foundry `cast` to inspect Ethereum contracts.

## Features

- Get balance, nonce, chain id
- Fetch bytecode
- Extract function selectors
- Resolve selectors via my own custom 4byte (extract_push4_selectors())

## Usage

```bash
python3 scan.py <address> <rpc_url>
