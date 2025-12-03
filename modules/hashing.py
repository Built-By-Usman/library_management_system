from pwdlib import PasswordHash


PasswordHash=PasswordHash.recommended()

def getHashedPassword(password):
    return PasswordHash.hash(password)

def verifyPassword(plainPassword,hashedPassword):
    return PasswordHash.verify(plainPassword,hashedPassword)