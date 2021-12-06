def transforma_cateto(num1, num2):
    metros_por_grau = 111320
    cateto = (num1 - num2)
    if cateto < 0:
        cateto = cateto * -1
    x = metros_por_grau * cateto
    return x

def CalcularDistancias(lat1, long1, lat2, long2):
    cat_lat = transforma_cateto(lat1, lat2)
    cat_long = transforma_cateto(long1, long2)

    novo_cateto1 = cat_lat ** 2
    novo_cateto2 = cat_long ** 2
    hipotenusa = (novo_cateto2 + novo_cateto1) ** (1 / 2)
    return hipotenusa