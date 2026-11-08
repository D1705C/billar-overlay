from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from geometria import trayectoria, COLORES

if platform == 'android':
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Settings = autoclass('android.provider.Settings')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')
    LP = autoclass('android.view.WindowManager$LayoutParams')
    PixelFormat = autoclass('android.graphics.PixelFormat')
    Gravity = autoclass('android.view.Gravity')
    Color = autoclass('android.graphics.Color')
    OverlayView = autoclass('org.diego.billar.OverlayView')

    class ToqueListener(PythonJavaClass):
        __javainterfaces__ = ['org/diego/billar/OverlayView$Listener']
        __javacontext__ = 'app'

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method('(FF)V')
        def onToque(self, x, y):
            self.callback(x, y)
else:
    def run_on_ui_thread(f):
        return f


class Panel(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kw)
        self.add_widget(Label(text='Trayectorias de billar (proyecto educativo)'))
        for texto, fn in [('Iniciar overlay', self.iniciar),
                          ('Modo marcar / pasar', self.alternar),
                          ('Ocultar / mostrar lineas', self.ocultar),
                          ('Borrar', self.borrar)]:
            self.add_widget(Button(text=texto, on_release=lambda _, f=fn: f()))
        self.puntos = []
        self.view = None
        self.marcando = True
        self.lineas_visibles = True

    def tiene_permiso(self):
        return Settings.canDrawOverlays(PythonActivity.mActivity)

    def pedir_permiso(self):
        i = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                   Uri.parse('package:' + PythonActivity.mActivity.getPackageName()))
        PythonActivity.mActivity.startActivity(i)

    def iniciar(self):
        if platform != 'android':
            return
        if not self.tiene_permiso():
            self.pedir_permiso()
            return
        self._crear_overlay()

    @run_on_ui_thread
    def _crear_overlay(self):
        act = PythonActivity.mActivity
        wm = act.getSystemService(Context.WINDOW_SERVICE)
        self.wm = wm
        self.view = OverlayView(act)
        self.listener = ToqueListener(self.on_toque)
        self.view.setListener(self.listener)
        self.params = LP(
            LP.MATCH_PARENT, LP.MATCH_PARENT,
            LP.TYPE_APPLICATION_OVERLAY,
            LP.FLAG_NOT_FOCUSABLE | LP.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT)
        self.params.gravity = Gravity.TOP | Gravity.LEFT
        wm.addView(self.view, self.params)

    @run_on_ui_thread
    def _aplicar_flags(self):
        flags = LP.FLAG_NOT_FOCUSABLE | LP.FLAG_LAYOUT_IN_SCREEN
        if not self.marcando:
            flags |= LP.FLAG_NOT_TOUCHABLE
        self.params.flags = flags
        self.wm.updateViewLayout(self.view, self.params)

    def alternar(self):
        if self.view is None:
            return
        self.marcando = not self.marcando
        self._aplicar_flags()

    def on_toque(self, x, y):
        if len(self.puntos) >= 2:
            self.puntos = []
        self.puntos.append((x, y))
        if len(self.puntos) == 2:
            self.dibujar()

    def dibujar(self):
        m = PythonActivity.mActivity.getResources().getDisplayMetrics()
        rect = (m.widthPixels * 0.05, m.heightPixels * 0.15,
                m.widthPixels * 0.95, m.heightPixels * 0.85)
        segs = trayectoria(self.puntos[0], self.puntos[1], rect, rebotes=5)
        flat, cols = [], []
        for i, ((x1, y1), (x2, y2)) in enumerate(segs):
            flat += [x1, y1, x2, y2]
            r, g, b, a = COLORES[i % len(COLORES)]
            cols.append(Color.argb(255, int(r * 255), int(g * 255), int(b * 255)))
        self.view.setLines(flat, cols)

    def ocultar(self):
        self.lineas_visibles = not self.lineas_visibles
        if self.view:
            self.view.setVisibleLines(self.lineas_visibles)

    def borrar(self):
        self.puntos = []
        if self.view:
            self.view.setLines([], [])


class BillarApp(App):
    def build(self):
        return Panel()


BillarApp().run()
