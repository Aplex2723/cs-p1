
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from PyPDF2 import PdfReader, PdfWriter
import base64
import os

def generar_claves(nombre, tamano=1024):
    """Genera un par de claves RSA y las guarda en archivos"""
    key = RSA.generate(tamaño)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Guardar claves en archivos
    with open(f"{nombre}_privada.pem", "wb") as f:
        f.write(private_key)

    with open(f"{nombre}_publica.pem", "wb") as f:
        f.write(public_key)

    return private_key, public_key

def obtener_hash_pdf(pdf_path):
    """Calcula el hash SHA-256 del contenido del PDF"""
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()

    h = SHA256.new(pdf_content)
    return h

def firmar_documento(pdf_path, clave_privada_path, output_path=None):
    """Firma un documento PDF con la clave privada y devuelve la firma"""
    if output_path is None:
        output_path = pdf_path.replace('.pdf', '_firmado.pdf')

    # Obtener hash del documento
    hash_documento = obtener_hash_pdf(pdf_path)

    # Cargar clave privada
    with open(clave_privada_path, 'rb') as f:
        private_key = RSA.import_key(f.read())

    # Firmar el hash
    firma = pkcs1_15.new(private_key).sign(hash_documento)

    # Codificar la firma como base64 (para facilitar su manipulación como texto)
    firma_base64 = base64.b64encode(firma).decode('utf-8')

    # Agregar la firma al PDF
    agregar_firma_a_pdf(pdf_path, firma_base64, output_path)

    return firma_base64

def agregar_firma_a_pdf(pdf_path, firma, output_path):
    """Agrega la firma como metadato al PDF"""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copiar todas las páginas al nuevo PDF
    for page in reader.pages:
        writer.add_page(page)

    # Agregar firma como metadato
    writer.add_metadata({
        "/Signature": firma
    })

    # Guardar el PDF firmado
    with open(output_path, "wb") as f:
        writer.write(f)

def verificar_firma(pdf_path, clave_publica_path):
    """Verifica la firma de un PDF usando la clave pública"""
    # Obtener la firma del PDF
    reader = PdfReader(pdf_path)
    firma_base64 = reader.metadata.get('/Signature')

    if not firma_base64:
        return False, "El documento no contiene una firma digital"

    # Decodificar la firma
    firma = base64.b64decode(firma_base64)

    # Obtener hash del documento original (sin la firma)
    # Para esto, creamos una copia temporal sin la firma
    temp_pdf = pdf_path + ".temp"
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Guardar sin los metadatos de firma
    with open(temp_pdf, "wb") as f:
        writer.write(f)

    # Calcular el hash del documento original
    hash_documento = obtener_hash_pdf(temp_pdf)

    # Eliminar el archivo temporal
    os.remove(temp_pdf)

    # Cargar clave pública
    with open(clave_publica_path, 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Verificar firma
    try:
        pkcs1_15.new(public_key).verify(hash_documento, firma)
        return True, "La firma es válida"
    except (ValueError, TypeError):
        return False, "La firma no es válida"