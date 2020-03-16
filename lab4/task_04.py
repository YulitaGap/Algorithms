import math


class HashTable:
    def __init__(self, hash_type, values):
        self.hash_type = hash_type
        self.values = values
        if hash_type == 1 or hash_type == 2:
            self.hash_table = ChainedHash(hash_type, values)
        elif hash_type == 3 or hash_type == 4 or hash_type == 5:
            self.hash_table = OpenAddressingHash(hash_type, values)
        self.generate()

    def generate(self):
        for val in self.values:
            self.hash_table.insert(val)

    def get_collisions_amount(self):
        if self.hash_type ==1 or self.hash_type ==2:
            return self.hash_table.collisions
        else:
            empty = 0
            for value in self.hash_table.table:
                if value is None:
                    empty += 1
            return len(self.hash_table.values) - self.hash_table.capacity + empty

    def search(self, value):
        return self.hash_table.search(value)

    def find_sum(self, s):
        for a in range(s // 2 + 1):
            if self.hash_table.search(a) and self.hash_table.search(s-a):
                return a, s-a


class Node(object):
    """
    Class for Node representation
    """
    def __init__(self, value=None, next_=None):
        self.value = value
        self.next = next_


class ChainedHash:
    """
    Class for Chained hash tables representation
    """
    def __init__(self, hash_type, values):
        self.collisions = 0
        self.hash_type = hash_type
        self.values = values
        self.capacity = self.count_nearest_prime(len(values) * 3 - 1)
        self.table = [[] for i in range(self.capacity)]
        self.__gold_section = (math.sqrt(5) - 1) / 2

    @staticmethod
    def count_nearest_prime(n):
        primes = []
        limit = n+100
        numbers = [True] * limit
        for i in range(2, limit):
            if numbers[i]:
                primes.append(i)
                for n in range(i ** 2, limit, i):
                    numbers[n] = False
        max_distance = 99999999
        numb = 0
        for p in primes:
            if abs(n - p) < max_distance:
                max_distance = abs(n - p)
                numb = p
        return numb

    def hash(self, key):
        if self.hash_type == 2:
            return int(self.capacity * ((key * self.__gold_section) % 1))
        elif self.hash_type == 1:
            return key % self.capacity

    def insert(self, number):
        key = self.hash(number)
        if self.table[key]:
            self.collisions += 1
        self.table[key].append(number)

    def search(self, number):
        key = self.hash(number)
        if number in self.table[key]:
            return True
        return False


class OpenAddressingHash:
    """
    Class for hash tables with open addressing representation
    """
    def __init__(self, hash_type, values):
        self.hash_type = hash_type
        self.values = values
        self.capacity = self.count_nearest_prime(len(values) * 3 - 1)
        self.table = [None] * self.capacity
        self.__gold_section = (math.sqrt(5) - 1) / 2

    @staticmethod
    def count_nearest_prime(n):
        primes = []
        limit = n + 100
        numbers = [True] * limit
        for i in range(2, limit):
            if numbers[i]:
                primes.append(i)
                for n in range(i ** 2, limit, i):
                    numbers[n] = False
        max_distance = 99999999
        numb = 0
        for p in primes:
            if abs(n - p) < max_distance:
                max_distance = abs(n - p)
                numb = p
        return numb

    def hash_func(self, key, i):
        if self.hash_type == 3:
            return ((key % self.capacity) + i) % self.capacity
        elif self.hash_type == 4:
            return ((key % self.capacity) + i * 2 + i ** 2 * 3) % self.capacity
        elif self.hash_type == 5:
            def hash1(x):
                return x % self.capacity

            def hash2(x):
                return int(self.capacity * (x * self.__gold_section % 1))

            return (hash1(key) + i * hash2(key)) % self.capacity

    def insert(self, value):
        head = self.hash_func(value, 0)
        counter = 0
        current_node = self.table[head]
        if current_node:
            while self.table[head + counter] is not None:
                counter += 1
            self.table[head + counter] = value
        else:
            self.table[head] = value

    def search(self, value):
        counter = 0
        head = self.hash_func(value, counter)
        curr_node = self.table[head]
        if curr_node:
            while self.table[(head + counter) % self.capacity] != value:
                if not self.table[(head + counter) % self.capacity]:
                    return False
                counter += 1
            return True
        else:
            return False
