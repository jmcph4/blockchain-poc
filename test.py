from blockchain_poc.block import Block
from blockchain_poc.blockchain import Blockchain

chain = Blockchain()
new_block = Block(
        1,
        bytes.fromhex("963e34534a16a7d3987daa3aa7c0709e6b096e6bb71da67245304318acdd2e17e41c4e21a81dc93035cab213f62af9233dd8c51b11bdf9a4c3bd4276935fe038"),
        1563527202,
        "Hello, world!",
        1,
        19)
chain.add_data("Hello, world!")
chain.add_data("A" * 64)

