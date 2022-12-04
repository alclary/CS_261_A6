# Name: Anthony Logan Clary
# OSU Email: claryan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: Assignment 6: HashMap Implementation

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """Updates or inserts the given key/value pair in the hash map. If the
            given key already exists, the previous value is overwritten.

        Args:
            key (str): key of key/value pair to be added to hash map
            value (object): value of key/value pair to be added to hash map
        """
        # if table is overloaded, double size
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        key_hash = self._hash_function(key)
        index = key_hash % self._capacity

        if self._buckets[index].length() == 0:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value
                    return
            self._buckets[index].insert(key, value)
            self._size += 1
        return

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash table

        Returns:
            int: number of currently empty buckets
        """
        empty_buckets = 0

        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """Returns the current hash table load factor

        Returns:
            float: current load factor of the hash map
        """
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """Clears the contents of the hash map. Does not change capacity"""
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        return

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the internal hash table. All existing key/
            value pairs are rehashed based on the new capacity. If new capacity
            is less than 1, return with no changes.

        Args:
            new_capacity (int): new capacity for table (if not prime, method
                will find the next prime)
        """
        if new_capacity < 1:
            return
        elif self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # preserve previous map
        old_table = self._buckets
        self._capacity = new_capacity
        self.clear()

        # rehash existing key/value pairs
        for i in range(old_table.length()):
            bucket = old_table[i]
            if bucket.length() == 0:
                continue
            else:
                for node in bucket:
                    self.put(node.key, node.value)
        return

    def get(self, key: str):
        """Returns the value associated with the given key. If the key is not
            in the hash table, returns None.

        Args:
            key (str): key to find value for in hash table

        Returns:
            object: paired value if key is found, otherwise None.
        """
        key_hash = self._hash_function(key)
        index = key_hash % self._capacity

        if self.contains_key(key):
            bucket = self._buckets[index]
        else:
            return None

        for node in bucket:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """Returns True if the given key is in the hash map, otherwise returns
            False. An empty hash map does not contain any keys.

        Args:
            key (str): key to search for in hash map

        Returns:
            bool: True if given key found, otherwise False.
        """
        key_hash = self._hash_function(key)
        index = key_hash % self._capacity

        if index in range(self._capacity):
            bucket = self._buckets[index]
        else:
            return False

        if bucket.length() == 0:
            return False
        else:
            for node in bucket:
                if node.key == key:
                    return True

        return False

    def remove(self, key: str) -> None:
        """Removes given key and its value pair if key exists in the hash map.
            If the key is not in the hashmap return silently.

        Args:
            key (str): key to search for and remove from hash map
        """
        key_hash = self._hash_function(key)
        index = key_hash % self._capacity

        if self.contains_key(key):
            self._buckets[index].remove(key)
            self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """Returns a dynamic array where each index contains a tuple of a
            a key/value pair stored in the hash map. Array is not necessarily
            ordered.

        Returns:
            DynamicArray: array containing key/value pairs of hash map in tuples
        """
        keys_and_values = DynamicArray()

        for i in range(self._buckets.length()):
            for node in self._buckets[i]:
                keys_and_values.append((node.key, node.value))

        return keys_and_values

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """Returns a tuple containing a dynamic array comprising the mode value(s)
        of the array, and an integer representing the highest frequency.

    Args:
        da (DynamicArray): dynamic array to locate mode value(s) and mode of

    Returns:
        DynamicArray: mode value(s)/most occuring values from array
        int: mode (highest frequency)
    """
    map = HashMap()
    mode = 0
    mode_list = DynamicArray()


    # create a frequency hashmap
    for i in range(da.length()):
        key = da[i]

        # if key already exists increase count, else single count
        mapped_value = map.get(key)

        if mapped_value:
            value = mapped_value + 1
        else:
            value = 1

        # insert or replace key in hashmap
        map.put(da[i], value)

        # see if key count meets or breaks previous best mode
        if value == mode:
            mode_list.append(key)
        elif value > mode:
            mode = value
            mode_list = DynamicArray()
            mode_list.append(key)

    return (mode_list, mode)

# ------------------- BASIC TESTING ---------------------------------------- #

# if __name__ == "__main__":

#     print("\nPDF - put example 1")
#     print("-------------------")
#     m = HashMap(53, hash_function_1)
#     for i in range(150):
#         m.put('str' + str(i), i * 100)
#         if i % 25 == 24:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

#     print("\nPDF - put example 2")
#     print("-------------------")
#     m = HashMap(41, hash_function_2)
#     for i in range(50):
#         m.put('str' + str(i // 3), i * 100)
#         if i % 10 == 9:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"],
    # )

    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
