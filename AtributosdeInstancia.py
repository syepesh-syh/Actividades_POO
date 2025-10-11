class Persona:
    def __init__(self, Nombre, Apellido, Documento, Nacimiento):
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Documento = Documento
        self.Nacimiento = Nacimiento

Persona1 = Persona("Santiago", "Yepes", "1007222328","19 de febrero del 20")
Persona2 = Persona("Gloria","Hurtado","43515432","14 de marzo de 1967")

print(Persona1.Nombre)
print(Persona2.Nombre)
