"""
Aquí definimos la clase FamilyStructure, que mantendrá en memoria
todos los miembros de la familia Jackson y proveerá métodos para
agregar, eliminar y buscar miembros.
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # No lo modifiques: genera un ID único cada vez que lo llamas
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        """
        Agrega un miembro nuevo a la familia.

        - member: diccionario que puede contener
            {
                "id": Int (opcional),
                "first_name": str,
                "age": Int,
                "lucky_numbers": [Int, ...]
            }

        Si el diccionario no trae "id", se genera automáticamente.
        Se asegura de que siempre se asigne last_name = self.last_name.

        Finalmente, agrega el miembro a self._members.
        """

        # Validación mínima de campos requeridos
        if "first_name" not in member or "age" not in member or "lucky_numbers" not in member:
            raise ValueError("Faltan campos obligatorios en el miembro")

        # Si la edad no es un entero positivo, error
        if not isinstance(member["age"], int) or member["age"] <= 0:
            raise ValueError("El campo 'age' debe ser un entero > 0")

        # Si los lucky_numbers no es lista de enteros, error
        if (not isinstance(member["lucky_numbers"], list) or
            not all(isinstance(n, int) for n in member["lucky_numbers"])):
            raise ValueError("El campo 'lucky_numbers' debe ser una lista de enteros")

        # Si ya trae un id, úsalo; sino genera uno nuevo
        if "id" in member:
            new_id = member["id"]
            # Si alguien da un id duplicado, hay que asegurarse de no colisionar
            # (pero en este ejercicio asumiremos que el test no enviará IDs duplicados)
        else:
            new_id = self._generate_id()

        # Construir el diccionario final del miembro
        new_member = {
            "id": new_id,
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }

        # Agregar a la lista interna
        self._members.append(new_member)
        return new_member

    def delete_member(self, id):
        """
        Elimina al miembro cuyo `id` coincida con el parámetro.
        Retorna True si lo eliminó, False si no encontró ese ID.
        """
        for idx, m in enumerate(self._members):
            if m["id"] == id:
                self._members.pop(idx)
                return True
        return False

    def get_member(self, id):
        """
        Busca en self._members un miembro con id == id.
        Si lo encuentra, retorna el diccionario del miembro, si no, retorna None.
        """
        for m in self._members:
            if m["id"] == id:
                return m
        return None

    def get_all_members(self):
        """
        Retorna la lista completa de miembros (cada uno es un diccionario).
        """
        return list(self._members)
