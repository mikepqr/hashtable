class hashtable(object):

    def __init__(self, num_buckets=256):
        # create a list of num_buckets empty lists (buckets), i.e.
        # [ [], [], [], [] ... [] ]
        self.table = []
        for i in range(0, num_buckets):
            self.table.append([])

        self.length = 0

    def hash_key(self, key):
        # given a key, produce a value in the 0 < hash_key < len(table) using
        # hash() built-in
        return hash(key) % len(self.table)

    def get_bucket(self, key):
        # get the contents of the bucket containing key
        bucket_id = self.hash_key(key)
        return self.table[bucket_id]

    def get_slot(self, key, default=None):
        '''
        Get the index, key and value of the slot containing key. index = -1 and
        value = default if key not found.
        '''
        # first determine which bucket contains the slot containing key
        bucket = self.get_bucket(key)

        # search through this bucket for key, and return if found. search is
        # enumerate because this function is required to return index of bucket
        # as well as its contents
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                return i, k, v

        return -1, key, default

    def get(self, key, default=None):
        '''
        Gets the value of key
        '''
        # convenience wrapper around get_slot that returns only the value (not
        # the index and key)
        i, k, v = self.get_slot(key, default=None)
        return v

    def set(self, key, value):
        '''
        Set the value of key
        '''

        # Get the contents of the bucket in which key should be stored
        bucket = self.get_bucket(key)
        # Get the contents of the slot in which key should be stored
        i, k, v = self.get_slot(key)

        # If key is found (i.e. if i != -1), rewrite k, v pair
        if i >= 0:
            bucket[i] = (key, value)
        # If not found, append k, v pair
        else:
            bucket.append((key, value))
            self.length += 1

    def delete(self, key):
        '''
        Delete a key
        '''

        # Get the contents of the bucket in which key should be stored
        bucket = self.get_bucket(key)

        # Linear search for key
        for i in xrange(len(bucket)):
            k, v = bucket[i]
            if key == k:
                del bucket[i]
                self.length -= 1
                break

    def __len__(self):
        return self.length


def test_hashtable():
    x = hashtable(num_buckets=256)

    # test set and get
    x.set(1, 3)
    assert x.get(1) == 3
    assert len(x) == 1

    # test overwrite
    x.set(1, "hello")
    assert x.get(1) == "hello"
    assert len(x) == 1

    # test modify in place
    x.set(1, x.get(1) * 3)
    assert x.get(1) == "hellohellohello"
    assert len(x) == 1

    # test length and more keys than buckets
    n = 300
    for i in range(n):
        x.set(i, i)
    assert len(x) == n
