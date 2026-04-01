from PIL import Image

try:
    img = Image.open(r"C:\Users\autom\Music\Nueva carpeta\gato negro\gato\reposa\frame 1.png")
    # Convert image if needed
    img = img.convert("RGBA")
    
    # Resize and save as ICO
    img.save(r"C:\Users\autom\.gemini\antigravity\scratch\gato_icon.ico", format="ICO", sizes=[(256, 256)])
    print("El archivo gato_icon.ico ha sido generado exitosamente.")
except Exception as e:
    print(f"Error generando el icono: {e}")
