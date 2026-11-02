import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class UIManager:
    """
    Gestion de la paleta de colores, estilos y carga de imagenes
    mantiene la referncia a las imagenes para evitar  que se desparescan
    """
    COLOR_BG = "#121212"
    COLOR_PANEL = "#1E1E1E"
    COLOR_TEXT = "#E0E0E0"
    COLOR_ACCENT = "#00E5FF"
    COLOR_DANGER = "#FF1744"

    def __init__(self):
        self._cache_imagenes = {}

    def configurar_estilos_ttk(self, root):
        """Aplica un diseño oscuro y moderno a los widgets ttk"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Accent.TButton",
                        background = self.COLOR_ACCENT,
                        foreground = self.COLOR_BG,
                        font = ("Segoe UI", 11, "bold"),
                        borderwidth = 0
                        )
        style.configure("Accent.TButton", background = [("active", "#00B8CC")])

        style.configure("TEntry",
                        fieldbackground = self.COLOR_PANEL,
                        foreground = self.COLOR_TEXT,
                        insertcolor = self.COLOR_TEXT,
                        borderwidth = 1, relief = "flat"
                        )

    def cargar_imagen(self, ruta_relativa: str, size: tuple = None):
        """Carga una imagen desde la carpeta assets y la redimensiona"""
        ruta_abs = os.path.join(os.getcwd(), "assets", ruta_relativa)

        try:
            img = Image.open(ruta_abs).convert("RGBA")
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)

            tk_img = ImageTk.PhotoImage(img)

            self._cache_imagenes[ruta_relativa] = tk_img
            return tk_img

        except Exception as e:
            print(f"Error al cargar imagen: {ruta_abs}: {e}")
            return None
