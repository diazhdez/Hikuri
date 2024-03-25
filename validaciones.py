# Valida el ID de la planta
def validar_id(id_planta: str) -> bool:
    return (id_planta.isnumeric())

# Valida el nombre común


def validar_nombre_comun(nombre_comun: str) -> bool:
    nombre_comun = nombre_comun.strip()
    return (len(nombre_comun) > 0 and len(nombre_comun) <= 100)

# Valida el nombre cientifico


def validar_nombre_cientifico(nombre_cientifico: str) -> bool:
    nombre_cientifico = nombre_cientifico.strip()
    return (len(nombre_cientifico) > 0 and len(nombre_cientifico) <= 100)

# Valida la región


def validar_region(region: str) -> bool:
    region = region.strip()
    return (len(region) > 0 and len(region) <= 100)

# Valida las propiedades


def validar_propiedades(propiedades: str) -> bool:
    propiedades = propiedades.strip()
    return (len(propiedades) > 0 and len(propiedades) <= 500)
