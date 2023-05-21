# Descripción: Este archivo contiene los parámetros y sets del modelo.
# Todos los datos obtenidos han sido llevado a cabo por una empresa en 2020.


# Sets
I = range(1, 4)  # Monocristalino, Policristalino, Amorfos.
J = range(1, 13)  # Los 12 meses del año.
K = range(1, 5)  # Inversor de tipo 1, 2, 3 & 4.
L = range(1, 3)  # Piso & Techo.

np = len(I)
nm = len(J)
ni = len(K)
ns = len(L)

# Costo Unitario de los Paneles Solares (En Watt Peak)
costo_unitario_panel = [10, 10, 10]  # Arreglar

# Costos de Transporte de los Paneles Solares (En Watt Peak)
costos_transporte_panel = [10, 10, 10]  # Arreglar

# Costos de Instalación de los Paneles Solares (En Watt Peak)
costos_instalacion_panel = [10, 10, 10]  # Arreglar

# Costos de Mantenimiento de los Paneles Solares (En Watt Peak)
costos_mantenimiento_panel = [10, 10, 10]  # Arreglar

# Costo Unitario del Inversor de tipo K (En Watt Peak)
costo_unitario_inversor = [10, 10, 10, 10]  # Arreglar

# Constos de Transporte del Inversor de tipo K (En Watt Peak)
costos_transporte_inversor = [10, 10, 10, 10]  # Arreglar

# Costos de Instalación del Inversor de tipo K (En Watt Peak)
costos_instalacion_inversor = [10, 10, 10, 10]  # Arreglar

# Costos de Mantenimiento del Inversor de tipo K (En Watt Peak)
costos_mantenimiento_inversor = [10, 10, 10, 10]  # Arreglar

# Numero Máximo de Paneles del tipo I por inversor del tipo K
nro_max_paneles = [[100, 10, 10, 10], [100, 10, 10, 10],
                   [100, 10, 10, 10]]  # Arreglar

# Espacio disponible por tipo de suelo L (en m2)
espacio_disponible = [1250, 4100]  # Arreglar

# Tamaño del panel I (en m2)
tamano_panel = [1, 1, 1]  # Arreglar

# Energía producida por panel I en mes J
energia_producida_panel = [[100, 100, 100, 100, 1000, 10, 10, 10, 10, 10, 10, 10],
                           [100, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                           [100, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]]  # Arreglar

# Parámetros
C = {i: costo_unitario_panel[i - 1] for i in I}
CT = {i: costos_transporte_panel[i - 1] for i in I}
CI = {i: costos_instalacion_panel[i - 1] for i in I}
CM = {i: costos_mantenimiento_panel[i - 1] for i in I}
CZ = {k: costo_unitario_inversor[k - 1] for k in K}
CTZ = {k: costos_transporte_inversor[k - 1] for k in K}
CIZ = {k: costos_instalacion_inversor[k - 1] for k in K}
CMZ = {k: costos_mantenimiento_inversor[k - 1] for k in K}
muZ = {(i, k): nro_max_paneles[i - 1][k - 1] for i in I for k in K}
EA = {l: espacio_disponible[l - 1] for l in L}
T = {i: tamano_panel[i - 1] for i in I}
PC = 25  # Arreglar
SC = 10  # Arreglar
E = {(i, j): energia_producida_panel[i - 1][j - 1] for i in I for j in J}
PT = 1000000000000000000  # Arreglar
M = 1 * (10**100)
