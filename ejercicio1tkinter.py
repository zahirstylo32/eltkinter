import tkinter as tk
from tkinter import messagebox

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("300x400")

# Variable para guardar lo que se escribe
entrada = tk.StringVar()

# Función para agregar valores a la pantalla
def presionar(valor):
    entrada.set(entrada.get() + str(valor))

# Función para limpiar la pantalla
def limpiar():
    entrada.set("")

# Función para calcular el resultado
def calcular():
    try:
        resultado = eval(entrada.get())
        entrada.set(resultado)
    except ZeroDivisionError:
        messagebox.showerror("Error", "No se puede dividir por cero")
    except:
        messagebox.showerror("Error", "Entrada inválida")

# Pantalla de la calculadora
pantalla = tk.Entry(ventana, textvariable=entrada, font=("Arial", 20), bd=10, relief="ridge", justify="right")
pantalla.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

# Frame para los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack()

# Botones
botones = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '=', '+'),
]

# Crear botones con bucles
for fila in botones:
    fila_frame = tk.Frame(frame_botones)
    fila_frame.pack(expand=True, fill="both")
    
    for boton in fila:
        if boton == "=":
            accion = calcular
        else:
            accion = lambda x=boton: presionar(x)
        
        tk.Button(fila_frame, text=boton, font=("Arial", 15), command=accion).pack(side="left", expand=True, fill="both")

# Botón limpiar
tk.Button(ventana, text="C", font=("Arial", 15), command=limpiar).pack(fill="both")

# Ejecutar la ventana
ventana.mainloop()