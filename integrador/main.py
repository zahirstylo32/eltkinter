import tkinter as tk
from tkinter import ttk, messagebox
import json, os

root = tk.Tk()
root.title("gestion de inventario zahir")
root.geometry("1000x500")
root.resizable(False, False)

class Inventario():
    def __init__(self):
        self.root = root
        self.inventario = "inventario.json"
        self.productos = self.cargar_datos()
        self.root = root

        self.panel_operaciones = ttk.LabelFrame(root, text="Panel de Operaciones", padding=10)
        self.panel_operaciones.pack(side="left", fill="y", padx=10, pady=10)

        self.panel_tabla = ttk.LabelFrame(root, text="Existencias", padding=10)
        self.panel_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree = self.crear_tabla()
        self.crear_formulario()

    def cargar_datos(self):
        if os.path.exists(self.inventario):
            with open(self.inventario) as f:
                return json.load(f)
        return []

    def guardar_datos(self):
        with open(self.inventario, "w") as f:
            json.dump(self.productos, f, indent=4)

    def crear_formulario(self):
        campos = ["Codigo", "Descripcion", "Precio", "Categoria"]
        self.entries = {}
        for i, campo in enumerate(campos):
            ttk.Label(self.panel_operaciones, text=f"{campo}"). grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.panel_operaciones)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[campo] = entry
        
        ttk.Label(self.panel_operaciones, text="Cantidad: ").grid(row=4, column=0, sticky="w", pady=5)
        self.spin_cantidad = ttk.Spinbox(self.panel_operaciones, from_=0, to=9999)
        self.spin_cantidad.grid(row=4, column=1, pady=5)

        btn_frame = ttk.Frame(self.panel_operaciones)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Guardar", command=self.crear_prodcuto).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Modificar", command=self.actualizar_producto).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Borrar", command=self.borrar_productos).pack(side="left", padx=2)

    def crear_tabla(self):
        columnas = ("cod", "desc", "pre", "cat", "cant")
        tree = ttk.Treeview(self.panel_tabla, columns=columnas, show="headings")

        tree.heading("cod", text="Código")
        tree.heading("desc", text="Descripción")
        tree.heading("pre", text="Precio $")
        tree.heading("cat", text="Categoría")
        tree.heading("cant", text="Stock")

        scrolly = ttk.Scrollbar(self.panel_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrolly.set)

        tree.pack(side="left", fill="both", expand=True)
        scrolly.pack(side="right", fill="y")

        tree.bind("<ButtonRelease-1>", self.leer_seleccion)

        tree.tag_configure("stock_bajo", background="#fd7070")

        return tree

    def refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for p in self.productos:
            tag = "stock_bajo" if int(p["cant"]) < 5 else ""
            self.tree.insert("", "end", values=(p["cod"], p["desc"], p["pre"], p["cat"], p["cant"]), tags=(tag,))
        
    def crear_prodcuto(self):
        cod = self.entries["Codigo"].get()
        desc = self.entries["Descripcion"].get()
        pre= self.entries["Precio"].get()
        cat = self.entries["Categoria"].get()
        cant = self.spin_cantidad.get()

        if not (cod and desc and pre):
            messagebox.showwarning("Atencion!", "Llene los campos obligatorios")
            return
        if any(p["cod"] == cod for p in self.productos):
            messagebox.showerror("Error", "Este producto ya a sido subido")
            return

        nuevo_p = {"cod":cod, "desc":desc, "pre":pre, "cat":cat, "cant":cant}
        self.productos.append(nuevo_p)
        self.finalizar_operacion()

    def leer_seleccion(self, event=None):
        item_id = self.tree.selection()
        if not item_id: return

        valores = self.tree.item(item_id)["values"]

        self.entries["Codigo"].delete(0, "end")
        self.entries["Codigo"].insert(0, valores[0])
        self.entries["Descripcion"].delete(0, "end")
        self.entries["Descripcion"].insert(0, valores[1])
        self.entries["Precio"].delete(0, "end")
        self.entries["Precio"].insert(0, valores[2])
        self.entries["Categoria"].delete(0, "end")
        self.entries["Categoria"].insert(0, valores[3])
        self.spin_cantidad.set(valores[4])
    
    def actualizar_producto(self):
        cod = self.entries["Codigo"].get()
        for p in self.productos:
            if p['cod'] == cod:
                p['desc'] = self.entries["Descripcion"].get()
                p['pre'] = self.entries["Precio"].get()
                p['cat'] = self.entries["Categoria"].get()
                p['cant'] = self.spin_cantidad.get()
                self.finalizar_operacion()
                return
        messagebox.showerror("Error", "No se encontro el producto a modificar")

    def borrar_productos(self):
        cod = self.entries["Codigo"].get()
        for i in range(len(self.productos)):
            if self.productos[i]["cod"] == cod:
                del self.productos[i]
                self.finalizar_operacion()
                return
        messagebox.showerror("Error", "Producto no encontrado")

    def finalizar_operacion(self):
        self.guardar_datos()
        self.refrescar_tabla()
        for i in self.entries.values(): i.delete(0,"end")
        self.spin_cantidad.set(0)


if __name__ == "__main__":
    app = Inventario()
    root.mainloop()