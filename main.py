import sys
import os
import random
import time
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtGui import QPixmap, QTransform, QCursor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QPoint

class FloatingLabel(QLabel):
    def __init__(self, text, color, x, y, duration_ms=2000):
        super().__init__()
        # Frameless and stays on top of everything
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setText(text)
        self.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        self.move(int(x), int(y))
        
        # Animación
        self.opacity = 1.0
        self.duration_ms = duration_ms
        self.steps = 20
        self.step_delay = self.duration_ms // self.steps
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(self.step_delay)
        
        self.show()

    def animate(self):
        # Sube lentamente
        self.move(int(self.x()), int(self.y() - 2))
        # Se desvanece
        self.opacity -= 1.0 / self.steps
        self.setWindowOpacity(max(0, self.opacity))
        if self.opacity <= 0:
            self.timer.stop()
            self.close()

class VirtualPet(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURACIÓN DE VENTANA ---
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        
        # --- ESTADOS DEL GATO ---
        self.state = 'idle'
        self.direction = 1 
        self.speed = 2 
        self.idle_pause_counter = 0 
        
        # --- INTERACCIONES Y SUEÑO ---
        self.last_interaction_time = time.time()
        
        # --- FÍSICAS ---
        self.dragging = False
        self.offset = QPoint()
        self.vy = 0 
        self.gravity = 1.5 
        
        # --- CARGAR ANIMACIONES ---
        self.idle_frames_right = []
        self.idle_frames_left = []
        self.walk_frames_right = []
        self.walk_frames_left = []
        
        # --- FUNCIÓN DE RUTAS PYINSTALLER ---
        def resource_path(relative_path):
            """ Obtiene la ruta absoluta al archivo temporal (dentro del exe) o local. """
            try:
                base_path = sys._MEIPASS # Carpeta temporal creada al ejecutar el .exe
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
            
        reposa_path = resource_path(r"assets\reposa")
        camina_path = resource_path(r"assets\camina")
        
        def load_frames(path_dir, count, target_height=180):
            frames_right = []
            frames_left = []
            transform = QTransform().scale(-1, 1)
            for i in range(1, count + 1):
                path = os.path.join(path_dir, f"frame {i}.png")
                if os.path.exists(path):
                    pixmap = QPixmap(path)
                    pixmap = pixmap.scaledToHeight(target_height, Qt.SmoothTransformation)
                    frames_right.append(pixmap)
                    frames_left.append(pixmap.transformed(transform, Qt.SmoothTransformation))
            return frames_right, frames_left

        self.idle_frames_right, self.idle_frames_left = load_frames(reposa_path, 4)
        self.walk_frames_right, self.walk_frames_left = load_frames(camina_path, 7)
        
        self.frame_index = 0
        
        if self.idle_frames_right:
            self.resize(self.idle_frames_right[0].width(), self.idle_frames_right[0].height())

        # --- POSICIÓN EN PANTALLA ---
        screen = QApplication.primaryScreen().geometry()
        self.floor_y = screen.height() - self.height() - 40 
        
        self.x = screen.width() // 2
        self.y = self.floor_y
        self.move(int(self.x), int(self.y))
        
        # --- BANDEJA DEL SISTEMA (TRAY ICON) ---
        self.tray = QSystemTrayIcon(self)
        if self.idle_frames_right:
            icon_pixmap = self.idle_frames_right[0].scaledToHeight(64, Qt.SmoothTransformation)
            self.tray.setIcon(QIcon(icon_pixmap))
            self.tray.setToolTip("Tu Gatito Virtual")
            
            tray_menu = QMenu()
            show_action = QAction("Llamar de vuelta (Mostrar)", self)
            show_action.triggered.connect(self.showNormal)
            quit_action = QAction("❌ Cerrar mascota para siempre", self)
            quit_action.triggered.connect(QApplication.quit)
            
            tray_menu.addAction(show_action)
            tray_menu.addAction(quit_action)
            self.tray.setContextMenu(tray_menu)
            self.tray.show()

        # --- RELOJ / BUCLE DE JUEGO ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pet)
        self.timer.start(150) 
        
        # UI Elementos flotantes
        self.floating_texts = []

    def reset_interaction(self):
        """Resetea el reloj de aburrimiento del gato."""
        self.last_interaction_time = time.time()

    def update_pet(self):
        current_time = time.time()
        
        # Lógica de siesta (Zzz) si han pasado > 30 segundos de inactividad
        if self.state == 'idle' and not self.dragging:
            if current_time - self.last_interaction_time > 30:
                # Spawnear un "Zzz..." esporádicamente (ej. 2% de chance para no llenarlo de texto)
                if random.randint(1, 100) <= 2:
                    bubble_x = self.x + self.width() * 0.7 if self.direction == 1 else self.x + self.width() * 0.1
                    bubble = FloatingLabel("Zzz...", "#87CEFA", bubble_x, self.y - 10, 3000)
                    self.floating_texts.append(bubble)

        # 1. Aplicar Gravedad
        if not self.dragging and self.y < self.floor_y:
            self.vy += self.gravity
            self.y += self.vy
            if self.y >= self.floor_y:
                self.y = self.floor_y
                self.vy = 0
            self.move(int(self.x), int(self.y))
            self.state = 'idle'
            
        # 2. IA / Lógica de decisión interactiva
        if not self.dragging and self.y >= self.floor_y:
            # Si el gato está dormido (sin interactuar > 30s) no se moverá por sí solo
            if current_time - self.last_interaction_time < 30: 
                if random.randint(1, 100) <= 5: 
                    if self.state == 'idle' and self.walk_frames_right:
                        self.state = 'walk'
                        self.direction = random.choice([-1, 1])
                    else:
                        self.state = 'idle'
                    self.frame_index = 0
                    self.idle_pause_counter = 0

        # 3. Animaciones
        if self.state == 'idle' and self.idle_frames_right:
            frames = self.idle_frames_right if self.direction == 1 else self.idle_frames_left
            
            if self.frame_index == 1 and self.idle_pause_counter > 0:
                self.idle_pause_counter -= 1
            else:
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.label.setPixmap(frames[self.frame_index])
                if self.frame_index == 1:
                    self.idle_pause_counter = 30 
                    
        elif self.state == 'walk' and self.walk_frames_right:
            self.reset_interaction() 
            frames = self.walk_frames_right if self.direction == 1 else self.walk_frames_left
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.label.setPixmap(frames[self.frame_index])
            
            self.x += self.speed * self.direction
            screen = QApplication.primaryScreen().geometry()
            if self.x < 0:
                self.direction = 1
                self.x = 0
            elif self.x > screen.width() - self.width():
                self.direction = -1
                self.x = screen.width() - self.width()
                
            self.move(int(self.x), int(self.y))

        # Limpiar referencias de animaciones flotantes terminadas
        self.floating_texts = [ft for ft in self.floating_texts if ft.isVisible()]

    # --- INTERACTIVIDAD CON EL RATÓN ---
    def mouseDoubleClickEvent(self, event):
        self.reset_interaction()
        if event.button() == Qt.LeftButton:
            # Generar un corazón flotante cuando le acaricias (doble clic)
            heart_x = self.x + self.width() / 2 - 15
            heart_y = self.y - 20
            heart = FloatingLabel("❤️", "#FF1493", heart_x, heart_y, 2500)
            self.floating_texts.append(heart)

    def mousePressEvent(self, event):
        self.reset_interaction()
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.state = 'idle'
            self.vy = 0
            self.offset = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)
            
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 5px 20px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        hide_action = QAction("💤 Esconder un rato", self)
        hide_action.triggered.connect(self.hide)
        
        speed_text = "🏃 Modo Correr" if self.speed == 2 else "🚶 Modo Relajado"
        speed_action = QAction(speed_text, self)
        speed_action.triggered.connect(self.toggle_speed)
        
        exit_action = QAction("❌ Despedirse", self)
        exit_action.triggered.connect(QApplication.quit) # Cierra todo permanentemente
        
        menu.addAction(hide_action)
        menu.addAction(speed_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        
        # Abrir el menú asegurando buena posición
        menu.exec_(pos)

    def toggle_speed(self):
        if self.speed == 2:
            self.speed = 8 # Acelerar
        else:
            self.speed = 2 # Normalizar

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.reset_interaction()
            new_pos = event.globalPos() - self.offset
            self.x = new_pos.x()
            self.y = new_pos.y()
            self.vy = 0 
            self.move(int(self.x), int(self.y))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Importante: Como puede quedarse escondido en la bandeja del sistema, 
    # evitamos que el programa se cierre al ocultar la ventana base.
    app.setQuitOnLastWindowClosed(False) 
    pet = VirtualPet()
    pet.show()
    sys.exit(app.exec_())
