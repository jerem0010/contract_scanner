import subprocess
import json
import re
import sys

def run_cast(args):
    result = subprocess.run(
        ["cast"] + args,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()

def get_code(address, rpc_url):
    return run_cast(["code", address, "--rpc-url", rpc_url])

def get_balance(address, rpc_url):
    return run_cast(["balance", address, "--rpc-url", rpc_url])

def get_nonce(address, rpc_url):
    return run_cast(["nonce", address, "--rpc-url", rpc_url])

def classify_address(address, rpc_url):
    code = get_code(address, rpc_url)
    if code == "0x":
        return "EOA_or_no_code", code
    return "Contract", code

def extract_push4_selectors(bytecode):
    if bytecode.startswith("0x"):
        bytecode = bytecode[2:]

    selectors = set()
    i = 0
    while i < len(bytecode) - 10:
        opcode = bytecode[i:i+2]
        if opcode.lower() == "63":  # PUSH4
            selector = "0x" + bytecode[i+2:i+10]
            selectors.add(selector)
            i += 10
        else:
            i += 2
    return sorted(selectors)

def main():
    if len(sys.argv) != 3:
        print("Usage: python inspect.py <address> <rpc_url>")
        sys.exit(1)

    address = sys.argv[1]
    rpc_url = sys.argv[2]

    kind, code = classify_address(address, rpc_url)
    balance = get_balance(address, rpc_url)
    nonce = get_nonce(address, rpc_url)

    print(f"Address: {address}")
    print(f"Type: {kind}")
    print(f"Balance: {balance}")
    print(f"Nonce: {nonce}")

    if kind == "Contract":
        print(f"Code size: {(len(code)-2)//2} bytes")
        selectors = extract_push4_selectors(code)
        print("Possible selectors:")
        for s in selectors[:50]:
            print(f"  - {s}")

if __name__ == "__main__":
    main()