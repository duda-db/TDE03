# -*- coding: utf-8 -*-
import os
from collections import defaultdict
import email
directory_name = "/amostra/"

class Grafo:
    def __init__(self, direcionado=False, ponderado=False):
        self.lista_adjacencias = defaultdict(list)
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.ordem = 0
        self.tamanho = 0

    def adiciona_aresta(self, u, v, peso=None):
        if peso is None:
            peso = 1 if not self.ponderado else None
        self.lista_adjacencias[u].append((v, peso))
        if not self.direcionado:
            self.lista_adjacencias[v].append((u, peso))
        self.tamanho += 1
        self.atualiza_ordem()

    def remove_aresta(self, u, v):
        self.lista_adjacencias[u] = [(vertex, weight) for vertex, weight in self.lista_adjacencias[u] if vertex != v]
        if not self.direcionado:
            self.lista_adjacencias[v] = [(vertex, weight) for vertex, weight in self.lista_adjacencias[v] if vertex != u]
        self.tamanho -= 1
        self.atualiza_ordem()

    def remove_vertice(self, u):
        if u in self.lista_adjacencias:
            del self.lista_adjacencias[u]
            for vertex in self.lista_adjacencias:
                self.lista_adjacencias[vertex] = [(v, peso) for v, peso in self.lista_adjacencias[vertex] if v != u]
            self.atualiza_ordem()
            if not self.direcionado:
                self.tamanho -= sum(1 for vertex in self.lista_adjacencias[u])

    def tem_aresta(self, u, v):
        return any(vertex == v for vertex, _ in self.lista_adjacencias[u])

    def grau(self, u):
        return len(self.lista_adjacencias[u])

    def grau_entrada(self, u):
        if self.direcionado:
            return sum(1 for vertices in self.lista_adjacencias.values() for vertex, _ in vertices if vertex == u)
        else:
            return None

    def grau_saida(self, u):
        if self.direcionado:
            return len(self.lista_adjacencias[u])
        else:
            return None

    def retorna_adjacentes(self, u):
        return [vertex for vertex, _ in self.lista_adjacencias[u]]

    def get_max_arestas(self):
        if self.direcionado:
            return float('inf')
        else:
            n = len(self.lista_adjacencias)
            return n * (n - 1) / 2

    def atualiza_ordem(self):
        self.ordem = len(self.lista_adjacencias)
    
    def Djkstra(self, node_origem, node_destino):
            menor_caminho = {node_origem: (None, 0)}
            node_atual = node_origem
            visitados = set()

            while node_atual != node_destino:
                visitados.add(node_atual)
                destinos = self.lista_adjacencias[node_atual]
                peso_ate_node_atual = menor_caminho[node_atual][1]

                for proximo_node, peso in destinos:
                    peso = peso_ate_node_atual + peso
                    if proximo_node not in menor_caminho:
                        menor_caminho[proximo_node] = (node_atual, peso)
                    else:
                        peso_minimo_atual = menor_caminho[proximo_node][1]
                        if peso_minimo_atual > peso:
                            menor_caminho[proximo_node] = (node_atual, peso)

                proximos_destinos = {node: menor_caminho[node] for node in menor_caminho if node not in visitados}
                if not proximos_destinos:
                    return "Não é possível realizar essa rota."
                #próximo node é o destino com o menor peso
                node_atual = min(proximos_destinos, key=lambda k: proximos_destinos[k][1])

            #revisita os destinos na ordem do caminho mais curto
            caminho = []
            while node_atual is not None:
                caminho.append(node_atual)
                proximo_node = menor_caminho[node_atual][0]
                node_atual = proximo_node
            #inverte o caminho
            caminho = caminho[::-1]
            return caminho, menor_caminho[node_destino][1]


emails = {}

G = Grafo(direcionado=True, ponderado=True)

def primeira_questao():
    cwd = os.getcwd() 
    path = cwd + directory_name
    folders = os.listdir(path)
    for someDir in folders:
        for dirpath, dirnames, filenames in os.walk(path + "/" + someDir):
            for f in filenames:
                try:
                    with open(path + "/" + someDir + "/all_documents/" + f, "r") as f:
                        message = email.message_from_file(f)
                        email_parser = email.parser.Parser()
                        parsed_message = email_parser.parsestr(message.as_string())

                        sender = parsed_message["From"]
                        receiver = parsed_message["To"]
                        if receiver != None:
                            receivers = receiver.split(",")
                            for r in receivers:
                                txt = r.strip()
                                senderReceiver = sender + ", " + txt
                                try:
                                    emails[senderReceiver] += 1 
                                except KeyError:
                                    emails[senderReceiver] = 1                                     
                                     
                                G.adiciona_aresta(sender, txt, emails[senderReceiver])
                            
                except FileNotFoundError:
                    pass
    for k, v in G.lista_adjacencias.items():
        f = open("questao1.txt", "a")
        f.write(f"{k} -> {v}\n")
        f.close()


def segunda_questao():
    print(f"o grafo G possui {G.ordem} vértices e {G.tamanho} arestas.") 
    sort = sorted(G.lista_adjacencias.items(), key=lambda k: G.grau_entrada(k[0]), reverse=True)
    i = 0
    for k,v in sort:
        if (i < 20):
            print(f"{k} - {G.grau_entrada(k)}")
        else:
            break
        i += 1
    print("-----------------------------------")
    sort1 = sorted(G.lista_adjacencias.items(), key=lambda k: G.grau_saida(k[0]), reverse=True)
    j = 0
    for k,v in sort1:
        if (j < 20):
            print(f"{k} - {G.grau_saida(k)}")
        else:
            break
        j += 1
        
    
def sexta_questao():
    print(G.Djkstra("Maçã", "Banana"))
        
        
G = Grafo(direcionado=True)
def quarta_questao():
    selected_node = "martin.cuilla@enron.com"
    searched_node = "felicia.doan@enron.com"
    queue = []
    visited = []
    for items in G.lista_adjacencias[selected_node]:
        queue.append(items[0])
    while len(queue) > 0:
        visited.append(queue[0])
        if (queue[0] == searched_node):
            print(f"\n{visited}")
            break
        for items in G.lista_adjacencias[queue[0]]:
            if items[0] in visited or items[0] in queue:
                pass
            else:
                queue.append(items[0])            
        queue.pop(0)
        

def terceira_questao():
    lists = []
    for k, v in G.lista_adjacencias.items():
        if G.direcionado:
            if G.grau_entrada(k) != G.grau_saida(k):
                lists.append("Um dos nós do grafo não possui um grau de entrada e saída que sejam iguais.")
                break
        else:
            if G.grau_entrada(k) % 2 != 0 or G.grau_saida(k) % 2 != 0:
                lists.append("Um dos nós do grafo não possui grau par.")
                break
    print(lists)
            
        
def main():
    primeira_questao()
    segunda_questao()
    #quarta_questao()

    #sexta_questao()
    terceira_questao()
                

if __name__ == "__main__":
    main()