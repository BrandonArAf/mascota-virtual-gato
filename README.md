# 🐾 Mascota Virtual (Gatito de Escritorio)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple)

Un divertido gatito interactivo que pasea, duerme y reacciona directamente sobre el escritorio de tu ordenador. Construido puramente en Python con la potencia gráfica de **PyQt5** para lograr una transparencia perfecta (canal alfa) sin bordes feos ni bloqueos de interfaz.

## ✨ Características Principales

* **Libre por el escritorio**: Camina automáticamente por encima de la barra de tareas y da la vuelta de forma inteligente al chocar con los bordes de tu pantalla.
* **Físicas de Gravedad**: ¡Atrápalo! Si lo arrastras con el botón izquierdo hacia la cima de tu pantalla y lo sueltas, caerá suavemente obedeciendo a la gravedad.
* **Mimos (Doble Clic)**: ¡Acarícialo! Un doble clic generará una linda animación de corazones flotantes (❤️).
* **Las siestas son importantes (Zzz)**: Si lo ignoras por más de 30 segundos, entrará en fase de sueño profundo y empezará a soltar burbujitas exhalando un tierno "Zzz...".
* **Bandeja de Sistema Inteligente (Tray Icon)**: Control total en todo momento. Puedes "esconder" al gato si necesitas trabajar súper concentrado y hacer que vuelva cuando lo necesites directamente desde el icono de la bandeja de Windows.
* **Menú Contextual Avanzado**: Haz clic derecho directamente sobre el gato para alternar su nivel de energía (Modo caminar tranquilo o Modo correr) o para cerrarlo del todo.

## 🚀 Cómo jugar (Para Desarrolladores)

1. Clona este repositorio o descarga el ZIP.
2. Instala la dependencia gráfica (PyQt5):
   ```bash
   pip install PyQt5
   ```
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```

## 📦 Exportar y Empaquetar a un (.exe)

Si quieres enviar este programa a tus amigos y que lo disfruten sin saber nada de código o terminales, se ha configurado el proyecto para empaquetarlo ágilmente con PyInstaller, incluyendo todas las imágenes de forma embebida.

1. Instala PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Ejecuta este comando exacto en la carpeta raíz del proyecto:
   ```bash
   pyinstaller --noconsole --name="MascotaVirtual" --onefile --add-data "assets;assets" main.py
   ```
3. ¡Tu archivo `.exe` estará mágicamente listo para compartir dentro de la carpeta `dist/`!

---
*Hecho para darle un poco de vida a tu escritorio mientras programas.*
