import math
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------
# CLASE BASE
# ---------------------------
class FiguraGeometrica:
    def calcular_volumen(self):
        pass

    def calcular_superficie(self):
        pass


# ---------------------------
# CLASES DERIVADAS
# ---------------------------
class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def calcular_volumen(self):
        return math.pi * (self.radio ** 2) * self.altura

    def calcular_superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)


class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def calcular_volumen(self):
        return (4/3) * math.pi * (self.radio ** 3)

    def calcular_superficie(self):
        return 4 * math.pi * (self.radio ** 2)


class Piramide(FiguraGeometrica):
    def __init__(self, base, altura, apotema):
        self.base = base
        self.altura = altura
        self.apotema = apotema

    def calcular_volumen(self):
        return (1/3) * (self.base ** 2) * self.altura

    
    def calcular_superficie(self):
    # Área base + área lateral (2 * base * apotema)
        return (self.base ** 2) + (2 * self.base * self.apotema)



# ---------------------------
# CLASES DE INTERFAZ GRÁFICA
# ---------------------------

# Ventana principal
class VentanaPrincipal:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Cálculo de Figuras Geométricas")
        raiz.geometry("300x250")

        ttk.Label(raiz, text="Seleccione una figura:", font=("Arial", 12)).pack(pady=20)

        ttk.Button(raiz, text="Cilindro", command=self.abrir_cilindro).pack(pady=10)
        ttk.Button(raiz, text="Esfera", command=self.abrir_esfera).pack(pady=10)
        ttk.Button(raiz, text="Pirámide", command=self.abrir_piramide).pack(pady=10)

    def abrir_cilindro(self):
        VentanaCilindro(self.raiz)

    def abrir_esfera(self):
        VentanaEsfera(self.raiz)

    def abrir_piramide(self):
        VentanaPiramide(self.raiz)


# ---------------------------
# Ventana del CILINDRO
# ---------------------------
class VentanaCilindro:
    def __init__(self, raiz):
        self.ventana = tk.Toplevel(raiz)
        self.ventana.title("Cilindro")
        self.ventana.geometry("300x300")

        ttk.Label(self.ventana, text="CÁLCULO DEL CILINDRO", font=("Arial", 12, "bold")).pack(pady=10)

        # Campos de entrada
        ttk.Label(self.ventana, text="Radio (cm):").pack()
        self.radio = ttk.Entry(self.ventana)
        self.radio.pack()

        ttk.Label(self.ventana, text="Altura (cm):").pack()
        self.altura = ttk.Entry(self.ventana)
        self.altura.pack()

        ttk.Button(self.ventana, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado = ttk.Label(self.ventana, text="")
        self.resultado.pack(pady=10)

    def calcular(self):
        try:
            r = float(self.radio.get())
            h = float(self.altura.get())
            figura = Cilindro(r, h)

            vol = figura.calcular_volumen()
            sup = figura.calcular_superficie()

            self.resultado.config(
                text=f"Volumen: {vol:.2f} cm³\nSuperficie: {sup:.2f} cm²"
            )
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")


# ---------------------------
# Ventana de la ESFERA
# ---------------------------
class VentanaEsfera:
    def __init__(self, raiz):
        self.ventana = tk.Toplevel(raiz)
        self.ventana.title("Esfera")
        self.ventana.geometry("300x250")

        ttk.Label(self.ventana, text="CÁLCULO DE LA ESFERA", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self.ventana, text="Radio (cm):").pack()
        self.radio = ttk.Entry(self.ventana)
        self.radio.pack()

        ttk.Button(self.ventana, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado = ttk.Label(self.ventana, text="")
        self.resultado.pack(pady=10)

    def calcular(self):
        try:
            r = float(self.radio.get())
            figura = Esfera(r)

            vol = figura.calcular_volumen()
            sup = figura.calcular_superficie()

            self.resultado.config(
                text=f"Volumen: {vol:.2f} cm³\nSuperficie: {sup:.2f} cm²"
            )
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido.")


# ---------------------------
# Ventana de la PIRÁMIDE
# ---------------------------
class VentanaPiramide:
    def __init__(self, raiz):
        self.ventana = tk.Toplevel(raiz)
        self.ventana.title("Pirámide")
        self.ventana.geometry("300x320")

        ttk.Label(self.ventana, text="CÁLCULO DE LA PIRÁMIDE", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self.ventana, text="Base (cm):").pack()
        self.base = ttk.Entry(self.ventana)
        self.base.pack()

        ttk.Label(self.ventana, text="Altura (cm):").pack()
        self.altura = ttk.Entry(self.ventana)
        self.altura.pack()

        ttk.Label(self.ventana, text="Apotema (cm):").pack()
        self.apotema = ttk.Entry(self.ventana)
        self.apotema.pack()

        ttk.Button(self.ventana, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado = ttk.Label(self.ventana, text="")
        self.resultado.pack(pady=10)

    def calcular(self):
        try:
            b = float(self.base.get())
            h = float(self.altura.get())
            a = float(self.apotema.get())

            figura = Piramide(b, h, a)

            vol = figura.calcular_volumen()
            sup = figura.calcular_superficie()

            self.resultado.config(
                text=f"Volumen: {vol:.2f} cm³\nSuperficie: {sup:.2f} cm²"
            )
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")


# ---------------------------
# PROGRAMA PRINCIPAL
# ---------------------------
if __name__ == "__main__":
    raiz = tk.Tk()
    app = VentanaPrincipal(raiz)
    raiz.mainloop()
