import bcrypt

password = b"super secret password"

# Hash a password for the first time, with a certain number of rounds
hashed = bcrypt.hashpw(password, bcrypt.gensalt(13))

print(hashed)

# Check that a unhashed password matches one that has previously been
# hashed
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
	print("It Does not Match :(")