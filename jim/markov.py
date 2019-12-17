from collections import defaultdict
import pickle
import random


class Markov():
    """The chain generating part of the program!"""

    def __init__(self, stop_condition, starting_symbols=None, memory_bytes=None):
        if memory_bytes:
            self._memory = pickle.loads(memory_bytes)
        else:
            self._memory = defaultdict(list)
        self._stop_condition = stop_condition
        self._starting_symbols = starting_symbols

    def chains(self):
        while True:
            symbol = self._get_starting_symbol()
            chain = [symbol]
            while not self._stop_condition(chain):
                symbol = random.choice(self._memory[symbol])
                if symbol is None:
                    break
                chain.append(symbol)

            yield chain

    def _get_starting_symbol(self):
        if self._starting_symbols:
            starting_symbol = random.choice(self._starting_symbols)
            return random.choice(self._memory[starting_symbol])
        else:
            return random.choice(list(self._memory.keys()))

    def memory_bytes(self):
        return pickle.dumps(self._memory)

    def _fetch_pair(self, symbols):
        for i in range(0, len(symbols) - 1):
            yield symbols[i], symbols[i + 1]

    def learn(self, symbols):
        '''Pass a list for the markov chain to learn from'''
        for key, val in self._fetch_pair(symbols):
            self._memory[key] += [val]
