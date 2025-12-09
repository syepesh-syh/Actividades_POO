import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date


# ============================================================
# Clase Habitacion: modela cada habitación del hotel
# ============================================================
class Habitacion:
    def __init__(self, numero: int, precio_por_dia: int):
        self.numero = numero
        self.precio_por_dia = precio_por_dia
        self.disponible = True
        self.huesped = None  # dict: {"nombre","apellidos","dni"}
        self.fecha_ingreso = None  # date object

    def ocupar(self, nombre: str, apellidos: str, dni: str, fecha_ingreso: date):
        """Ocupa la habitación con los datos del huésped."""
        self.disponible = False
        self.huesped = {"nombre": nombre, "apellidos": apellidos, "dni": dni}
        self.fecha_ingreso = fecha_ingreso

    def calcular_estancia(self, fecha_salida: date):
        """
        Calcula días y total entre fecha_ingreso (inclusive) y fecha_salida (exclusive).
        Retorna (dias, total).
        Asume que fecha_salida > fecha_ingreso.
        """
        dias = (fecha_salida - self.fecha_ingreso).days
        if dias < 1:
            dias = 1
        total = dias * self.precio_por_dia
        return dias, total

    def liberar(self):
        """Libera la habitación y devuelve los datos previos (para registro si se necesita)."""
        datos = {
            "huesped": self.huesped,
            "fecha_ingreso": self.fecha_ingreso
        } if self.huesped and self.fecha_ingreso else None
        self.disponible = True
        self.huesped = None
        self.fecha_ingreso = None
        return datos


# ============================================================
# Clase Hotel: contiene las 10 habitaciones y utilidades
# ============================================================
class Hotel:
    def __init__(self):
        self.habitaciones = []
        # Crear 10 habitaciones: 1-5 => 120000, 6-10 => 160000
        for n in range(1, 6):
            self.habitaciones.append(Habitacion(n, 120000))
        for n in range(6, 11):
            self.habitaciones.append(Habitacion(n, 160000))

    def get_habitacion(self, numero: int):
        """Obtiene la habitación por número (1..10). Devuelve None si no existe."""
        if not (1 <= numero <= 10):
            return None
        return self.habitaciones[numero - 1]


# ============================================================
# Interfaz gráfica principal (POO)
# ============================================================
class AppHotel:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel - Gestión de Habitaciones")
        self.root.geometry("600x400")
        self.hotel = Hotel()

        # Crear menú principal
        self.crear_menu()

        # Crear la sección principal "Habitaciones" (listado)
        self.crear_panel_habitaciones()

    # ----------------------------
    # Menú principal
    # ----------------------------
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú "Opciones"
        menu_op = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Opciones", menu=menu_op)
        menu_op.add_command(label="Consultar habitaciones", command=self.mostrar_habitaciones_panel)
        menu_op.add_command(label="Salida de huéspedes", command=self.abrir_ventana_solicitar_num_habitacion_salida)
        menu_op.add_separator()
        menu_op.add_command(label="Salir", command=self.root.quit)

    # ----------------------------
    # Panel principal que muestra las 10 habitaciones y su estado
    # ----------------------------
    def crear_panel_habitaciones(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        titulo = ttk.Label(frame, text="Habitaciones del Hotel (1 - 10)", font=("Arial", 14))
        titulo.pack(pady=(0, 10))

        # Usamos un Treeview para mostrar número, precio y estado
        columns = ("Número", "Precio/día", "Estado")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones al pie: Seleccionar habitación (para abrir ventana ingreso)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        btn_select = ttk.Button(btn_frame, text="Seleccionar habitación", command=self.on_seleccionar_habitacion)
        btn_select.pack(side=tk.LEFT, padx=(0, 5))
        btn_refresh = ttk.Button(btn_frame, text="Actualizar listado", command=self.actualizar_listado_habitaciones)
        btn_refresh.pack(side=tk.LEFT)

        # Inicializar listado
        self.actualizar_listado_habitaciones()

    def mostrar_habitaciones_panel(self):
        """Foco en la ventana principal y actualiza el listado."""
        self.root.deiconify()
        self.actualizar_listado_habitaciones()

    def actualizar_listado_habitaciones(self):
        """Rellena/actualiza el Treeview con el estado actual de las habitaciones."""
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insertar
        for hab in self.hotel.habitaciones:
            estado = "Disponible" if hab.disponible else "No disponible"
            self.tree.insert("", tk.END, values=(hab.numero, f"${hab.precio_por_dia}", estado))

    def on_seleccionar_habitacion(self):
        """Acción cuando usuario selecciona una habitación en el listado."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar", "Seleccione una habitación del listado.")
            return
        vals = self.tree.item(sel[0], "values")
        numero = int(vals[0])
        habit = self.hotel.get_habitacion(numero)
        if habit is None:
            messagebox.showerror("Error", "Número de habitación inválido.")
            return
        if not habit.disponible:
            messagebox.showerror("Error", f"Habitación {numero} no está disponible.")
            return
        # Abrir ventana de ingreso (check-in) para esa habitación
        self.abrir_ventana_ingreso(numero)

    # ----------------------------
    # Ventana de ingreso (check-in)
    # ----------------------------
    def abrir_ventana_ingreso(self, numero_habitacion: int):
        habit = self.hotel.get_habitacion(numero_habitacion)
        if habit is None:
            messagebox.showerror("Error", "Habitación no encontrada.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Ingreso - Habitación {numero_habitacion}")
        win.geometry("380x340")
        win.transient(self.root)
        win.grab_set()  # modal

        # Etiqueta con número de habitación
        ttk.Label(win, text=f"Habitación {numero_habitacion}", font=("Arial", 12, "bold")).pack(pady=(8, 6))

        # Fecha de ingreso
        frm_fecha = ttk.Frame(win)
        frm_fecha.pack(fill=tk.X, padx=12, pady=6)
        ttk.Label(frm_fecha, text="Fecha de ingreso (AAAA-MM-DD):").pack(anchor=tk.W)
        entry_fecha = ttk.Entry(frm_fecha)
        entry_fecha.pack(fill=tk.X)

        # Nombre
        frm_nom = ttk.Frame(win)
        frm_nom.pack(fill=tk.X, padx=12, pady=6)
        ttk.Label(frm_nom, text="Nombre:").pack(anchor=tk.W)
        entry_nombre = ttk.Entry(frm_nom)
        entry_nombre.pack(fill=tk.X)

        # Apellidos
        frm_ape = ttk.Frame(win)
        frm_ape.pack(fill=tk.X, padx=12, pady=6)
        ttk.Label(frm_ape, text="Apellidos:").pack(anchor=tk.W)
        entry_apellidos = ttk.Entry(frm_ape)
        entry_apellidos.pack(fill=tk.X)

        # Documento de identidad
        frm_doc = ttk.Frame(win)
        frm_doc.pack(fill=tk.X, padx=12, pady=6)
        ttk.Label(frm_doc, text="Documento de identidad:").pack(anchor=tk.W)
        entry_doc = ttk.Entry(frm_doc)
        entry_doc.pack(fill=tk.X)

        # Botones Aceptar / Cancelar
        btns = ttk.Frame(win)
        btns.pack(fill=tk.X, pady=12, padx=12)
        btn_aceptar = ttk.Button(btns, text="Aceptar",
                                 command=lambda: self._accion_aceptar_ingreso(
                                     numero_habitacion,
                                     entry_fecha.get(),
                                     entry_nombre.get(),
                                     entry_apellidos.get(),
                                     entry_doc.get(),
                                     win
                                 ))
        btn_aceptar.pack(side=tk.LEFT, padx=(0, 8))
        btn_cancel = ttk.Button(btns, text="Cancelar", command=win.destroy)
        btn_cancel.pack(side=tk.LEFT)

    def _accion_aceptar_ingreso(self, numero, fecha_str, nombre, apellidos, dni, ventana):
        """Valida los campos y registra el huésped si todo está correcto."""
        # Validaciones: campos obligatorios
        if not (fecha_str.strip() and nombre.strip() and apellidos.strip() and dni.strip()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar formato fecha YYYY-MM-DD
        try:
            fecha_ingreso = datetime.strptime(fecha_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return

        # Fecha de ingreso no puede ser futura
        hoy = date.today()
        if fecha_ingreso > hoy:
            messagebox.showerror("Error", "La fecha de ingreso no puede ser futura.")
            return

        # Registrar ocupación
        habit = self.hotel.get_habitacion(numero)
        if habit is None:
            messagebox.showerror("Error", "Habitación inválida.")
            return
        if not habit.disponible:
            messagebox.showerror("Error", f"Habitación {numero} ya está ocupada.")
            return

        habit.ocupar(nombre.strip(), apellidos.strip(), dni.strip(), fecha_ingreso)

        # Mensaje de confirmación y actualizar listado
        messagebox.showinfo("Registrado", "El huésped ha sido registrado. (Ok)")
        ventana.destroy()
        self.actualizar_listado_habitaciones()

    # ----------------------------
    # Salida de huésped (check-out) - paso 1: solicitar número habitación
    # ----------------------------
    def abrir_ventana_solicitar_num_habitacion_salida(self):
        win = tk.Toplevel(self.root)
        win.title("Salida de huésped - Seleccionar habitación")
        win.geometry("300x140")
        win.transient(self.root)
        win.grab_set()

        ttk.Label(win, text="Ingrese número de habitación a entregar (1-10):").pack(pady=(12, 6))
        entry_num = ttk.Entry(win)
        entry_num.pack(pady=(0, 8), padx=12)

        btns = ttk.Frame(win)
        btns.pack(pady=6)
        btn_ok = ttk.Button(btns, text="Ok",
                            command=lambda: self._accion_ok_salida_num(entry_num.get(), win))
        btn_ok.pack(side=tk.LEFT, padx=(0, 8))
        btn_cancel = ttk.Button(btns, text="Cancelar", command=win.destroy)
        btn_cancel.pack(side=tk.LEFT)

    def _accion_ok_salida_num(self, num_str, ventana):
        """Valida número de habitación e inicia ventana de fecha de salida."""
        # Validar entero
        try:
            numero = int(num_str)
        except ValueError:
            messagebox.showerror("Error", "Número de habitación inválido.")
            return
        habit = self.hotel.get_habitacion(numero)
        if habit is None:
            messagebox.showerror("Error", "Habitación no existe.")
            return
        if habit.disponible:
            messagebox.showerror("Error", f"Habitación {numero} no está ocupada.")
            return

        # Todo bien: cerrar esta ventana y abrir ventana de salida con detalles
        ventana.destroy()
        self.abrir_ventana_salida_detalles(numero)

    # ----------------------------
    # Ventana de salida con fecha de salida, cálculo y registro
    # ----------------------------
    def abrir_ventana_salida_detalles(self, numero_habitacion: int):
        habit = self.hotel.get_habitacion(numero_habitacion)
        if habit is None:
            messagebox.showerror("Error", "Habitación inválida.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Salida - Habitación {numero_habitacion}")
        win.geometry("420x360")
        win.transient(self.root)
        win.grab_set()

        ttk.Label(win, text=f"Habitación {numero_habitacion}", font=("Arial", 12, "bold")).pack(pady=(8, 6))

        # Mostrar datos del huésped y fecha de ingreso (no editables)
        frm_info = ttk.Frame(win)
        frm_info.pack(fill=tk.X, padx=12, pady=6)
        ttk.Label(frm_info, text=f"Huésped: {habit.huesped['nombre']} {habit.huesped['apellidos']}").pack(anchor=tk.W)
        ttk.Label(frm_info, text=f"Documento: {habit.huesped['dni']}").pack(anchor=tk.W)
        ttk.Label(frm_info, text=f"Fecha ingreso: {habit.fecha_ingreso}").pack(anchor=tk.W)

        # Campo para fecha de salida
        frm_fecha_s = ttk.Frame(win)
        frm_fecha_s.pack(fill=tk.X, padx=12, pady=(10, 6))
        ttk.Label(frm_fecha_s, text="Fecha de salida (AAAA-MM-DD):").pack(anchor=tk.W)
        entry_fecha_salida = ttk.Entry(frm_fecha_s)
        entry_fecha_salida.pack(fill=tk.X)

        # Botón calcular
        resultado_frame = ttk.Frame(win)
        resultado_frame.pack(fill=tk.X, padx=12, pady=(12, 6))
        lbl_result_dias = ttk.Label(resultado_frame, text="Días: -")
        lbl_result_dias.pack(anchor=tk.W)
        lbl_result_total = ttk.Label(resultado_frame, text="Total a pagar: -")
        lbl_result_total.pack(anchor=tk.W)

        btns = ttk.Frame(win)
        btns.pack(pady=12)

        def accion_calcular():
            fecha_str = entry_fecha_salida.get().strip()
            if not fecha_str:
                messagebox.showerror("Error", "Ingrese la fecha de salida.")
                return
            # Validar formato fecha
            try:
                fecha_salida = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
                return
            # Comparar fechas
            if fecha_salida <= habit.fecha_ingreso:
                messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de ingreso.")
                return
            # Calcular días y total
            dias, total = habit.calcular_estancia(fecha_salida)
            lbl_result_dias.config(text=f"Días: {dias}")
            lbl_result_total.config(text=f"Total a pagar: ${total}")
            # Habilitar botón registrar salida (lo creamos/desbloqueamos aquí)
            btn_registrar.config(state=tk.NORMAL)
            # Guardamos los datos calculados temporalmente en la ventana
            win._calculo = {"dias": dias, "total": total, "fecha_salida": fecha_salida}

        btn_calcular = ttk.Button(btns, text="Calcular", command=accion_calcular)
        btn_calcular.pack(side=tk.LEFT, padx=(0, 8))

        btn_cancel = ttk.Button(btns, text="Cancelar", command=win.destroy)
        btn_cancel.pack(side=tk.LEFT)

        # Botón registrar salida (inicialmente deshabilitado hasta calcular)
        def accion_registrar_salida():
            calc = getattr(win, "_calculo", None)
            if calc is None:
                messagebox.showwarning("Atención", "Primero debe calcular la cuenta.")
                return
            # Registrar salida: liberar habitación y mostrar resumen
            datos_previos = habit.liberar()
            dias = calc["dias"]
            total = calc["total"]
            fecha_salida = calc["fecha_salida"]
            messagebox.showinfo("Salida registrada",
                                f"Salida registrada para habitación {numero_habitacion}.\n\n"
                                f"Días: {dias}\nTotal a pagar: ${total}\nFecha salida: {fecha_salida}")
            win.destroy()
            self.actualizar_listado_habitaciones()

        btn_registrar = ttk.Button(win, text="Registrar salida", state=tk.DISABLED, command=accion_registrar_salida)
        btn_registrar.pack(pady=(0, 12))

    # ----------------------------
    # Funciones adicionales si se requieren...
    # ----------------------------


# ============================================================
# Función principal
# ============================================================
def main():
    root = tk.Tk()
    app = AppHotel(root)
    root.mainloop()


if __name__ == "__main__":
    main()
