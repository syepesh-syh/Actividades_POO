import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ============================================================
#                    CLASE EMPLEADO
# ============================================================
class Empleado:
    """Representa un empleado y calcula su salario mensual."""

    def __init__(self, nombre, apellidos, cargo, genero,
                 salario_dia, dias_trabajados,
                 otros_ingresos, pagos_salud, aporte_pensiones):

        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.generero = genero
        self.salario_dia = float(salario_dia)
        self.dias_trabajados = int(dias_trabajados)
        self.otros_ingresos = float(otros_ingresos)
        self.pagos_salud = float(pagos_salud)
        self.aporte_pensiones = float(aporte_pensiones)

    def calcular_salario_mensual(self):
        """Calcula el salario del empleado según la fórmula dada."""
        salario = (self.dias_trabajados * self.salario_dia)
        salario += self.otros_ingresos
        salario -= self.pagos_salud
        salario -= self.aporte_pensiones
        return salario


# ============================================================
#                    CLASE NÓMINA
# ============================================================
class Nomina:
    """Maneja la lista de empleados y el cálculo total."""

    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, emp):
        self.empleados.append(emp)

    def total_nomina(self):
        return sum(emp.calcular_salario_mensual() for emp in self.empleados)

    def generar_archivo(self, ruta_archivo):
        """Genera un archivo TXT con TODA la información de cada empleado."""
        with open(ruta_archivo, "w", encoding="utf-8") as f:

            f.write("=========== NÓMINA DE EMPLEADOS ===========\n\n")

            for emp in self.empleados:
                sueldo = emp.calcular_salario_mensual()

                f.write("--------------------------------------------------\n")
                f.write(f"Nombre: {emp.nombre}\n")
                f.write(f"Apellidos: {emp.apellidos}\n")
                f.write(f"Cargo: {emp.cargo}\n")
                f.write(f"Género: {emp.generero}\n")
                f.write(f"Salario por día: {emp.salario_dia}\n")
                f.write(f"Días trabajados: {emp.dias_trabajados}\n")
                f.write(f"Otros ingresos: {emp.otros_ingresos}\n")
                f.write(f"Pagos salud: {emp.pagos_salud}\n")
                f.write(f"Aporte pensiones: {emp.aporte_pensiones}\n")
                f.write(f"➡ Sueldo mensual: ${sueldo:.2f}\n")
                f.write("--------------------------------------------------\n\n")

            f.write("\n=========== TOTAL NÓMINA ===========\n")
            f.write(f"Total a pagar: ${self.total_nomina():.2f}\n")


# Instancia global de nómina
nomina = Nomina()


# ============================================================
#             VENTANA PARA AGREGAR EMPLEADO
# ============================================================
def ventana_agregar_empleado():
    win = tk.Toplevel()
    win.title("Agregar empleado")
    win.geometry("350x450")

    # Etiquetas y entradas de texto
    tk.Label(win, text="Nombre:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Apellidos:").pack()
    entry_apellidos = tk.Entry(win)
    entry_apellidos.pack()

    # Lista de cargos (JList equivalente)
    tk.Label(win, text="Cargo:").pack()
    lista_cargos = tk.Listbox(win, height=3, exportselection=False)
    for cargo in ["Directivo", "Estratégico", "Operativo"]:
        lista_cargos.insert(tk.END, cargo)
    lista_cargos.pack()

    # Género (RadioButtons)
    genero_var = tk.StringVar(value="Masculino")
    tk.Label(win, text="Género:").pack()
    tk.Radiobutton(win, text="Masculino", variable=genero_var, value="Masculino").pack()
    tk.Radiobutton(win, text="Femenino", variable=genero_var, value="Femenino").pack()

    # Salario día
    tk.Label(win, text="Salario por día:").pack()
    entry_salario = tk.Entry(win)
    entry_salario.pack()

    # Días trabajados
    tk.Label(win, text="Días trabajados (1-31):").pack()
    spin_dias = tk.Spinbox(win, from_=1, to=31)
    spin_dias.pack()

    # Otros ingresos
    tk.Label(win, text="Otros ingresos:").pack()
    entry_ingresos = tk.Entry(win)
    entry_ingresos.pack()

    # Pagos salud
    tk.Label(win, text="Pagos salud:").pack()
    entry_salud = tk.Entry(win)
    entry_salud.pack()

    # Aporte pensiones
    tk.Label(win, text="Aporte pensiones:").pack()
    entry_pensiones = tk.Entry(win)
    entry_pensiones.pack()

    # Acción del botón
    def guardar_empleado():
        try:
            cargo = lista_cargos.get(lista_cargos.curselection())

            emp = Empleado(
                entry_nombre.get(),
                entry_apellidos.get(),
                cargo,
                genero_var.get(),
                float(entry_salario.get()),
                int(spin_dias.get()),
                float(entry_ingresos.get()),
                float(entry_salud.get()),
                float(entry_pensiones.get())
            )

            nomina.agregar_empleado(emp)
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
            win.destroy()

        except:
            messagebox.showerror("Error", "Complete todos los campos correctamente.")

    tk.Button(win, text="Guardar empleado", command=guardar_empleado).pack(pady=10)


# ============================================================
#              VENTANA CALCULAR NÓMINA
# ============================================================
def ventana_calcular_nomina():
    win = tk.Toplevel()
    win.title("Nómina")
    win.geometry("500x300")

    # Tabla
    columnas = ("Nombre", "Apellidos", "Salario")
    tabla = ttk.Treeview(win, columns=columnas, show="headings")
    tabla.pack(fill="both", expand=True)

    for col in columnas:
        tabla.heading(col, text=col)

    # Insertar datos en tabla
    for emp in nomina.empleados:
        tabla.insert("", tk.END, values=(
            emp.nombre,
            emp.apellidos,
            f"${emp.calcular_salario_mensual():.2f}"
        ))

    # Total de nómina
    total = nomina.total_nomina()
    tk.Label(win, text=f"TOTAL NÓMINA: ${total:.2f}",
             font=("Arial", 12, "bold")).pack(pady=10)


# ============================================================
#                  GUARDAR ARCHIVO COMPLETO
# ============================================================
def guardar_archivo():
    carpeta = filedialog.askdirectory()
    if carpeta:
        ruta = carpeta + "/Nomina.txt"
        nomina.generar_archivo(ruta)
        messagebox.showinfo("Archivo guardado", f"Archivo creado correctamente:\n{ruta}")


# ============================================================
#                   VENTANA PRINCIPAL
# ============================================================
root = tk.Tk()
root.title("Sistema de Nómina")
root.geometry("400x200")

# Barra de menú
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_bar.add_command(label="Agregar empleado", command=ventana_agregar_empleado)
menu_bar.add_command(label="Calcular nómina", command=ventana_calcular_nomina)
menu_bar.add_command(label="Guardar archivo", command=guardar_archivo)

tk.Label(root, text="Sistema de Nómina", font=("Arial", 16)).pack(pady=40)

root.mainloop()
