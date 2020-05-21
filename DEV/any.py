import hashlib

arg = 'md5'
string = 'test1'.encode('ascii')
md5_hash = getattr(hashlib, arg)(string).hexdigest()

print(md5_hash)