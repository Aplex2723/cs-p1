from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes

# 1. Generación de claves RSA (Bob)
key = RSA.generate(1024)
private_key = key.export_key()
public_key = key.publickey().export_key()

# 2. Preparación del mensaje (Alice)
mensaje_original = "M" * 1050  # Mensaje de 1050 caracteres
bloques = [mensaje_original[i:i+128] for i in range(0, 1050, 128)]

# 3. Cifrado (Alice)
cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
bloques_cifrados = [cipher.encrypt(bloque.encode()) for bloque in bloques]
hM = SHA256.new(mensaje_original.encode()).hexdigest()

# 4. Transmisión (simulada)
# Enviar bloques_cifrados y hM a Bob

# 5. Descifrado y verificación (Bob)
cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
bloques_descifrados = [cipher.decrypt(bloque_cifrado).decode() for bloque_cifrado in bloques_cifrados]
M_prima = "".join(bloques_descifrados)
hM_prima = SHA256.new(M_prima.encode()).hexdigest()

# Verificación
autentico = (hM == hM_prima)
print("Mensaje auténtico:", autentico)