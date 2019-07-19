from copy import deepcopy
import hashlib
import datetime
import time

CLOCK_DRIFT_TOLERANCE = 0.01 # 1% clock drift in the future

class Block(object):
    def __init__(self, index, previous_hash, timestamp, data, difficulty,
            nonce):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")

        if previous_hash is not None and not isinstance(previous_hash, bytes):
            raise TypeError("Previous hash must be bytes")

        if not isinstance(timestamp, int):
            raise TypeError("Timestamp must be an integer")

        if not isinstance(difficulty, int):
            raise TypeError("Difficulty must be an integer")

        if not isinstance(nonce, int):
            raise TypeError("Nonce must be an integer")

        if index < 0:
            raise ValueError("Index must be non-negative")

        if timestamp < 0:
            raise ValueError("Timestamp must be non-negative")

        if difficulty <= 0 and index != 0 and previous_hash is not None:
            raise ValueError("Difficulty must be positive")

        if previous_hash is None and index != 0:
            raise ValueError("Only genesis block can have null previous hash")

        self.__index = index
        self.__previous_hash = deepcopy(previous_hash)
        self.__timestamp = timestamp
        self.__data = deepcopy(data)
        self.__difficulty = difficulty
        self.__nonce = nonce
        
        if self.__previous_hash is None:
            self.__previous_hash = b"\00"

        self.__hash = self.__generate_hash()

    @property
    def index(self):
        return self.__index

    @property
    def hash(self):
        return deepcopy(self.__hash)

    @property
    def prev(self):
        return deepcopy(self.__previous_hash)

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def data(self):
        return deepcopy(self.__data)

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def nonce(self):
        return self.__nonce

    def get_timestamp_dt(self):
        return datetime.datetime.fromtimestamp(self.__timestamp)

    @staticmethod
    def is_valid(block):
        # block is from the future
        if block.timestamp > int(time.time() * (1 + CLOCK_DRIFT_TOLERANCE)):
            return False

        return True

    def __eq__(self, o):
        return isinstance(o, Block) and \
                self.index == o.index and \
                self.hash == o.hash and \
                self.prev == o.prev and \
                self.timestamp == o.timestamp and \
                self.data == o.data and \
                self.difficulty == o.difficulty and \
                self.nonce == o.nonce
    
    def __generate_hash(self):
        data = self.__data
        
        if isinstance(data, str):
            data = bytes(data, "utf-8")
        
        elems = [bytes(self.__index),
                bytes(self.__previous_hash),
                bytes(self.__timestamp),
                bytes(data),
                bytes(self.__difficulty),
                bytes(self.__nonce)]

        hash_input = b"".join([e for e in elems])
        m = hashlib.sha3_512()
        m.update(hash_input)
        return m.digest()

    def __str__(self):
        return str(self.hash.hex())

    def __repr__(self):
        return  "Index: {}\n"\
                "Hash: {}\n"\
                "Previous Hash: {}\n"\
                "Timestamp: {}\n"\
                "Difficulty: {}\n"\
                "Nonce: {}\n"\
                "Data: {}\n".format(
                        self.index,
                        self.hash.hex(),
                        self.prev.hex(),
                        self.get_timestamp_dt(),
                        self.difficulty,
                        self.nonce,
                        self.data)

