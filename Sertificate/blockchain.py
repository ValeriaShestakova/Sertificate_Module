import hashlib
import json
import pickle


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.new_block('', previous_hash=1)

    def new_block(self, results, previous_hash):
        """
                Create a new Block in the Blockchain

                :param previous_hash: (Optional) <str> Hash of previous Block
                :return: <dict> New Block
                """
        index = len(self.chain) + 1
        block = {
            'index': index,
            'data': results,
            'previous_hash': previous_hash,
        }

        self.chain.append(block)
        return block

    def full_chain(self):
        full_chain = {
            'chain': self.chain,
            'length': len(self.chain),
        }
        return full_chain

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            last_block = block
            current_index += 1
        return True

    def get_data(self, hash):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        current_index = 1
        ans = {}
        while current_index < len(self.chain):
            block = self.chain[current_index]
            if block['previous_hash'] == hash:
                block = self.chain[current_index-1]
                ans = block['data']
                break
            current_index += 1
        return ans

    def add_block(self, results):
        last_block = self.last_block
        previous_hash = self.hash(last_block)
        block = self.new_block(results, previous_hash)
        current_hash = self.hash(block)
        return current_hash

    def save_blockchain(self):
        with open('data.txt', 'wb') as f:
            pickle.dump(self.chain, f)
        return 'Saved'

    @staticmethod
    def hash(block):
        """
                Creates a SHA-256 hash of a Block

                :param block: <dict> Block
                :return: <str>
                """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]


