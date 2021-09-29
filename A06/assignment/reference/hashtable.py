"""Initializes a Map with the a specified number of buckets."""
def new(number_of_buckets = 128):

    hmap = []
    for i in range(0, number_of_buckets):
        hmap.append([])
    return hmap

"""Takes a key, create a hash number from it and then convert it to an index for the hashmap's bucket."""
def hash_key(hmap, key):
    return hash(key) % len(hmap)

"""Given a key, get the bucket index."""
def get_bucket(hmap, key):
    bucket_id = hash_key(hmap, key)
    return hmap[bucket_id]

"""Returns the index, key, and value of a slot found in a bucket. Returns -1, key, and none when not found."""
def get_slot(hmap, key, default=None):
    bucket = get_bucket(hmap, key)

    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return i, k, v

    return -1, key, default

"""Set the key to the value or replacing any existing value."""
def set(hmap, key, value):
    bucket = get_bucket(hmap, key)
    i, k, v = get_slot(hmap, key)

    if i >= 0:
        """If the key exists, replace it"""
        bucket[i] = (key, value)
    else:
        """the key does not, append to create it"""
        bucket.append((key, value))

"""Gets the value in a bucket for the given key if it exist"""
def get(hmap, key, default=None):
    i, k, v = get_slot(hmap, key, default=default)
    return v

"""Deletes the given key from the Map."""
def delete(hmap, key):
    bucket = get_bucket(hmap, key)

    for i in range(len(bucket)):
        k, v = bucket[i]
        if key == k:
            del bucket[i]
            break

""" Print bucket content"""
def list(hmap):
    n=0
    for bucket in hmap:
        if bucket:
            for k, v in bucket:
                n+=1

    print(n)