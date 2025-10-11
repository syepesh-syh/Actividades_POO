import tkinter as tk
from tkinter import messagebox
import statistics

class VentanaNotas:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Cálculo de Notas")
        self.ventana.geometry("350x400")
        self.ventana.resizable(False, False)

        # Lista para guardar las entradas de las notas
        self.entradas = []

        # Etiqueta de título
        tk.Label(self.ventana, text="Ingrese las 5 notas del estudiante",
                 font=("Arial", 12, "bold")).pack(pady=10)

        # Crear las etiquetas y cajas de texto para las notas
        for i in range(5):
            frame = tk.Frame(self.ventana)
            frame.pack(pady=3)
            tk.Label(frame, text=f"Nota {i+1}:", width=10, anchor="w").pack(side="left")
            entrada = tk.Entry(frame, width=10)
            entrada.pack(side="left")
            self.entradas.append(entrada)

        # Botones de acción
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=15)

        tk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=10)

        # Etiquetas de resultados
        self.etiqueta_promedio = tk.Label(self.ventana, text="Promedio: ", font=("Arial", 10))
        self.etiqueta_promedio.pack()
        self.etiqueta_desviacion = tk.Label(self.ventana, text="Desviación estándar: ", font=("Arial", 10))
        self.etiqueta_desviacion.pack()
        self.etiqueta_mayor = tk.Label(self.ventana, text="Mayor nota: ", font=("Arial", 10))
        self.etiqueta_menor = tk.Label(self.ventana, text="Menor nota: ", font=("Arial", 10))
        self.etiqueta_mayor.pack()
        self.etiqueta_menor.pack()

    def calcular(self):
        try:
            # Obtener las notas como números flotantes
            notas = [float(e.get()) for e in self.entradas]
            
            # Validar rango de notas
            if not all(0 <= n <= 5 for n in notas):
                messagebox.showerror("Error", "Las notas deben estar entre 0 y 5.")
                return
            
            # Calcular resultados
            promedio = statistics.mean(notas)
            desviacion = statistics.stdev(notas)
            mayor = max(notas)
            menor = min(notas)

            # Mostrar resultados
            self.etiqueta_promedio.config(text=f"Promedio: {promedio:.2f}")
            self.etiqueta_desviacion.config(text=f"Desviación estándar: {desviacion:.2f}")
            self.etiqueta_mayor.config(text=f"Mayor nota: {mayor}")
            self.etiqueta_menor.config(text=f"Menor nota: {menor}")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese solo números válidos.")

    def limpiar(self):
        # Limpiar las entradas y etiquetas
        for e in self.entradas:
            e.delete(0, tk.END)
        self.etiqueta_promedio.config(text="Promedio: ")
        self.etiqueta_desviacion.config(text="Desviación estándar: ")
        self.etiqueta_mayor.config(text="Mayor nota: ")
        self.etiqueta_menor.config(text="Menor nota: ")

    def ejecutar(self):
        self.ventana.mainloop()


# Programa principal
if __name__ == "__main__":
    app = VentanaNotas()
    app.ejecutar()

