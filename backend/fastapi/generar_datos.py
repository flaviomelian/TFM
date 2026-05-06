import pandas as pd
import random

# Definimos patrones lógicos por categoría
data = {
    "Refund request": [
        "I want my money back for the broken laptop", "Requesting a full refund for order 123",
        "The product arrived damaged, return my payment", "I am not happy with the purchase, refund please",
        "Chargeback requested for the double billing", "Give me a refund, the item never arrived",
        "The quality is poor, I want to return it for cash", "I was overcharged and I want the difference back",
        "The item is not as described, process a refund", "Money back guarantee was promised, I want it now",
        "The package was empty, I need a total refund", "Accidental purchase, please revert the transaction",
        "The subscription renewed without my consent, refund me", "Applying for a reimbursement of the shipping costs",
        "Where is my refund? It's been two weeks", "I received the wrong item and I want my money back",
        "The service was never provided, give me a refund", "I found it cheaper elsewhere, can I return this?",
        "Product stopped working after one day, I want a refund", "The box was torn and the product smashed, refund me",
        "I am cancelling within the 14-day cooling-off period", "My bank advised me to request a refund for this",
        "Total disappointment, I demand a full reimbursement", "Please credit the amount back to my original payment method",
        "The software license didn't work, I want a refund", "Is it possible to get my money back for this?",
        "I need a refund because the delivery was 3 weeks late", "The shoes don't fit, I want a full refund",
        "Unsatisfied customer here, how do I get my money back?", "I want to return this and get my cash back"
    ],
    "Technical issue": [
        "The software keeps crashing on Windows 11", "I cannot login to my account, password error",
        "The blue screen appears every time I open the app", "Wi-Fi connection is dropping constantly",
        "Error code 500 when trying to upload a file", "The screen is flickering and showing lines",
        "The application is freezing during the startup", "I can't hear any audio during the video call",
        "The driver installation failed with an unknown error", "My database connection is timed out",
        "The mobile app is stuck on the loading screen", "Keyboard is not responding to any input",
        "I am getting a 404 error on the dashboard", "The update won't install no matter what I try",
        "The battery is overheating when I use the software", "I lost my data after the last system update",
        "Synchronisation is not working between my devices", "The printer is not recognized by the computer",
        "Touchpad stopped working after the sleep mode", "Memory leak detected, the app uses too much RAM",
        "I cannot export my project to PDF format", "The server is down and I cannot access my files",
        "Plugin conflict is breaking the website layout", "The camera lens won't focus automatically",
        "My account is locked due to too many login attempts", "Slow performance after the latest security patch",
        "Graphics card is showing artifacts in the game", "Microphone level is too low for others to hear",
        "Hard drive is making a clicking noise", "The VPN connection keeps disconnecting every 5 minutes"
    ],
    "Cancellation request": [
        "Cancel my monthly subscription immediately", "I want to close my account and stop billing",
        "Stop my premium plan, I don't use it anymore", "Unsubscribe me from the yearly service",
        "Please terminate my contract with you", "Delete my profile and cancel the order",
        "I want to opt-out of the automatic renewal", "How do I deactivate my membership?",
        "The service is too expensive, cancel my plan", "I am switching to a competitor, stop my service",
        "I don't need this tool anymore, please cancel", "Remove my credit card and close the account",
        "Stop sending me invoices, I am cancelling", "I wish to end my trial before the charge",
        "Is there a way to stop my subscription online?", "Cancel my membership but keep my data for now",
        "I am moving abroad and need to cancel the service", "The free trial is over, do not charge me",
        "I want to downgrade to the free version and cancel pro", "Please stop the recurring payment for my account",
        "I am unhappy with the new terms, I want to cancel", "Close my business account effective today",
        "I mistakenly signed up, cancel it immediately", "End my subscription at the end of the current cycle",
        "Put an end to my membership right now", "I can't find the cancel button in my settings",
        "Disable the auto-pay and terminate the service", "I want to quit using this platform forever",
        "No longer interested in the service, please unsubscribe", "Confirm the cancellation of my account via email"
    ],
    "Product inquiry": [
        "Does this camera support 4K video recording?", "Is the jacket available in size XL and blue?",
        "What is the battery life of this smartphone?", "Does it come with a warranty?",
        "I want to know more about the technical specs", "Can I use this device in Europe?",
        "What are the dimensions of the dining table?", "Does the laptop have an international keyboard?",
        "Is this compatible with Apple HomeKit?", "How many ports does the USB hub have?",
        "What materials are used in this sofa?", "Does it require professional installation?",
        "Are the headphones water-resistant?", "Can I expand the storage with a micro SD card?",
        "What is the maximum weight capacity of the chair?", "Is there a discount for bulk orders?",
        "When will the black version be back in stock?", "Does the software support Linux OS?",
        "Is the power supply included in the box?", "How long is the charging cable?",
        "Do you offer student discounts on this item?", "Can this be integrated with Slack?",
        "What is the difference between the pro and air model?", "Are there any hidden fees with this product?",
        "Does it come in an eco-friendly packaging?", "Can I try the software before I buy it?",
        "Is this item suitable for outdoor use?", "What is the brightness level in nits?",
        "Does it support fast charging technology?", "Where is this product manufactured?"
    ],
    "Billing inquiry": [
        "Why was I charged twice this month?", "I don't recognize this transaction on my card",
        "Send me the invoice for my last purchase", "Update my credit card information",
        "My discount code was not applied to the price", "I need to change my billing address",
        "I was charged for a service I already cancelled", "Why is there a tax added to my total?",
        "Is there a way to pay via PayPal instead?", "My payment was declined but the money is gone",
        "I need a breakdown of the charges on my receipt", "When is my next billing date?",
        "Can I get a VAT invoice for my company?", "There is a mistake in my monthly statement",
        "Why did the price increase without notice?", "I want to change my payment method to wire transfer",
        "How can I download all my past invoices?", "Explain this hidden fee on my account",
        "My bank says the payment is pending for days", "Is there a late fee for delayed payments?",
        "I was promised a credit that is not showing up", "Do you accept cryptocurrency for payment?",
        "The currency on my bill is wrong", "Why was I charged a foreign transaction fee?",
        "I need to split the bill between two cards", "Where can I find my billing history?",
        "The promotion I used has expired, why?", "I want to renew my plan manually, not auto",
        "There is a discrepancy in the total amount", "Can I pay for the whole year in advance?"
    ],
    "Solicitud de reembolso": [
        "Quiero que me devuelvan el dinero por el portátil roto", "Solicito un reembolso completo para el pedido 123",
        "El producto llegó dañado, devuélvanme mi pago", "No estoy contento con la compra, reembolso por favor",
        "Solicitud de devolución por cargo doble", "Denme un reembolso, el artículo nunca llegó",
        "La calidad es mala, quiero devolverlo y recuperar mi dinero", "Me cobraron de más y quiero la diferencia de vuelta",
        "El artículo no es como se describía, procesen un reembolso", "Prometieron garantía de devolución, la quiero ahora",
        "El paquete estaba vacío, necesito un reembolso total", "Compra accidental, por favor reviertan la transacción",
        "La suscripción se renovó sin mi consentimiento, devuélvanme el dinero", "Solicito el reembolso de los gastos de envío",
        "¿Dónde está mi reembolso? Han pasado dos semanas", "Recibí el artículo equivocado y quiero mi dinero de vuelta",
        "El servicio nunca se prestó, denme un reembolso", "Lo encontré más barato en otro lugar, ¿puedo devolverlo?",
        "El producto dejó de funcionar después de un día, quiero un reembolso", "La caja estaba rota y el producto aplastado, reembolso",
        "Voy a cancelar dentro del periodo de desistimiento de 14 días", "Mi banco me aconsejó solicitar un reembolso por esto",
        "Decepción total, exijo un reembolso completo", "Por favor, abonen el importe en mi método de pago original",
        "La licencia de software no funcionó, quiero un reembolso", "¿Es posible recuperar mi dinero por esto?",
        "Necesito un reembolso porque la entrega se retrasó 3 semanas", "Los zapatos no me quedan, quiero un reembolso completo",
        "Cliente insatisfecho, ¿cómo recupero mi dinero?", "Quiero devolver esto y recuperar mi efectivo"
    ],
    "Problema técnico": [
        "El software sigue fallando en Windows 11", "No puedo iniciar sesión en mi cuenta, error de contraseña",
        "La pantalla azul aparece cada vez que abro la aplicación", "La conexión Wi-Fi se corta constantemente",
        "Código de error 500 al intentar subir un archivo", "La pantalla parpadea y muestra líneas",
        "La aplicación se congela durante el inicio", "No puedo escuchar audio durante la videollamada",
        "La instalación del controlador falló con un error desconocido", "Mi conexión a la base de datos ha expirado",
        "La aplicación móvil se queda bloqueada en la pantalla de carga", "El teclado no responde a ninguna entrada",
        "Me sale un error 404 en el panel de control", "La actualización no se instala por mucho que lo intente",
        "La batería se sobrecalienta cuando uso el software", "Perdí mis datos después de la última actualización del sistema",
        "La sincronización no funciona entre mis dispositivos", "El ordenador no reconoce la impresora",
        "El panel táctil dejó de funcionar después del modo suspensión", "Fuga de memoria detectada, la app usa demasiada RAM",
        "No puedo exportar mi proyecto a formato PDF", "El servidor está caído y no puedo acceder a mis archivos",
        "Un conflicto de plugins está rompiendo el diseño web", "La lente de la cámara no enfoca automáticamente",
        "Mi cuenta está bloqueada por demasiados intentos de inicio de sesión", "Rendimiento lento tras el último parche de seguridad",
        "La tarjeta gráfica muestra artefactos en el juego", "El nivel del micrófono es demasiado bajo",
        "El disco duro hace un ruido de clic", "La conexión VPN se desconecta cada 5 minutos"
    ],
    "Solicitud de cancelación": [
        "Cancelar mi suscripción mensual inmediatamente", "Quiero cerrar mi cuenta y dejar de pagar",
        "Detengan mi plan premium, ya no lo uso", "Darme de baja del servicio anual",
        "Por favor, rescindan mi contrato con ustedes", "Eliminar mi perfil y cancelar el pedido",
        "Quiero desactivar la renovación automática", "¿Cómo desactivo mi membresía?",
        "El servicio es demasiado caro, cancelen mi plan", "Me cambio a la competencia, detengan mi servicio",
        "Ya no necesito esta herramienta, por favor cancelen", "Eliminen mi tarjeta de crédito y cierren la cuenta",
        "Dejen de enviarme facturas, voy a cancelar", "Deseo finalizar mi prueba antes del cargo",
        "¿Hay alguna forma de cancelar mi suscripción online?", "Cancelar mi suscripción pero mantener mis datos por ahora",
        "Me mudo al extranjero y necesito cancelar el servicio", "La prueba gratuita ha terminado, no me cobren",
        "Quiero bajar a la versión gratuita y cancelar el pro", "Por favor, detengan el pago recurrente de mi cuenta",
        "No estoy conforme con los nuevos términos, quiero cancelar", "Cerrar mi cuenta de empresa a partir de hoy",
        "Me registré por error, cancelen inmediatamente", "Finalizar mi suscripción al terminar el ciclo actual",
        "Poner fin a mi membresía ahora mismo", "No encuentro el botón de cancelar en mis ajustes",
        "Desactivar el pago automático y terminar el servicio", "Quiero dejar de usar esta plataforma para siempre",
        "Ya no me interesa el servicio, por favor denme de baja", "Confirmar la cancelación de mi cuenta por correo"
    ],
    "Consulta de producto": [
        "¿Esta cámara soporta grabación de video en 4K?", "¿Está la chaqueta disponible en talla XL y azul?",
        "¿Cuál es la duración de la batería de este smartphone?", "¿Viene con garantía?",
        "Quiero saber más sobre las especificaciones técnicas", "¿Puedo usar este dispositivo en Europa?",
        "¿Cuáles son las dimensiones de la mesa de comedor?", "¿Tiene el portátil teclado internacional?",
        "¿Es compatible con Apple HomeKit?", "¿Cuántos puertos tiene el concentrador USB?",
        "¿Qué materiales se utilizan en este sofá?", "¿Requiere instalación profesional?",
        "¿Son los auriculares resistentes al agua?", "¿Puedo ampliar el almacenamiento con una tarjeta micro SD?",
        "¿Cuál es la capacidad máxima de peso de la silla?", "¿Hay descuento por pedidos al por mayor?",
        "¿Cuándo volverá a estar disponible la versión en negro?", "¿El software es compatible con Linux?",
        "¿Está incluida la fuente de alimentación en la caja?", "¿Cuánto mide el cable de carga?",
        "¿Ofrecen descuentos para estudiantes en este artículo?", "¿Puede integrarse esto con Slack?",
        "¿Cuál es la diferencia entre el modelo pro y el air?", "¿Hay cargos ocultos con este producto?",
        "¿Viene en un embalaje ecológico?", "¿Puedo probar el software antes de comprarlo?",
        "¿Es este artículo adecuado para uso en exteriores?", "¿Cuál es el nivel de brillo en nits?",
        "¿Soporta tecnología de carga rápida?", "¿Dónde se fabrica este producto?"
    ],
    "Consulta de facturación": [
        "¿Por qué me han cobrado dos veces este mes?", "No reconozco esta transacción en mi tarjeta",
        "Envíenme la factura de mi última compra", "Actualizar mi información de tarjeta de crédito",
        "Mi código de descuento no se aplicó al precio", "Necesito cambiar mi dirección de facturación",
        "Me cobraron por un servicio que ya cancelé", "¿Por qué hay un impuesto añadido a mi total?",
        "¿Hay alguna forma de pagar por PayPal en su lugar?", "Mi pago fue rechazado pero el dinero se ha ido",
        "Necesito un desglose de los cargos en mi recibo", "¿Cuándo es mi próxima fecha de facturación?",
        "¿Puedo obtener una factura con IVA para mi empresa?", "Hay un error en mi estado de cuenta mensual",
        "¿Por qué aumentó el precio sin previo aviso?", "Quiero cambiar mi método de pago a transferencia",
        "¿Cómo puedo descargar todas mis facturas pasadas?", "Expliquen este cargo oculto en mi cuenta",
        "Mi banco dice que el pago está pendiente por días", "¿Hay algún recargo por pagos atrasados?",
        "Me prometieron un crédito que no aparece", "¿Aceptan criptomonedas para el pago?",
        "La moneda en mi factura es incorrecta", "¿Por qué se me cobró una comisión por transacción extranjera?",
        "Necesito dividir la factura entre dos tarjetas", "¿Dónde puedo encontrar mi historial de facturación?",
        "La promoción que usé ha caducado, ¿por qué?", "Quiero renovar mi plan manualmente, no automático",
        "Hay una discrepancia en el importe total", "¿Puedo pagar todo el año por adelantado?"
    ]
}

#Mapeo de categorias a etiquetas numéricas
category_mapping = {
    "Refund request": 0, "Solicitud de reembolso": 0,
    "Technical issue": 1, "Problema técnico": 1,
    "Cancellation request": 2, "Solicitud de cancelación": 2,
    "Product inquiry": 3, "Consulta de producto": 3,
    "Billing inquiry": 4, "Consulta de facturación": 4
}

rows = []
def inject_noise(text):
    words = text.split()
    if len(words) > 3:
        # 1. Eliminar una palabra al azar (simula saltos de escritura)
        if random.random() < 0.2:
            words.pop(random.randint(0, len(words)-1))
        
        # 2. Intercambiar dos palabras (simula errores de sintaxis)
        if random.random() < 0.1:
            idx = random.randint(0, len(words)-2)
            words[idx], words[idx+1] = words[idx+1], words[idx]
            
    # 3. Simular un "typo" (error de dedo)
    text = " ".join(words)
    if random.random() < 0.2:
        chars = list(text)
        idx = random.randint(0, len(chars)-1)
        chars[idx] = random.choice('abcdefghijklmnopqrstuvwxyz')
        text = "".join(chars)
        
    return text

rows = []
for category_name, phrases in data.items():
    label_id = category_mapping[category_name]
    for _ in range(1000):
        original_phrase = random.choice(phrases)
        # Aplicamos ruido a la mayoría de las muestras
        final_phrase = inject_noise(original_phrase) if random.random() > 0.3 else original_phrase
        rows.append({"full_text": final_phrase, "category_label": label_id})

df_new = pd.DataFrame(rows)
df_new = df_new.sample(frac=1).reset_index(drop=True)
df_new.to_csv('dataset/cleaned_data.csv', index=False)
print("¡Dataset con RUIDO generado! Ahora el modelo tendrá que trabajar.")
