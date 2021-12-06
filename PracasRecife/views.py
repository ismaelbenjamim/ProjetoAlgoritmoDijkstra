import json

from django.shortcuts import render
from django.views.generic import TemplateView

from PracasRecife.funcionalidades.dijkstra import dijkstra
from PracasRecife.funcionalidades.importar_banco import ImportarBanco
from PracasRecife.models import DistanciasPracas, Grafo


class ImportarBancoView(TemplateView):
    template_name = 'importar_banco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quantidade_arestas = DistanciasPracas.objects.all().count()
        if quantidade_arestas > 0:
            resultado = (quantidade_arestas * 100) / 34670
            context['banco_de_dados'] = int(resultado)
        else:
            context['banco_de_dados'] = 0
        if quantidade_arestas == 34670 and Grafo.objects.all().count() > 0:
            context['grafo'] = 100
        else:
            context['grafo'] = 0
        return context


class ResultadoImportarBancoView(TemplateView):
    template_name = 'resultado_importar_banco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if DistanciasPracas.objects.all().count() > 0:
            DistanciasPracas.objects.all().delete()
        ImportarBanco('PracasRecife/bd_pracas_recife.json')
        grafo = {}
        valor_vertice = 0
        arestas_id = {}
        arestas = DistanciasPracas.objects.all()
        for aresta in arestas:
            if valor_vertice == 0:
                valor_vertice = aresta.id_inicial
            if valor_vertice != aresta.id_inicial:
                grafo[str(valor_vertice)] = arestas_id
                arestas_id = {}
                valor_vertice = aresta.id_inicial
            if aresta.id == arestas.last().id:
                grafo[str(valor_vertice)] = arestas_id

            arestas_id[str(aresta.id_final)] = aresta.distancia

        Grafo.objects.create(
            grafo=grafo
        )

        quantidade_arestas = DistanciasPracas.objects.all().count()
        if quantidade_arestas > 0:
            resultado = (quantidade_arestas * 100) / 34670
            context['banco_de_dados'] = int(resultado)
        else:
            context['banco_de_dados'] = 0
        if quantidade_arestas == 34670 and Grafo.objects.all().count() > 0:
            context['grafo'] = 100
        else:
            context['grafo'] = 0

        return context

class PorcentagemImportarBancoView(TemplateView):
    template_name = 'porcentagem_importar_banco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quantidade_arestas = DistanciasPracas.objects.all().count()
        if quantidade_arestas > 0:
            resultado = (quantidade_arestas * 100) / 34670
            context['banco_de_dados'] = int(resultado)
        else:
            context['banco_de_dados'] = 0
        if quantidade_arestas == 34670 and Grafo.objects.all().count() > 0:
            context['grafo'] = 100
        else:
            context['grafo'] = 0

        return context


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class ProcurarPracaView(TemplateView):
    template_name = 'procurar_pecas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        f = open('PracasRecife/bd_pracas_recife.json', 'r', encoding='utf-8')
        pracas = json.loads(f.read())
        f.close()
        lista_pracas = []
        for praca in pracas['records']:
            if praca[1]:
                lista_pracas.append([praca[0], praca[1]])
            else:
                lista_pracas.append([praca[0], praca[3]])
        context['lista_pracas'] = lista_pracas

        quantidade_arestas = DistanciasPracas.objects.all().count()
        if quantidade_arestas == 34670 and Grafo.objects.all().count() > 0:
            context['banco_importado'] = True
        else:
            context['banco_importado'] = False
        return context


class ResultadoBuscaPracaView(TemplateView):
    template_name = 'resultado_busca_praca.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        praca_inicial = self.request.GET.get('praca_inicial')
        praca_final = self.request.GET.get('praca_final')

        if praca_inicial and praca_final:
            if praca_inicial != '0' and praca_final != '0':
                grafo_obj = Grafo.objects.all().last()
                grafo = json.loads(str(grafo_obj.grafo).replace("\'", "\""))
                p = dijkstra(grafo, praca_inicial, praca_final)

                f = open('PracasRecife/bd_pracas_recife.json', 'r', encoding='utf-8')
                pracas = json.loads(f.read())
                f.close()
                distancias_pracas = []
                for num, x in enumerate(p):
                    try:
                        distancias_pracas.append(DistanciasPracas.objects.get(id_inicial=p[num], id_final=p[num+1]).distancia)
                    except:
                        distancias_pracas.append(None)

                lista_pracas = []
                for id in p:
                    for praca in pracas['records']:
                        if int(id) == praca[0]:
                            if praca[1] != "":
                                lista_pracas.append([praca[0], praca[1], praca[-2], praca[-1]])
                            else:
                                lista_pracas.append([praca[0], praca[3], praca[-2], praca[-1]])

                if lista_pracas == [None]:
                    context['resposta'] = 'Não existe um menor caminho entre essas praças'
                else:
                    context['resposta'] = zip(lista_pracas, distancias_pracas)


        return context
