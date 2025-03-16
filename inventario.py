import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import openpyxl
import json

root = tk.Tk()
root.title("Control de Inventario")
root.geometry("1600x600")

productos = []
pedidos_pendientes = []
ARCHIVO_DATOS = "datos.json"

def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, "r") as archivo:
            datos = json.load(archivo)
            global productos, pedidos_pendientes
            productos = datos.get("productos", [])
            pedidos_pendientes = datos.get("pedidos_pendientes", [])
    except FileNotFoundError:
        productos = []
        pedidos_pendientes = []

def guardar_datos():
    datos = {
        "productos": productos,
        "pedidos_pendientes": pedidos_pendientes
    }
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def agregar_producto():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Producto")
    
    tk.Label(ventana_agregar, text="ID:").grid(row=0, column=0)
    id_entry = tk.Entry(ventana_agregar)
    id_entry.grid(row=0, column=1)
    
    tk.Label(ventana_agregar, text="Sección:").grid(row=1, column=0)
    seccion_entry = tk.Entry(ventana_agregar)
    seccion_entry.grid(row=1, column=1)
    
    tk.Label(ventana_agregar, text="Nombre:").grid(row=2, column=0)
    nombre_entry = tk.Entry(ventana_agregar)
    nombre_entry.grid(row=2, column=1)
    
    tk.Label(ventana_agregar, text="Cantidad:").grid(row=3, column=0)
    cantidad_entry = tk.Entry(ventana_agregar)
    cantidad_entry.grid(row=3, column=1)
    
    tk.Label(ventana_agregar, text="Observaciones:").grid(row=4, column=0)
    observaciones_entry = tk.Entry(ventana_agregar)
    observaciones_entry.grid(row=4, column=1)
    
    def guardar_producto():
        id = id_entry.get()
        seccion = seccion_entry.get()
        nombre = nombre_entry.get()
        cantidad_texto = cantidad_entry.get()
        observaciones = observaciones_entry.get()
        
        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        if id and seccion and nombre and cantidad_texto:
            productos.append({
                "ID": id,
                "Sección": seccion,
                "Nombre": nombre,
                "Cantidad": cantidad,
                "Observaciones": observaciones
            })
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            ventana_agregar.destroy()
            mostrar_productos()
            guardar_datos()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    
    tk.Button(ventana_agregar, text="Guardar", command=guardar_producto).grid(row=5, column=0, columnspan=2)

def eliminar_producto():
    seleccionado = lista_productos.selection()
    if seleccionado:
        producto_id = lista_productos.item(seleccionado, "text")
        for producto in productos:
            if producto["ID"] == producto_id:
                productos.remove(producto)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                mostrar_productos()
                guardar_datos()
                return
    else:
        messagebox.showerror("Error", "Seleccione un producto")

def editar_producto():
    seleccionado = lista_productos.selection()
    if seleccionado:
        producto_id = lista_productos.item(seleccionado, "text")
        for producto in productos:
            if producto["ID"] == producto_id:
                ventana_editar = tk.Toplevel(root)
                ventana_editar.title("Editar Producto")
                
                tk.Label(ventana_editar, text="ID:").grid(row=0, column=0)
                id_entry = tk.Entry(ventana_editar)
                id_entry.insert(0, producto["ID"])
                id_entry.grid(row=0, column=1)
                
                tk.Label(ventana_editar, text="Sección:").grid(row=1, column=0)
                seccion_entry = tk.Entry(ventana_editar)
                seccion_entry.insert(0, producto["Sección"])
                seccion_entry.grid(row=1, column=1)
                
                tk.Label(ventana_editar, text="Nombre:").grid(row=2, column=0)
                nombre_entry = tk.Entry(ventana_editar)
                nombre_entry.insert(0, producto["Nombre"])
                nombre_entry.grid(row=2, column=1)
                
                tk.Label(ventana_editar, text="Cantidad:").grid(row=3, column=0)
                cantidad_entry = tk.Entry(ventana_editar)
                cantidad_entry.insert(0, producto["Cantidad"])
                cantidad_entry.grid(row=3, column=1)
                
                tk.Label(ventana_editar, text="Observaciones:").grid(row=4, column=0)
                observaciones_entry = tk.Entry(ventana_editar)
                observaciones_entry.insert(0, producto["Observaciones"])
                observaciones_entry.grid(row=4, column=1)
                
                def guardar_cambios():
                    producto["ID"] = id_entry.get()
                    producto["Sección"] = seccion_entry.get()
                    producto["Nombre"] = nombre_entry.get()
                    producto["Cantidad"] = cantidad_entry.get()
                    producto["Observaciones"] = observaciones_entry.get()
                    messagebox.showinfo("Éxito", "Producto editado correctamente")
                    ventana_editar.destroy()
                    mostrar_productos()
                    guardar_datos()
                
                tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios).grid(row=5, column=0, columnspan=2)
                return
    else:
        messagebox.showerror("Error", "Seleccione un producto")

def sumar_stock():
    ventana_sumar = tk.Toplevel(root)
    ventana_sumar.title("Sumar Stock")
    
    tk.Label(ventana_sumar, text="ID del Producto:").grid(row=0, column=0)
    id_entry = tk.Entry(ventana_sumar)
    id_entry.grid(row=0, column=1)
    
    tk.Label(ventana_sumar, text="Cantidad a Sumar:").grid(row=1, column=0)
    cantidad_entry = tk.Entry(ventana_sumar)
    cantidad_entry.grid(row=1, column=1)
    
    def confirmar_suma():
        id = id_entry.get()
        cantidad_texto = cantidad_entry.get()
        
        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        if id and cantidad_texto:
            for producto in productos:
                if producto["ID"] == id:
                    producto["Cantidad"] = int(producto["Cantidad"]) + cantidad
                    messagebox.showinfo("Éxito", "Stock sumado correctamente")
                    ventana_sumar.destroy()
                    mostrar_productos()
                    guardar_datos()
                    return
            messagebox.showerror("Error", "Producto no encontrado")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    
    tk.Button(ventana_sumar, text="Sumar", command=confirmar_suma).grid(row=2, column=0, columnspan=2)

def restar_stock():
    ventana_restar = tk.Toplevel(root)
    ventana_restar.title("Restar Stock")
    
    tk.Label(ventana_restar, text="ID del Producto:").grid(row=0, column=0)
    id_entry = tk.Entry(ventana_restar)
    id_entry.grid(row=0, column=1)
    
    tk.Label(ventana_restar, text="Cantidad a Restar:").grid(row=1, column=0)
    cantidad_entry = tk.Entry(ventana_restar)
    cantidad_entry.grid(row=1, column=1)
    
    def confirmar_resta():
        id = id_entry.get()
        cantidad_texto = cantidad_entry.get()
        
        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        if id and cantidad_texto:
            for producto in productos:
                if producto["ID"] == id:
                    if int(producto["Cantidad"]) >= cantidad:
                        producto["Cantidad"] = int(producto["Cantidad"]) - cantidad
                        messagebox.showinfo("Éxito", "Stock restado correctamente")
                        ventana_restar.destroy()
                        mostrar_productos()
                        guardar_datos()
                    else:
                        messagebox.showerror("Error", "No hay suficiente stock")
                    return
            messagebox.showerror("Error", "Producto no encontrado")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
    
    tk.Button(ventana_restar, text="Restar", command=confirmar_resta).grid(row=2, column=0, columnspan=2)

def exportar_a_excel():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Inventario"
    
    sheet.append(["ID", "Sección", "Nombre", "Cantidad", "Observaciones"])
    
    for producto in productos:
        sheet.append([producto["ID"], producto["Sección"], producto["Nombre"], producto["Cantidad"], producto["Observaciones"]])
    
    workbook.save("inventario.xlsx")
    messagebox.showinfo("Éxito", "Inventario exportado a Excel correctamente")

def agregar_pedido_pendiente():
    ventana_pedido = tk.Toplevel(root)
    ventana_pedido.title("Agregar Pedido Pendiente")
    
    tk.Label(ventana_pedido, text="Pedido realizado por:").grid(row=0, column=0)
    realizado_por_entry = tk.Entry(ventana_pedido)
    realizado_por_entry.grid(row=0, column=1)
    
    tk.Label(ventana_pedido, text="Materiales:").grid(row=1, column=0)
    materiales_entry = tk.Entry(ventana_pedido)
    materiales_entry.grid(row=1, column=1)
    
    tk.Label(ventana_pedido, text="Fecha y hora (opcional):").grid(row=2, column=0)
    fecha_hora_entry = tk.Entry(ventana_pedido)
    fecha_hora_entry.grid(row=2, column=1)
    
    def guardar_pedido():
        realizado_por = realizado_por_entry.get()
        materiales = materiales_entry.get()
        fecha_hora = fecha_hora_entry.get() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if realizado_por and materiales:
            pedidos_pendientes.append({
                "Realizado por": realizado_por,
                "Materiales": materiales,
                "Fecha y hora": fecha_hora
            })
            messagebox.showinfo("Éxito", "Pedido agregado correctamente")
            ventana_pedido.destroy()
            mostrar_pedidos_pendientes()
            guardar_datos()
        else:
            messagebox.showerror("Error", "Los campos 'Realizado por' y 'Materiales' son obligatorios")
    
    tk.Button(ventana_pedido, text="Guardar", command=guardar_pedido).grid(row=3, column=0, columnspan=2)

def eliminar_pedido_pendiente():
    try:
        # Obtener el texto seleccionado en el widget Text
        seleccionado = lista_pedidos.get(tk.SEL_FIRST, tk.SEL_LAST)
        if seleccionado:
            # Buscar el índice del pedido seleccionado
            lineas = lista_pedidos.get("1.0", tk.END).split("\n")
            for i, linea in enumerate(lineas):
                if seleccionado.strip() in linea:
                    # Eliminar el pedido correspondiente
                    pedidos_pendientes.pop(i // 4)  # Cada pedido ocupa 4 líneas
                    messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
                    mostrar_pedidos_pendientes()
                    guardar_datos()
                    return
    except tk.TclError:
        messagebox.showerror("Error", "Seleccione un pedido")

def buscar_producto():
    nombre = entrada_busqueda.get()
    if nombre:
        resultados = [p for p in productos if nombre.lower() in p["Nombre"].lower()]
        lista_productos.delete(*lista_productos.get_children())
        for producto in resultados:
            lista_productos.insert("", "end", text=producto["ID"], values=(
                producto["ID"],  # ID
                producto["Sección"],  # Sección
                producto["Nombre"],  # Nombre
                producto["Cantidad"],  # Cantidad
                producto["Observaciones"]  # Observaciones
            ))
    else:
        mostrar_productos()

def mostrar_productos():
    lista_productos.delete(*lista_productos.get_children())
    for producto in productos:
        lista_productos.insert("", "end", text=producto["ID"], values=(
            producto["ID"],  # ID
            producto["Sección"],  # Sección
            producto["Nombre"],  # Nombre
            producto["Cantidad"],  # Cantidad
            producto["Observaciones"]  # Observaciones
        ))

def mostrar_pedidos_pendientes():
    lista_pedidos.delete(1.0, tk.END)
    for i, pedido in enumerate(pedidos_pendientes, start=1):
        lista_pedidos.insert(tk.END, f"{i}. Realizado por: {pedido['Realizado por']}\n")
        lista_pedidos.insert(tk.END, f"   Materiales: {pedido['Materiales']}\n")
        lista_pedidos.insert(tk.END, f"   Fecha y hora: {pedido['Fecha y hora']}\n\n")

def crear_interfaz():
    global lista_productos, lista_pedidos, entrada_busqueda
    
    frame_botones = tk.Frame(root)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    
    tk.Button(frame_botones, text="Agregar Producto", command=agregar_producto).pack(fill=tk.X)
    tk.Button(frame_botones, text="Eliminar Producto", command=eliminar_producto).pack(fill=tk.X)
    tk.Button(frame_botones, text="Editar Producto", command=editar_producto).pack(fill=tk.X)
    tk.Button(frame_botones, text="Sumar Stock", command=sumar_stock).pack(fill=tk.X)
    tk.Button(frame_botones, text="Restar Stock", command=restar_stock).pack(fill=tk.X)
    tk.Button(frame_botones, text="Exportar a Excel", command=exportar_a_excel).pack(fill=tk.X)
    
    frame_busqueda = tk.Frame(root)
    frame_busqueda.pack(side=tk.TOP, fill=tk.X)
    
    tk.Label(frame_busqueda, text="Buscar por Nombre:").pack(side=tk.LEFT)
    entrada_busqueda = tk.Entry(frame_busqueda)
    entrada_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(frame_busqueda, text="Buscar", command=buscar_producto).pack(side=tk.LEFT)
    
    frame_productos = tk.Frame(root)
    frame_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    columnas = ("ID", "Sección", "Nombre", "Cantidad", "Observaciones")
    lista_productos = ttk.Treeview(frame_productos, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        lista_productos.heading(col, text=col)
    lista_productos.pack(fill=tk.BOTH, expand=True)
    
    frame_pedidos = tk.Frame(root, width=800)
    frame_pedidos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    tk.Label(frame_pedidos, text="Pedidos Pendientes").pack()
    
    # Usar un Text widget para mostrar los pedidos pendientes
    scrollbar = tk.Scrollbar(frame_pedidos)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    lista_pedidos = tk.Text(frame_pedidos, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    lista_pedidos.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=lista_pedidos.yview)
    
    tk.Button(frame_pedidos, text="Agregar Pedido", command=agregar_pedido_pendiente).pack(fill=tk.X)
    tk.Button(frame_pedidos, text="Eliminar Pedido", command=eliminar_pedido_pendiente).pack(fill=tk.X)
    
    mostrar_productos()
    mostrar_pedidos_pendientes()

cargar_datos()
root.protocol("WM_DELETE_WINDOW", lambda: [guardar_datos(), root.destroy()])
crear_interfaz()
root.mainloop()