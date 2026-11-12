import hashlib
import time
from typing import List, Optional

class Block:
    # Create __init__ to take a property
    def __init__(self, index: int, previous_hash: str, data: str, timestamp: Optional[float] = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()  
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()          

    # Create the hash function
    def calculate_hash(self) -> str:               
        # combine all the data into one str
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    # Create a proof of work 
    def mineblock(self, difficulty: int) -> None:
        target = "0" * difficulty
        while not self.hash.startswith(target):    
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined: {self.hash}")


# Create BlockChain
class BlockChain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self) -> Block:
        return Block(index=0, previous_hash="0", data="Genesis Block", timestamp=1700000000.0)

    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_block(self, data: str) -> None:
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            data=data
        )
        new_block.mineblock(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash in block {current_block.index}")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Broken link between block {previous_block.index} and {current_block.index}")
                return False

        return True

if __name__ == "__main__":
    # Initialize blockchain with a difficulty of 2 (hashes must start with '00')
    my_coin = BlockChain(difficulty= 4)

    print("Mining Block 1...")
    my_coin.add_block("Alice sent 5 coins to Bob")

    print("Mining Block 2...")
    my_coin.add_block("Bob sent 2 coins to Charlie")

    print("Mining Block 3...")
    my_coin.add_block("Bob sent 2 coins to Charlie")

    # Verify blockchain integrity
    print(f"\nIs blockchain valid? {my_coin.is_chain_valid()}")

    # Tampering with the data
    print("\nTampering with Block 1 data...")
    my_coin.chain[1].data = "Alice sent 500 coins to Hacker"
    
    print(f"Is blockchain valid after tampering? {my_coin.is_chain_valid()}")