import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

# -----------------------------
# Clase Contacto (Modelo)
# -----------------------------
class Contacto:
    def __init__(self, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        # Ahora se muestra toda la información en la lista
        return (f"{self.nombres} {self.apellidos}  |  "
                f"Nac: {self.fecha_nacimiento}  |  "
                f"Dir: {self.direccion}  |  "
                f"Tel: {self.telefono}  |  "
                f"Correo: {self.correo}")


# -----------------------------
# Clase VentanaPrincipal (Vista-Controlador)
# -----------------------------
class VentanaAgenda:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Agenda Personal")
        self.ventana.geometry("750x500")

        # Lista donde se almacenan los contactos
        self.contactos = []

        # -----------------------------
        # Entradas de texto
        # -----------------------------
        tk.Label(self.ventana, text="Nombres:").pack()
        self.ent_nombres = tk.Entry(self.ventana)
        self.ent_nombres.pack()

        tk.Label(self.ventana, text="Apellidos:").pack()
        self.ent_apellidos = tk.Entry(self.ventana)
        self.ent_apellidos.pack()

        tk.Label(self.ventana, text="Fecha de nacimiento:").pack()
        self.ent_fecha = DateEntry(self.ventana, date_pattern='yyyy-mm-dd')
        self.ent_fecha.pack()

        tk.Label(self.ventana, text="Dirección:").pack()
        self.ent_direccion = tk.Entry(self.ventana)
        self.ent_direccion.pack()

        tk.Label(self.ventana, text="Teléfono:").pack()
        self.ent_telefono = tk.Entry(self.ventana)
        self.ent_telefono.pack()

        tk.Label(self.ventana, text="Correo electrónico:").pack()
        self.ent_correo = tk.Entry(self.ventana)
        self.ent_correo.pack()

        # -----------------------------
        # Botón Agregar
        # -----------------------------
        tk.Button(self.ventana, text="Agregar", command=self.agregar_contacto).pack(pady=10)

        # -----------------------------
        # ListView (Listbox)
        # -----------------------------
        tk.Label(self.ventana, text="Lista de contactos:").pack()
        self.lista_contactos = tk.Listbox(self.ventana, width=100, height=10)
        self.lista_contactos.pack(pady=10)

        self.ventana.mainloop()

    # -----------------------------
    # Método para agregar contacto
    # -----------------------------
    def agregar_contacto(self):
        nombres = self.ent_nombres.get().strip()
        apellidos = self.ent_apellidos.get().strip()
        fecha = self.ent_fecha.get()
        direccion = self.ent_direccion.get().strip()
        telefono = self.ent_telefono.get().strip()
        correo = self.ent_correo.get().strip()

        # Validación simple
        if not (nombres and apellidos and direccion and telefono and correo):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Crear el nuevo contacto
        nuevo = Contacto(nombres, apellidos, fecha, direccion, telefono, correo)
        self.contactos.append(nuevo)

        # Añadirlo a la lista visual con la representación completa
        self.lista_contactos.insert(tk.END, str(nuevo))

        # Limpiar entradas
        self.ent_nombres.delete(0, tk.END)
        self.ent_apellidos.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_correo.delete(0, tk.END)

        messagebox.showinfo("Contacto agregado", "El contacto se ha añadido exitosamente.")


# -----------------------------
# Ejecutar el programa
# -----------------------------
if __name__ == "__main__":
    VentanaAgenda()
