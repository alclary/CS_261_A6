# Name: Anthony Logan Clary
# OSU Email: claryan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: Assignment 6: HashMap Implementation

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        """Updates or inserts the given key/value pair in the hash map. If given
            key is already in the hash map, value will be replaced.

        Args:
            key (str): key to search hash map for and insert/update value for
            value (object): value to associate with given key in hash map
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        j = 1
        key_hash = self._hash_function(key)
        og_index = key_hash % self._capacity
        index = og_index

        while True:
            # create new value
            if self._buckets[index] is None:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            elif self._buckets[index].key == key:
                # reactivate tombstoned value
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index].value = value
                    self._buckets[index].is_tombstone = False
                    self._size += 1
                    return
                # change already existing value
                elif self._buckets[index].is_tombstone is False:
                    self._buckets[index].value = value
                    return
            # proceed to next possible index (quadratic + og_index); can wrap
            else:
                index = (og_index + (j ** 2)) % self._capacity
                j += 1

    def table_load(self) -> float:
        """Returns the current hash table load factor"""
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash table

        Returns:
            int: number of empty buckets in hash table
        """
        empty_buckets = 0

        for i in range(self._capacity):
            if self._buckets[i] is None:
                empty_buckets += 1

        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the internal hash table. All existing key/
            value pairs are rehashed based on new_capacity. Method will fail
            silently if new_capacity is less than current number of elements
            (i.e. current size). If given new_capacity is not a prime number,
            map will find next prime to use as new capacity.

        Args:
            new_capacity (int): new capacity to assign to the intern hash table
                and rehash existing keys to.
        """
        if new_capacity < self._size:
            return
        elif self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # preserve previous hash map
        old_table = self._buckets
        self._capacity = new_capacity
        self.clear()

        # rehash keys from old map; ignore empty or tombstoned keys
        for i in range(old_table.length()):
            bucket = old_table[i]
            if bucket is None:
                continue
            elif bucket.is_tombstone is True:
                continue
            else:
                self.put(bucket.key, bucket.value)
        return

    def get(self, key: str) -> object:
        """Returns the value associated with the given key, if that key exists
            in the current hash map. Returns None if key does not exist.

        Args:
            key (str): key to search hash map for, and if exists return value of

        Returns:
            object: value of given key if found, otherwise None
        """
        if self._capacity <= 0:
            return None

        j = 1
        key_hash = self._hash_function(key)
        og_index = key_hash % self._capacity
        index = og_index

        for _ in range(self._capacity):
            bucket = self._buckets[index]
            if bucket is not None:
                if bucket.key == key and bucket.is_tombstone is False:
                    return self._buckets[index].value
            index = (og_index + (j ** 2)) % self._capacity
            j += 1

        return None

    def contains_key(self, key: str) -> bool:
        """Returns True if the given key is in the hash map, otherise False. An
            empty hash map does not contain any keys.

        Args:
            key (str): key to search hash map for.

        Returns:
            bool: True if key found in hash map, otherwise False
        """
        if self._capacity <= 0:
            return False
        elif self.get(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """Removes the given key and its associated value from the hash map if
            the key exists. If key does not exist in map, returns silently.

        Args:
            key (str): key of key/value pair to remove from hash map if found
        """
        if self._capacity <= 0:
            return

        j = 1
        key_hash = self._hash_function(key)
        og_index = key_hash % self._capacity
        index = og_index

        # searches hash map for key, if found bucket is "tombstoned"
        for _ in range(self._capacity):
            if self._buckets[index] is not None:
                if self._buckets[index].key == key and \
                    self._buckets[index].is_tombstone is False:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return
            index = (og_index + (j ** 2)) % self._capacity
            j += 1

        return None

    def clear(self) -> None:
        """Clears the contents of the hash map. Underlying capacity is not
            changed
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)
        return

    def get_keys_and_values(self) -> DynamicArray:
        """Returns a dynamic array where each index contains a tuple of key/
            value pair(s) stored in the hash map. Returned array is not
            necessarily ordered.

        Returns:
            DynamicArray: array containing key/value pairs from hash map stored
                in tuples
        """
        keys_and_values = DynamicArray()

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            if bucket is None:
                continue
            elif bucket.is_tombstone is True:
                continue
            else:
                keys_and_values.append((bucket.key, bucket.value))

        return keys_and_values

    def __iter__(self):
        """
        Define iterator index counter
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Advance iterator to next active bucket (i.e. skip empty or tombstoned
            buckets)
        """
        try:
            while True:
                bucket = self._buckets[self._index]
                if bucket is None:
                    self._index = self._index + 1
                    continue
                elif bucket.is_tombstone is True:
                    self._index = self._index + 1
                    continue
                else:
                    break
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return bucket


# ------------------- BASIC TESTING ---------------------------------------- #

# if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
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
    # m = HashMap(11, hash_function_1)
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

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
