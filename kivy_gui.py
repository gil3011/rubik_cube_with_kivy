from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, Rectangle, Mesh
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup

from cube import Cube
import time


COLOR_MAP = {
    'w': (0.85, 0.85, 0.9),     # Soft lavender white
    'r': (0.9, 0.1, 0.3),       # Raspberry red
    'b': (0.2, 0.4, 0.9),       # Electric blue
    'g': (0.1, 0.8, 0.5),       # Minty green
    'o': (1, 0.4, 0.1),         # Tangy tangerine
    'y': (0.95, 0.9, 0.3)       # Golden mustard
}
Window.size = (360, 600)

class CubeGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.move_counter = 0
        self.cube = Cube()
        self.start_time = None
        self.history = []

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Top buttons
        top = BoxLayout(size_hint_y=None, height=50, spacing=5)
        top.add_widget(Button(text='Shuffle', background_color=(0.2, 0.6, 0.9, 1), on_press=lambda _: self.shuffle()))
        self.btn_undo = Button(text='Undo', background_color=(0.8, 0.3, 0.3, 1), on_press=lambda _: self.undo())
        top.add_widget(self.btn_undo)
        top.add_widget(Button(text='Reset', background_color=(0.3, 0.8, 0.3, 1), on_press=lambda _: self.reset()))
        self.add_widget(top)
        self.btn_undo.disabled = True

        # Canvas area
        self.canvas_area = Widget(size_hint=(1, None), height=350)
        self.add_widget(self.canvas_area)

        # Face move buttons
        self.face_moves = [
            ('U',  lambda: self.cube.u()), ('U\'', lambda: self.cube.u(3)),
            ('R',  lambda: self.cube.r()), ('R\'', lambda: self.cube.r(3)),
            ('F',  lambda: self.cube.f()), ('F\'', lambda: self.cube.f(3)),
            ('L',  lambda:self.cube.l()), ('L\'', lambda: self.cube.l(3)),
            ('D',  lambda:self.cube.d()), ('D\'', lambda: self.cube.d(3)),
            ('B',  lambda:self.cube.b()), ('B\'', lambda: self.cube.b(3)),
        ]
        grid = GridLayout(cols=4, size_hint_y=None, height=160, spacing=5)
        for label, action in self.face_moves:
            grid.add_widget(Button(text=label, font_size=14, background_color=(0.3, 0.3, 0.6, 1), on_press=lambda _, a=action: self.perform_move(a, True)))
        self.add_widget(grid)

        # Rotation buttons
        rotation = BoxLayout(size_hint_y=None, height=50, spacing=5)
        for label, action in [('X',  lambda:self.cube.rotate_x()), ('Y',  lambda:self.cube.rotate_y()), ('Z',  lambda:self.cube.rotate_z())]:
            rotation.add_widget(Button(text=label, background_color=(0.6, 0.4, 0.2, 1), on_press=lambda _, a=action: self.perform_move(a)))
        self.add_widget(rotation)

        # Labels
        self.timer_label = Label(text="Time: 00:00", color=(1, 1, 1, 1), font_size=18)
        self.moves_label = Label(text="Moves: 0", color=(1, 1, 1, 1), font_size=18)
        self.add_widget(self.timer_label)
        self.add_widget(self.moves_label)
        self.canvas_area.bind(pos=lambda *_: self.draw_isometric_cube(),
                      size=lambda *_: self.draw_isometric_cube())

        self.draw_isometric_cube()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
    def ask_restart_confirmation(self, shuffle = False):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Timer is running.\nStart over?", font_size=16))
        
        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)
        yes_btn = Button(text="Yes", background_color=(0.3, 0.8, 0.3, 1))
        no_btn = Button(text="No", background_color=(0.8, 0.3, 0.3, 1))
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)

        popup = Popup(title="Confirm Shuffle", content=content, size_hint=(None, None), size=(280, 180), auto_dismiss=False)

        if shuffle:
            yes_btn.bind(on_press=lambda _: (popup.dismiss(), self.start_shuffle()))
        else:
            yes_btn.bind(on_press=lambda _: (popup.dismiss(), self.perform_reset()))
        no_btn.bind(on_press=popup.dismiss)
        popup.open()      
    def perform_move(self, action, move=False):
        action()
        if move and self.start_time is not None:
            if len(self.history) == 0 or (action, move) != self.history[-1]:
                self.move_counter += 1
                self.moves_label.text = f"Moves: {self.move_counter}"
        self.history.append((action, move))
        self.btn_undo.disabled = False


        if self.cube.is_solved() and self.start_time is not None:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            content.add_widget(Label(text=f"You solved the cube!\nTime: {minutes:02d}:{seconds:02d}\nMoves: {self.move_counter}", font_size=16))
            return_btn = Button(text="Return", background_color=(0.3, 0.8, 0.3, 1))
            content.add_widget(return_btn)
            popup = Popup(title="Solved", content=content, size_hint=(None, None), size=(280, 280), auto_dismiss=False)
            return_btn.bind(on_press=lambda _:(popup.dismiss(), self.perform_reset()))
            popup.open()     
        self.draw_isometric_cube()
    def update_timer(self, dt):
        if self.start_time is None:
            return
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        self.timer_label.text = f"Time: {minutes:02d}:{seconds:02d}"
    def undo(self):
        if len(self.history) == 0:
            return
        action, move = self.history.pop()
        action(); action(); action()
        if move and self.start_time is not None:
            self.move_counter -= 1
            self.moves_label.text = f"Moves: {self.move_counter}"
        self.draw_isometric_cube()
        if len(self.history) == 0:
            self.btn_undo.disabled = True
    def shuffle(self):
        if self.start_time is not None:
            self.ask_restart_confirmation(True)
            return
        else:
            self.start_shuffle()
    def reset(self):
        if self.start_time is not None:
            self.ask_restart_confirmation()
        else:
            self.perform_reset()
    def perform_reset(self):
        self.move_counter = 0
        self.cube = Cube()
        self.start_time = None
        self.history = []
        self.btn_undo.disabled = True
        self.timer_label.text = "Time: 00:00"
        self.moves_label.text = "Moves: 0"
        self.draw_isometric_cube()
    def start_shuffle(self):
        Clock.unschedule(self.update_timer)
        self.start_time = time.time()
        Clock.schedule_interval(self.update_timer, 0.1)
        self.move_counter = 0
        self.moves_label.text = f"Moves: {self.move_counter}"
        self.cube.shuffle()
        self.draw_isometric_cube() 
    def draw_isometric_cube(self):
        self.canvas_area.canvas.clear()

        # Dynamically calculate size and position
        size = self.canvas_area.height / 6
        dx_front = size * 0.85  # Slightly wider front
        dx_right = size * 0.75   # Slightly narrower right
        dy = -size * 0.22

        origin_x = self.canvas_area.x + self.canvas_area.width / 2 - 3 * (dx_front+dx_right)/2
        origin_y = self.canvas_area.y + self.canvas_area.height / 2 - 1.5* size

        # Top face
        for i in range(3):
            for j in range(3):
                color = COLOR_MAP[self.cube.faces['up'][i][j]]
                
                x = origin_x + j * dx_front + (2 - i) * dx_right
                y = origin_y + j * dy - (2 - i) * dy + 3 * size
                with self.canvas_area.canvas:
                    Color(*color)
                    Mesh(vertices=[
                        x, y, 0, 0,
                        x + dx_right, y - dy, 0, 0,
                        x +  dx_right +dx_front , y, 0, 0,
                        x + dx_front, y + dy, 0, 0
                    ], indices=[0, 1, 2, 0, 2, 3], mode='triangles')
                    Color(0, 0, 0)
                    Line(points=[x, y, x + dx_right, y - dy, x + dx_right + dx_front, y, x + dx_front, y + dy, x, y], width=0.3)

        # Right face
        for i in range(3):
            for j in range(3):
                color = COLOR_MAP[self.cube.faces['right'][i][j]]
                x = origin_x + j * dx_right + 3 * dx_front
                y = origin_y - j * dy + (2 - i) * size + 3 * dy

                with self.canvas_area.canvas:
                    Color(*color)
                    Mesh(vertices=[
                        x, y, 0, 0,
                        x, y + size, 0, 0,
                        x + dx_right, y - dy + size, 0, 0,
                        x + dx_right, y - dy, 0, 0
                    ], indices=[0, 1, 2, 0, 2, 3], mode='triangles')
                    Color(0, 0, 0)
                    Line(points=[x, y, x, y + size, x + dx_right, y - dy + size, x + dx_right, y - dy, x, y], width=0.3)

        # Front face
        for i in range(3):
            for j in range(3):
                color = COLOR_MAP[self.cube.faces['front'][i][j]]
                x = origin_x + j * dx_front
                y = origin_y + j * dy + (2 - i) * size

                with self.canvas_area.canvas:
                    Color(*color)
                    Mesh(vertices=[
                        x, y, 0, 0,
                        x + dx_front, y + dy, 0, 0,
                        x + dx_front, y + dy + size, 0, 0,
                        x, y + size, 0, 0
                    ], indices=[0, 1, 2, 0, 2, 3], mode='triangles')
                    Color(0, 0, 0)
                    Line(points=[x, y, x + dx_front, y + dy, x + dx_front, y + dy + size, x, y + size, x, y], width=0.3)
class CubeApp(App): 
    def build(self): 
        self.icon = 'C:\\Users\\gil30\\Desktop\\cube\\app\\rubik.ico'
        self.title = "Rubik's Cube"
        return CubeGUI() 
if __name__ == '__main__': 
    CubeApp().run()