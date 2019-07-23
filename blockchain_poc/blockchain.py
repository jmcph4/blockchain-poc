from copy import deepcopy
import time
import datetime
import json
from .block import Block

BLOCK_GENERATION_INTERVAL = 10          # 10 seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10     # 10 blocks
DEFAULT_INITIAL_DIFFICULTY = 1


class Blockchain(object):
    def __init__(self):
        genesis_block = self.__generate_genesis_block()
        self.__blocks = [genesis_block]

    @property
    def blocks(self):
        return deepcopy(self.__blocks)

    def get_latest_block(self):
        return deepcopy(self.__blocks[-1])

    def add_data(self, data):
        prev_block = self.get_latest_block()

        new_index = prev_block.index + 1
        new_timestamp = int(time.time())
        difficulty = self.get_difficulty()
        
        # mine new block
        nonce = 0

        while True:
            new_block = Block(new_index,
                    prev_block.hash,
                    new_timestamp,
                    data,
                    difficulty,
                    nonce)

            print(datetime.datetime.now(), nonce, new_block.hash.hex(), flush=True) # DEBUG

            if self.__validate_hash(new_block.hash, difficulty):
                self.__blocks.append(new_block)
                return new_block

            nonce += 1

    def add_block(self, block):
        candidate_blocks = self.__blocks + [block]

        if Block.is_valid(block) and \
                Blockchain.__validate_raw_blocks(candidate_blocks):
                    self.__blocks.append(block)
    
    def get_difficulty(self):
        latest_block = self.get_latest_block()

        if latest_block.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and \
                latest_block.index > 0:
            return self.__get_adjusted_difficulty()
        else:
            return latest_block.difficulty

    def load_from_json(self, json_string):
        data = json.loads(json_string)

        for block_json in data:
            index = block_json["index"]
            hash = bytes.fromhex(block_json["hash"])
            prev = bytes.fromhex(block_json["prev"])
            timestamp = block_json["timestamp"]
            data = block_json["data"]
            difficulty = block_json["difficulty"]
            nonce = block_json["nonce"]

            block = Block(
                    index,
                    prev,
                    timestamp,
                    data,
                    difficulty,
                    nonce)
            self.add_block(block)

    def __get_adjusted_difficulty(self):
        prev_adjustment_block = self.__blocks[len(self) - \
                DIFFICULTY_ADJUSTMENT_INTERVAL]
        expected_time = BLOCK_GENERATION_INTERVAL * \
                DIFFICULTY_ADJUSTMENT_INTERVAL
        actual_time = latest_block.timestamp - prev_adjustment_block.timestamp

        if time_taken < expected_time / 2:
            return prev_adjustment_block.difficulty + 1
        elif time_taken > expected_time * 2:
            return prev_adjustment_block.difficulty - 1
        else:
            return prev_adjustment_block.difficulty

    def as_json(self):
        return json.dumps([block.as_dict() for block in self.__blocks])

    def __len__(self):
        return len(self.__blocks)

    @staticmethod
    def __generate_genesis_block():
        index = 0
        prev = None
        timestamp = int(time.time())
        data = b""
        difficulty = DEFAULT_INITIAL_DIFFICULTY
        nonce = 0

        genesis_block = Block(index, prev, timestamp, data, difficulty, nonce)

        return deepcopy(genesis_block)

    @staticmethod
    def __validate_hash(hash, difficulty):
        return hash[:difficulty] == b"\0" * difficulty

    @staticmethod
    def is_valid(blockchain):
        return self.__validate_raw_blocks(blockchain.blocks)

    @staticmethod
    def __validate_raw_blocks(blocks):
        for i in range(1, len(blocks)):
            curr_block = blocks[i]
            prev_block = blocks[i-1]

            if not Block.is_valid(curr_block):
                return False

            if not curr_block.prev != prev_block.hash:
                return False

            if curr_block.index != prev_block.index + 1:
                return False

        return True

