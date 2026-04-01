# Súper Mascota Virtual (Gato Noir) 🐈‍⬛

¡Bienvenido al proyecto de tu nueva mascota de escritorio virtual! Este código te permite tener un gatito negro paseándose y descansando directamente en la parte inferior de tu pantalla mientras trabajas.

## Características

* **Animaciones suaves:** El gato camina hacia la izquierda, derecha, te sigue y hasta toma pequeñas pausas para descansar y respirar.
* **Sigue tu ratón:** Puedes activar el modo **"🎯 Seguir al ratón"** desde el menú contextual y él irá directamente hacia ti.
* **Totalmente independiente:** Se ejecuta por encima de todas las ventanas para que siempre lo tengas a la vista y puedas cuidarlo.
* **Icono en Sistema:** Administra tus gatos desde la esquina inferior derecha de la pantalla en Windows (el *System Tray*).
* **¡Puedes clonarlo!:** ¿Un gato no es suficiente? Créale amiguitos al instante y llena tu pantalla.

## Requisitos 📥

Para correr el código fuente por tu cuenta necesitas tener **Python 3.x** instalado. Luego, debes instalar la librería `PyQt5`.

Abre tu terminal y ejecuta:
```bash
pip install PyQt5
```

## ¿Cómo jugar con el gato? 🪄

1. Clona el repositorio:
   ```bash
   git clone https://github.com/BrandonArAf/mascota-virtual-gato.git
   ```
2. Entra a la carpeta:
   ```bash
   cd mascota-virtual-gato
   ```
3. Ejecútalo con Python:
   ```bash
   python gato_virtual_main.py
   ```

## Crea tu propio '.exe' (Ejecutable)

Si deseas compartir el gato negro con tus amigos sin que tengan que instalar Python, puedes empaquetarlo con `PyInstaller`:

1. Instala PyInstaller: 
   ```bash
   pip install pyinstaller
   ```
2. Corre el script de creación (*asegúrate de correr el script del ícono antes si lo modificaste*):
   ```bash
   python -m PyInstaller --noconsole --windowed --icon="gato_icon.ico" --add-data "frames/reposa;frames/reposa" --add-data "frames/camina;frames/camina" gato_virtual_main.py
   ```

El resultado final, tu gatito empaquetado y portátil, aparecerá en la carpeta `dist`.

---
¡Diviértete con tu nueva mascota! Desarrollado con ❤️ para Brandon.
