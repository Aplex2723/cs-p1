from Ej2RSA import generar_claves, firmar_documento, verificar_firma
import os

def main():
    # Comprobar si el archivo NDA.pdf existe
    if not os.path.exists("NDA.pdf"):
        print("Error: No se encontró el archivo NDA.pdf")
        print("Creando un PDF de ejemplo...")
        crear_pdf_ejemplo()

    print("=== PROCESO DE FIRMA DIGITAL DEL DOCUMENTO NDA.pdf ===")

    # 1. Generación de claves para Alice y la Autoridad Certificadora (AC)
    print("\n1. Generando claves RSA para Alice y la AC...")
    alice_private, alice_public = generar_claves("alice")
    ac_private, ac_public = generar_claves("ac")
    print("   Claves generadas correctamente.")

    # 2. Alice firma digitalmente el documento
    print("\n2. Alice firma el documento NDA.pdf...")
    firma_alice = firmar_documento("NDA.pdf", "alice_privada.pem", "NDA_firmado_por_alice.pdf")
    print(f"   Documento firmado por Alice. Firma: {firma_alice[:20]}...")

    # 3. La AC verifica la firma de Alice
    print("\n3. La AC verifica la firma de Alice...")
    es_valida, mensaje = verificar_firma("NDA_firmado_por_alice.pdf", "alice_publica.pem")

    if not es_valida:
        print(f"   Error: {mensaje}")
        return

    print("   La firma de Alice es válida.")

    # 4. La AC firma el documento
    print("\n4. La AC firma el documento...")
    firma_ac = firmar_documento("NDA_firmado_por_alice.pdf", "ac_privada.pem", "NDA_firmado_por_alice_y_ac.pdf")
    print(f"   Documento firmado por la AC. Firma: {firma_ac[:20]}...")

    # 5. Bob verifica la firma de la AC
    print("\n5. Bob verifica la firma de la AC...")
    es_valida, mensaje = verificar_firma("NDA_firmado_por_alice_y_ac.pdf", "ac_publica.pem")

    if es_valida:
        print("   La firma de la AC es válida.")
        print("\n=== PROCESO COMPLETADO CON ÉXITO ===")
        print("El documento ha sido firmado por Alice y verificado por la AC.")
        print("La AC ha firmado el documento y Bob ha verificado la firma de la AC.")
    else:
        print(f"   Error: {mensaje}")

def crear_pdf_ejemplo():
    """Crea un PDF de ejemplo para las pruebas"""
    try:
        from reportlab.pdfgen import canvas

        c = canvas.Canvas("NDA.pdf")
        c.setFont("Helvetica", 12)
        c.drawString(50, 800, "ACUERDO DE CONFIDENCIALIDAD (NDA)")
        c.drawString(50, 780, "Este es un documento de ejemplo para probar el sistema de firma digital.")
        c.drawString(50, 760, "Firmado por Alice, verificado por la AC y enviado a Bob.")
        c.save()
        print("Se ha creado un archivo NDA.pdf de ejemplo.")
    except ImportError:
        print("No se pudo crear el PDF de ejemplo. Por favor, instale reportlab o cree manualmente un archivo NDA.pdf.")
        with open("NDA.pdf", "w") as f:
            f.write("Este es un archivo PDF de ejemplo")

if __name__ == "__main__":
    main()
