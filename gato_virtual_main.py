import sys
import os
import random
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPixmap, QCursor, QTransform, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QDesktopWidget, QSystemTrayIcon

class PetManager:
    def __init__(self, app):
        self.app = app
        self.pets = []
        self.is_hidden = False
        
        self.load_images()
        self.setup_tray()
        self.add_pet()
        
    def load_images(self):
        self.idle_frames = []
        self.idle_frames_left = []
        self.walk_frames = []
        self.walk_frames_left = []
        
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
            idle_path = os.path.join(base_dir, "frames", "reposa")
            walk_path = os.path.join(base_dir, "frames", "camina")
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            idle_path = os.path.join(base_dir, "frames", "reposa")
            walk_path = os.path.join(base_dir, "frames", "camina")
            
        transform = QTransform().scale(-1, 1)
        
        def iter_frames(path, frame_list, reverse_list, ping_pong=False):
            if not os.path.exists(path):
                print(f"Warning: Path not found {path}")
                return
                
            files = [f for f in os.listdir(path) if f.endswith('.png') and f != "frame 0.png"]
            # Sort by number in filename
            def extract_num(f):
                nums = ''.join(filter(str.isdigit, f))
                return int(nums) if nums else 0
                
            files.sort(key=extract_num)
            
            loaded_f = []
            loaded_r = []
            for file in files:
                full_path = os.path.join(path, file)
                original = QPixmap(full_path)
                if not original.isNull():
                    pixmap = original.scaledToWidth(180, Qt.SmoothTransformation)
                    loaded_f.append(pixmap)
                    loaded_r.append(pixmap.transformed(transform, Qt.SmoothTransformation))
                    
            if ping_pong and len(loaded_f) > 2:
                # Loop through frames back and forth for smoother idle animation
                loaded_f.extend(loaded_f[-2:0:-1])
                loaded_r.extend(loaded_r[-2:0:-1])
                
            frame_list.extend(loaded_f)
            reverse_list.extend(loaded_r)
                    
        iter_frames(idle_path, self.idle_frames, self.idle_frames_left, ping_pong=False)
        iter_frames(walk_path, self.walk_frames, self.walk_frames_left, ping_pong=False)
                
        if self.idle_frames:
            self.tray_icon_img = QIcon(self.idle_frames[0])
        else:
            self.tray_icon_img = QIcon()

    def setup_tray(self):
        self.tray = QSystemTrayIcon(self.tray_icon_img, self.app)
        self.tray.setToolTip("Súper Gato Virtual 🐈")
        
        menu = QMenu()
        menu.setStyleSheet("QMenu { background-color: #2b2b2b; color: white; border: 1px solid #444; font-weight: bold; padding: 5px; } QMenu::item:selected { background-color: #555; }")
        
        add_action = QAction("➕ Añadir un Gato", menu)
        add_action.triggered.connect(self.add_pet)
        
        self.toggle_action = QAction("👀 Ocultar todos", menu)
        self.toggle_action.triggered.connect(self.toggle_visibility)
        
        quit_action = QAction("👋 Despedir a Todos", menu)
        quit_action.triggered.connect(self.app.quit)
        
        menu.addAction(add_action)
        menu.addAction(self.toggle_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def add_pet(self, x=None, y=None):
        pet = VirtualPet(self)
        if x is not None and y is not None:
            pet.move(x, y)
        self.pets.append(pet)
        if not self.is_hidden:
            pet.show()
            
    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)
            pet.close()
            
    def toggle_visibility(self):
        self.is_hidden = not self.is_hidden
        self.toggle_action.setText("👀 Mostrar todos" if self.is_hidden else "👀 Ocultar todos")
        for pet in self.pets:
            if self.is_hidden:
                pet.hide()
            else:
                pet.show()

class VirtualPet(QLabel):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.current_frame = -1
        self.state = 'idle'
        self.direction = 'right'
        self.behavior = 'wander'
        
        self.screen_rect = QDesktopWidget().availableGeometry()
        
        if self.manager.idle_frames:
            self.setPixmap(self.manager.idle_frames[0])
            self.resize(self.manager.idle_frames[0].width(), self.manager.idle_frames[0].height())
            
        start_x = random.randint(0, self.screen_rect.width() - self.width())
        start_y = self.screen_rect.height() - self.height()
        self.move(start_x, start_y)
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(300) 
        
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.change_state)
        self.state_timer.start(random.randint(4000, 8000))
        
        self.dragging = False
        self.offset = QPoint()

    def update_animation(self):
        frames = []
        if self.state == 'idle':
            frames = self.manager.idle_frames if self.direction == 'right' else self.manager.idle_frames_left
            if not frames:
                return
            
            if self.current_frame < 0:
                self.current_frame = 0
            elif self.current_frame < 2:
                self.current_frame += 1
            else:
                if self.current_frame >= len(frames) - 1:
                    self.current_frame = 2
                else:
                    self.current_frame += 1
                    
            self.setPixmap(frames[self.current_frame])
        else:
            frames = self.manager.walk_frames if self.direction == 'right' else self.manager.walk_frames_left
            if not frames:
                return
                
            if self.current_frame < 0:
                self.current_frame = 0
            else:
                self.current_frame = (self.current_frame + 1) % len(frames)
                
            self.setPixmap(frames[self.current_frame])
            
        if self.dragging:
            return
            
        floor_y = self.screen_rect.height() - self.height()
        step = 5 
        new_x = self.x()
        y_pos = self.y()

        if self.state == 'walk':
            if self.behavior == 'mouse':
                target_x = QCursor.pos().x() - (self.width() // 2)
                if abs(self.x() - target_x) > step:
                    self.direction = 'right' if target_x > self.x() else 'left'
                    new_x += step if self.direction == 'right' else -step
                else:
                    self.state = 'idle'
                    
            else:
                new_x += step if self.direction == 'right' else -step
                if new_x <= 0:
                    self.direction = 'right'
                    new_x = 0
                elif new_x + self.width() >= self.screen_rect.width():
                    self.direction = 'left'
                    new_x = self.screen_rect.width() - self.width()

        gravity = 8
        if y_pos < floor_y:
            y_pos += gravity
            if y_pos > floor_y:
                y_pos = floor_y
        elif y_pos > floor_y:
            y_pos = floor_y

        self.move(new_x, y_pos)

    def change_state(self):
        if self.behavior == 'mouse' and self.state == 'walk':
            if random.random() > 0.7:
                self.state = 'idle'
                self.current_frame = -1
                self.anim_timer.setInterval(300)
            self.state_timer.start(random.randint(2000, 4000))
            return

        if self.state == 'idle':
            self.state = 'walk'
            self.current_frame = -1
            self.anim_timer.setInterval(120) 
            if random.random() > 0.4:
                self.direction = 'left' if self.direction == 'right' else 'right'
            self.state_timer.start(random.randint(3000, 6000))
        else:
            self.state = 'idle'
            self.current_frame = -1
            self.anim_timer.setInterval(300)
            self.state_timer.start(random.randint(3000, 7000))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            
        elif event.button() == Qt.RightButton:
            menu = QMenu(self)
            menu.setStyleSheet("QMenu { background-color: #2b2b2b; color: white; border: 1px solid #444; font-weight: bold; padding: 5px; } QMenu::item:selected { background-color: #555; }")
            
            mode_action = QAction("📍 Dejar de seguir al ratón", self) if self.behavior == 'mouse' else QAction("🎯 Seguir al ratón", self)
            mode_action.triggered.connect(self.toggle_mouse_follow)
            
            clone_action = QAction("👯 Crear Amigo Gatuno", self)
            clone_action.triggered.connect(lambda: self.manager.add_pet(max(0, self.x() - 100), self.y()))
            
            quit_action = QAction("👋 Despedir", self)
            quit_action.triggered.connect(lambda: self.manager.remove_pet(self))
            
            menu.addAction(mode_action)
            menu.addAction(clone_action)
            menu.addSeparator()
            menu.addAction(quit_action)
            
            menu.exec_(QCursor.pos())

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)

    def toggle_mouse_follow(self):
        if self.behavior == 'mouse':
            self.behavior = 'wander'
            self.state = 'idle'
            self.current_frame = -1
        else:
            self.behavior = 'mouse'
            self.state = 'walk'
            self.current_frame = -1

if __name__ == '__main__':
    QApplication.setQuitOnLastWindowClosed(False)
    app = QApplication(sys.argv)
    manager = PetManager(app)
    sys.exit(app.exec_())
