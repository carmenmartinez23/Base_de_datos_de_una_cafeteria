from Modelo.Clientes import Cliente
from Modelo.Empleado import Empleado
from Modelo.Pedidos import Pedido
from Modelo.Productos import Producto
from Modelo.Tarjeta import TarjetaFidelidad

clientes_prueba = [
    Cliente("C001", "María", "García López", "612345678", "maria.garcia@gmail.com", "Calle Real 15, Ronda", None),
    Cliente("C002", "Carlos", "Martínez Ruiz", "623456789", "carlos.martinez@hotmail.com", "Avda Andalucía 42, Ronda", None),
    Cliente("C003", "Ana", "Fernández Silva", "634567890", "ana.fernandez@outlook.com", "Plaza España 8, Ronda", None),
    Cliente("C004", "José", "Rodríguez Pérez", "745678901", "jose.rodriguez@yahoo.es", "Calle Armiñán 23, Ronda", None),
    Cliente("C005", "Laura", "Sánchez Moreno", "656789012", "laura.sanchez@gmail.com", "Calle Jerez 34, Ronda", None),
    Cliente("C006", "David", "Jiménez Torres", "667890123", "david.jimenez@telefonica.net", "Paseo Blas Infante 56, Ronda", None),
    Cliente("C007", "Isabel", "Romero Díaz", "678901234", "isabel.romero@icloud.com", "Calle Sevilla 12, Ronda", None),
    Cliente("C008", "Miguel", "Navarro Campos", "789012345", "miguel.navarro@correo.es", "Avda Victoria 78, Ronda", None),
    Cliente("C009", "Carmen", "Muñoz Ortiz", "790123456", "carmen.munoz@gmail.com", "Calle Virgen de la Paz 5, Ronda", None),
    Cliente("C010", "Francisco", "Álvarez Ramos", "601234567", "francisco.alvarez@hotmail.es", "Calle Molino 19, Ronda", None),
    Cliente("C011", "Sofía", "Castro Vargas", "612345987", "sofia.castro@outlook.es", "Plaza Toros 3, Ronda", None),
    Cliente("C012", "Antonio", "Rubio Guerrero", "623456098", "antonio.rubio@yahoo.com", "Calle Carmen Abela 27, Ronda", None),
    Cliente("C013", "Elena", "Morales Gil", "734567109", "elena.morales@gmail.com", "Avda Málaga 61, Ronda", None),
    Cliente("C014", "Javier", "Serrano Medina", "645678210", "javier.serrano@correo.com", "Calle Espinel 45, Ronda", None),
    Cliente("C015", "Raquel", "Vega Herrera", "656789321", "raquel.vega@icloud.com", "Calle Los Remedios 88, Ronda", None),
    Cliente("C016", "Alberto", "Jiménez Soto", "667890432", "alberto.jimenez@gmail.com", "Calle Laurel 14, Ronda", None),
    Cliente("C017", "Patricia", "Ruiz Delgado", "678901543", "patricia.ruiz@hotmail.com", "Avenida Poeta Rilke 29, Ronda", None),
    Cliente("C018", "Fernando", "López Carmona", "689012654", "fernando.lopez@yahoo.es", "Calle Pozo 7, Ronda", None),
    Cliente("C019", "Lucía", "Molina Reyes", "690123765", "lucia.molina@outlook.es", "Plaza Carmen Abela 11, Ronda", None),
    Cliente("C020", "Sergio", "Ortega Santos", "601234876", "sergio.ortega@correo.com", "Calle Virgen de los Dolores 36, Ronda", None)
]

empleados_prueba = [
    Empleado("E001", "Lucía", "Pérez", "600111001", "lucia.perez@cafeteria.com", "Calle Sol 1, Ronda", "1.450€", "Camarero"),
    Empleado("E002", "Manuel", "Gómez", "600111002", "manuel.gomez@cafeteria.com", "Calle Luna 2, Ronda", "1.450€", "Camarero"),
    Empleado("E003", "Paula", "Ruiz", "600111003", "paula.ruiz@cafeteria.com", "Calle Estrella 3, Ronda", "1.600€", "Camarero"),
    Empleado("E004", "Antonio", "López", "600111004", "antonio.lopez@cafeteria.com", "Calle Granada 4, Ronda", "1.950€", "Encargado"),
    Empleado("E005", "Marta", "Hidalgo", "600111005", "marta.hidalgo@cafeteria.com", "Calle Sevilla 5, Ronda", "2.200€", "Jefe"),
    Empleado("E006", "Sergio", "Ortega", "600111006", "sergio.ortega@cafeteria.com", "Calle Cádiz 6, Ronda", "1.700€", "Encargado"),
]

productos_prueba = [
    Producto("1", "Café solo", "Bebida", 1.50, 100),
    Producto("2","Café con leche", "Bebida", 1.80, 100),
    Producto("3","Capuchino", "Bebida", 2.00, 80),
    Producto("4","Latte", "Bebida", 2.20, 80),
    Producto("5","Café americano", "Bebida", 1.70, 90),
    Producto("6","Té verde", "Bebida", 1.60, 60),
    Producto("7","Té chai", "Bebida", 2.10, 60),
    Producto("8","Croissant", "Bollería", 1.40, 50),
    Producto("9","Napolitana", "Bollería", 1.80, 40),
    Producto("10","Magdalena", "Bollería", 1.20, 50),
    Producto("11","Brownie", "Postre", 2.50, 30),
    Producto("12","Tarta de zanahoria", "Postre", 3.00, 25),
    Producto("13","Cookie chocolate", "Postre", 1.50, 40),
    Producto("14","Zumo naranja", "Bebida", 2.00, 35),
    Producto("15","Agua mineral", "Bebida", 1.20, 100)
]

tarjetas_prueba = [
    TarjetaFidelidad("TF001", clientes_prueba[0], 120),
    TarjetaFidelidad("TF002", clientes_prueba[1], 90),
    TarjetaFidelidad("TF003", clientes_prueba[2], 30),
    TarjetaFidelidad("TF004", clientes_prueba[3], 200),
    TarjetaFidelidad("TF005", clientes_prueba[4], 150),
    TarjetaFidelidad("TF006", clientes_prueba[5], 10),
    TarjetaFidelidad("TF007", clientes_prueba[6], 80),
    TarjetaFidelidad("TF008", clientes_prueba[7], 60),
    TarjetaFidelidad("TF009", clientes_prueba[8], 110),
    TarjetaFidelidad("TF010", clientes_prueba[9], 95),
    TarjetaFidelidad("TF011", clientes_prueba[10], 45),
    TarjetaFidelidad("TF012", clientes_prueba[11], 70),
    TarjetaFidelidad("TF013", clientes_prueba[12], 55),
    TarjetaFidelidad("TF014", clientes_prueba[13], 130),
    TarjetaFidelidad("TF015", clientes_prueba[14], 160)
]

importe = [

]

# Número de productos por pedido fijo
productos_por_pedido = 3
num_productos = len(productos_prueba)

for i in range(15):  # 15 pedidos
    # Selección determinista: bloques consecutivos, modulo para repetir al final
    productos_pedido = [
        productos_prueba[(i + j) % num_productos]
        for j in range(productos_por_pedido)
    ]

    # Suma de precios
    total = sum(p.precio for p in productos_pedido)
    importe.append(f"{round(total, 2)}€")

pedidos_prueba = [
    Pedido("P001", 1, clientes_prueba[0], empleados_prueba[0], "2025-01-10", importe[0]),
    Pedido("P002", 2, clientes_prueba[1], empleados_prueba[1], "2025-01-11", importe[1]),
    Pedido("P003", 3, clientes_prueba[2], empleados_prueba[2], "2025-01-12", importe[2]),
    Pedido("P004", 4, clientes_prueba[3], empleados_prueba[3], "2025-01-13", importe[3]),
    Pedido("P005", 5, clientes_prueba[4], empleados_prueba[4], "2025-01-14", importe[4]),
    Pedido("P006", 6, clientes_prueba[5], empleados_prueba[5], "2025-01-15", importe[5]),
    Pedido("P007", 7, clientes_prueba[6], empleados_prueba[5], "2025-01-16", importe[6]),
    Pedido("P008", 8, clientes_prueba[7], empleados_prueba[4], "2025-01-17", importe[7]),
    Pedido("P009", 9, clientes_prueba[8], empleados_prueba[3], "2025-01-18", importe[8]),
    Pedido("P010", 10, clientes_prueba[9], empleados_prueba[2], "2025-01-19", importe[9]),
    Pedido("P011", 11, clientes_prueba[10], empleados_prueba[1], "2025-01-20", importe[10]),
    Pedido("P012", 12, clientes_prueba[11], empleados_prueba[0], "2025-01-21", importe[11]),
    Pedido("P013", 13, clientes_prueba[12], empleados_prueba[1], "2025-01-22", importe[12]),
    Pedido("P014", 14, clientes_prueba[13], empleados_prueba[2], "2025-01-23", importe[13]),
    Pedido("P015", 15, clientes_prueba[14], empleados_prueba[3], "2025-01-24", importe[14])
]

clientes_prueba[0].idPedido = pedidos_prueba[0]
clientes_prueba[1].idPedido = pedidos_prueba[1]
clientes_prueba[2].idPedido = pedidos_prueba[2]
clientes_prueba[3].idPedido = pedidos_prueba[3]
clientes_prueba[4].idPedido = pedidos_prueba[4]
clientes_prueba[5].idPedido = pedidos_prueba[5]
clientes_prueba[6].idPedido = pedidos_prueba[6]
clientes_prueba[7].idPedido = pedidos_prueba[7]
clientes_prueba[8].idPedido = pedidos_prueba[8]
clientes_prueba[9].idPedido = pedidos_prueba[9]
clientes_prueba[10].idPedido = pedidos_prueba[10]
clientes_prueba[11].idPedido = pedidos_prueba[11]
clientes_prueba[12].idPedido = pedidos_prueba[12]
clientes_prueba[13].idPedido = pedidos_prueba[13]
clientes_prueba[14].idPedido = pedidos_prueba[14]
clientes_prueba[15].idPedido = pedidos_prueba[0]
clientes_prueba[16].idPedido = pedidos_prueba[1]
clientes_prueba[17].idPedido = pedidos_prueba[2]
clientes_prueba[18].idPedido = pedidos_prueba[3]
clientes_prueba[19].idPedido = pedidos_prueba[4]

listadeclientes= clientes_prueba
listadeempleados = empleados_prueba
listadeproductos = productos_prueba
listadepedidos = pedidos_prueba
listadetarjeta = tarjetas_prueba
