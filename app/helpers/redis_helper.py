import redis
import faiss
import pickle

index = faiss.IndexFlatL2(256)
array = ['1', '2', '3']

# Serialize the index object
serialized_index = pickle.dumps(index)

# Create a Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a key-value pair
r.set('mykey', serialized_index)
r.set('mykey2', pickle.dumps(array))

# Retrieve the value for a key
serialized_value = r.get('mykey')

# Deserialize the value
deserialized_index = pickle.loads(serialized_value)

# Use the deserialized index object
print(deserialized_index)
print(index)

print(pickle.loads(r.get('mykey2')))