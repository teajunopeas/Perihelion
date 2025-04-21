# Definir la clase de cada producto
class Producto:
    def __init__(self, id_producto, nombre: str, precio_venta: float):
        # Verificar las variables que no se pueden verificar con ":"
        self.verificar_id(id_producto)

        # Inicializar las variables de la clase
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio_venta = precio_venta


    # de esta manera al usar producto1 == producto2, se llama a esta función internamente
    def __eq__(self, other):
        if isinstance(other, Producto):
            return self.id_producto == other.id_producto
        return False

    def __hash__(self):
        return hash(self.id_producto)

    def __str__(self):
        return f"[{self.id_producto}] {self.nombre} - Precio: {self.precio_venta} $"

    @staticmethod
    def verificar_id(id_producto):
        assert isinstance(id_producto, (int, str)), "id_producto debe ser un entero, o un string único"


class Inventario:
    def __init__(self):
        #Creamos el diccionario vacío
        self.productos = {}

    def agregar_producto(self, producto):
        assert producto.id_producto not in self.productos, f"El producto con ID {producto.id_producto} ya existe en el inventario"

        self.productos[producto.id_producto] = {'Producto': producto, 'Cantidad': 0}
        return f"Producto {producto.nombre} añadido al inventario"

    def incrementar_stock(self, id_producto, cantidad:int):
        assert id_producto in self.productos, f"No se ha encontrado el ID {id_producto} en el inventario"
        self.verificar_cantidad(cantidad)

        self.productos[id_producto]['Cantidad'] += cantidad
        return f"Se han añadido {cantidad} unidades del producto con ID[{id_producto}]"

    def decrementar_stock(self, id_producto, cantidad:int):
        assert id_producto in self.productos, f"No se ha encontrado el ID[{id_producto}] en el inventario"
        assert cantidad < self.productos[id_producto]['Cantidad'], f"El stock actual ({self.productos[id_producto]['Cantidad']}) es menor que la cantidad a vender ({cantidad})."
        self.verificar_cantidad(cantidad)


        self.productos[id_producto]['Cantidad'] -= cantidad
        return f"Se han sustraído {cantidad} unidades del producto con ID[{id_producto}]"

    def consultar_stock(self, id_producto):
        if id_producto in self.productos:
            stock = self.productos[id_producto]['Cantidad'] #Se busca en el diccionario con ID la etiqueta 'Cantidad'
        else:
            stock = 0
        return f"El stock del producto con ID[{id_producto}]: {stock}"

    def valor_total_inventario(self):
        total = 0
        for datos in self.productos.values():
            total += datos['Cantidad'].precio_venta * datos['Cantidad']
        return f"Valor total del inventario: {total}"

    #Función auxiliar para verificar si la cantidad es núm. natural
    @staticmethod
    def verificar_cantidad(cantidad):
        assert cantidad > 0, f"La cantidad añadida debe ser mayor que 0"

    def __str__(self):
        str_inventario = "Estado actuál del inventario:\n"
        for id_producto, datos in self.productos.items():
            producto = datos['Producto']
            cantidad = datos['Cantidad']
            str_inventario += f"{producto} - Stock: {cantidad}\n" #Implicitamente, usamos __str__ de Producto
        return str_inventario


# TEST DE LA CLASE CREADA

# Definición de los objetos
Carpetas    = Producto("car", "Carpetas", 2.3)
Boligrafos  = Producto(1, "Bolígrafos", 0.7)
Gomas       = Producto(2, "Gomas", 0.35)
Lapices     = Producto(3, "Lápices", 0.2)
Estuches    = Producto("est", "Estuches", 7.85)

#Añadir todos los productos al inventario
Trastienda = Inventario()
Trastienda.agregar_producto(Carpetas)
Trastienda.agregar_producto(Boligrafos)
Trastienda.agregar_producto(Gomas)
Trastienda.agregar_producto(Lapices)
Trastienda.agregar_producto(Estuches)

# Comprobar si da error al agregar un producto existente
try:
    Trastienda.agregar_producto(Boligrafos)
except Exception as e:
    print(e)


# Incrementar Stock de cada producto
Trastienda.incrementar_stock("car", 12)
Trastienda.incrementar_stock("est", 44)
Trastienda.incrementar_stock(1,     58)
Trastienda.incrementar_stock(2,     37)
Trastienda.incrementar_stock(3,     44)


# Comprobar el inventario
print(Trastienda)

#Probar a disminuir el stock
Trastienda.decrementar_stock("car", 3)
Trastienda.decrementar_stock(1, 10)
Trastienda.decrementar_stock(2, 6)

# Teóricamente, se debería generar una excepción
try:
    Trastienda.decrementar_stock(3, 186)
except Exception as e:
    print(e)