import tkinter as tk
from pathlib import Path

root = tk.Tk()
root.title("Futbol 11 zahir")
root.geometry("450x580")
root.resizable(False, False)

imagenes = {}
posicion_jugador = []

class Arrastre:
    def __init__(self):
        self.root = root
        self.jugador_seleccionado = None


    def iniciar_arrastre(self, event):
        self.jugador_seleccionado = event.widget
        self.x_original = self.jugador_seleccionado.winfo_x()
        self.y_original = self.jugador_seleccionado.winfo_y()
        self.jugador_seleccionado.lift()

    def hacer_arrastre(self, event):
        nuevo_x = self.root.winfo_pointerx() - self.root.winfo_rootx() - 25
        nuevo_y = self.root.winfo_pointery() - self.root.winfo_rooty() - 53
        self.jugador_seleccionado.place(x=nuevo_x, y=nuevo_y)

    def finalizar_arrastre(self, event):
        x_final = self.jugador_seleccionado.winfo_x()
        y_final = self.jugador_seleccionado.winfo_y()
        intercambiado = False

        for j in posicion_jugador:
            if j == self.jugador_seleccionado:
                continue
            
            # Si soltamos el jugador encima de otro (colisión simple)
            jx = j.winfo_x()
            jy = j.winfo_y()
            
            if (abs(x_final - jx) < 50 and abs(y_final - jy) < 53):
                # Intercambiamos coordenadas
                j.place(x=self.x_original, y=self.y_original)
                self.jugador_seleccionado.place(x=jx, y=jy)
                intercambiado = True
                break
        
        # Si no se soltó sobre nadie, vuelve a su lugar original
        if not intercambiado:
            self.jugador_seleccionado.place(x=self.x_original, y=self.y_original)

cords_iniciales = [
    (200, 480), # Portero (Centrado abajo)
    # Defensas (Línea de 4)
    (45, 380), (135, 400), (270, 400), (360, 380),
    # Mediocampistas (Línea de 4)
    (45, 220), (135, 240), (270, 240), (360, 220),
    # Delanteros (Línea de 2)
    (135, 60), (270, 60)
]

folder = Path(__file__).parent
path_pj = folder / "assets" / "camiseta.png"
path_cancha = folder / "assets" / "cancha.png"

try:
    imagenes["cancha"] = tk.PhotoImage(file=path_cancha)
    imagenes["jugador"] = tk.PhotoImage(file=path_pj)
except Exception:
    pass

fondo = tk.Label(root, image=imagenes["cancha"])
fondo.place(x=0, y=0, relheight=1, relwidth=1)

for i, (x,y) in enumerate(cords_iniciales):
    pj = tk.Canvas(root, width=50, height=56, bg="#267A4C")
    pj.place(x=x, y=y)
    pj.create_image(25, 28, image=imagenes["jugador"])

    numero= 1 if i == 0 else i+1

    pj.create_text(25, 28, text=str(numero), fill="black", font=("Arial", 18, "bold"))

    posicion_jugador.append(pj)
    manejador = Arrastre()

    pj.bind("<Button-1>", manejador.iniciar_arrastre)
    pj.bind("<B1-Motion>", manejador.hacer_arrastre)
    pj.bind("<ButtonRelease-1>", manejador.finalizar_arrastre)

root.mainloop()