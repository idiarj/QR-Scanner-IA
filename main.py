import cv2
from pyzbar.pyzbar import decode

# Función para validar si el QR contiene una URL válida
def validar_contenido_qr(texto):
    return texto.startswith("https://")

# Captura desde la cámara
cap = cv2.VideoCapture(0)

print("📷 Escaneando... Presiona 'q' para salir.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    qrs = decode(frame)
    for qr in qrs:
        texto = qr.data.decode('utf-8')
        puntos = qr.polygon

        # Dibuja el rectángulo
        pts = [(p.x, p.y) for p in puntos]
        if len(pts) > 4:
            pts = pts[:4]
        cv2.polylines(frame, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Texto y validación
        valido = validar_contenido_qr(texto)
        color = (0, 255, 0) if valido else (0, 0, 255)
        mensaje = f"{'VÁLIDO' if valido else 'INVÁLIDO'}: {texto}"
        cv2.putText(frame, mensaje, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        print(f"Contenido detectado: {texto}")
        print(f"¿Válido?: {'Sí' if valido else 'No'}\n")

    cv2.imshow("Escáner QR (presiona 'q' para salir)", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
