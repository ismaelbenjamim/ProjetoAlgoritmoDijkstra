import json

from PracasRecife.funcionalidades.calcular_distancias import CalcularDistancias
from PracasRecife.models import DistanciasPracas

def ImportarBanco(banco_de_dados):
    f = open(banco_de_dados, 'r', encoding='utf-8')
    pracas = json.loads(f.read())
    f.close()
    numero_id = 1
    numero_alterados = 0
    for numero, praca in enumerate(pracas['records']):
        latitude1 = praca[-2]
        longitude1 = praca[-1]

        for numero_praca_final, praca_final in enumerate(pracas['records']):
            if numero_praca_final != numero:
                latitude2 = praca_final[-2]
                longitude2 = praca_final[-1]

                distancia = CalcularDistancias(latitude1, longitude1, latitude2, longitude2)

                if distancia < 3000:
                    verificar_existe = DistanciasPracas.objects.filter(id=numero_id)
                    if verificar_existe:
                        DistanciasPracas.objects.filter(id=numero_id).update(
                            id_inicial=praca[0],
                            id_final=praca_final[0],
                            distancia=distancia
                        )
                    else:
                        DistanciasPracas.objects.create(
                            id=numero_id,
                            id_inicial=praca[0],
                            id_final=praca_final[0],
                            distancia=distancia
                        )
                    numero_id += 1
