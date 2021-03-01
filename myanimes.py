import requests
import json
import os, sys
from time import sleep
import traceback
# pip install mal-api
from mal import AnimeSearch


# pega os id da lista de animes
def id_animes():
    lista_id = []
    i = 0
    erros =  0
    count = 0
    # tenta entrar no json pra pegar os animes - nomes
    id = 1
    try:
        # abre o txt
        arquivo = open("animess.txt", "r",encoding='utf-8')
    # caso nao conseguir sai fora
    except:
        print(traceback.format_exc())
        print("verifica o arquivo ou nome ")
        # sair
        sys.exit()
    # linhs do txt
    linhas = arquivo.readlines()
    # for na lista  de animes do json
    for nomes_animes in linhas:
        # tenta pegar os nomes
        nomes_animes = nomes_animes.rstrip('\n')
        nomes_animes = nomes_animes.rstrip('\t')
        # pula linhas pares, os nome dos anime esta nas linhas impares
        if id % 2 == 1:
            print(nomes_animes)
            try:
                query = '''
                    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                        Page (page: $page, perPage: $perPage) {
                            media (id: $id, search: $search, type: ANIME, sort: POPULARITY_DESC) {
                                id
                                title {
                                    romaji
                                }
                            }
                        }
                    }
                    '''
                variables = {
                    'search': nomes_animes,
                    'page': 1,
                    'perPage': 1,
                    'MediaType': "ANIME"
                }
                url = 'https://graphql.anilist.co'
                response = requests.post(url, json={'query': query, 'variables': variables})
                response = json.loads(response.text)
                # pega o id do response
                response_id = response['data']['Page']['media'][0]['id']
                lista_id.append(response_id)
                print(f"id: {count} = id:{lista_id[i]} ")
                i += 1
                count += 1
                id += 1
            # caso aconteça algum erro 
            except:
                print("esse anime nao consegui achar o id: ",nomes_animes)
                try:
                    print("tentado com o My Anime List")
                    search = AnimeSearch(nomes_animes)
                    lista_id.append(search.results[0].mal_id)
                    print(f"id do My Anine List: {search.results[0].mal_id}")
                    print(f"id>: {count} = id:{lista_id[i]} ")
                    i += 1
                    count += 1
                except:
                    print("erro")
                    erros += 1
                    print("erros: ", erros)
        else:
            id += 1  
    # tudo pronto
    return lista_id


# função que faz as traquinagem 
def request_animes():
    lista_animes = []
    i = 0
    erros = 0
    lista_id = id_animes()
    # for nos na lista de ids
    for id_nomes in lista_id:
        # tenta pegar os nomes
        try:
            # Here we define our query as a multi-line string
            query = ''' 
              query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                    Page(page: $page, perPage: $perPage) {
                      media(id: $id, search: $search, type: ANIME) {
                        id
                        title {
                          romaji
                        }
                        episodes
                        description
                        genres
                        tags {
                          name
                        }
                        studios {
                          nodes {
                            name
                          }
                        }
                        meanScore
                        averageScore
                        popularity
                      }
                    }
                  }
              '''''
            # Define our query variables and values that will be used in the query request
            variables = {
                'id':  id_nomes
            }
            # url da API
            url = 'https://graphql.anilist.co'
            # Make the HTTP Api request
            response = requests.post(url, json={'query': query, 'variables': variables})
            # faz virar um dict python 
            response = json.loads(response.text)
            # pega as informaçoes que precisamos 
            response_desc = response['data']['Page']['media'][0]
            id = response_desc['id']
            title = response_desc['title']['romaji']
            episodes = response_desc['episodes']
            description = response_desc['description']
            genres = response_desc['genres']
            studios = response_desc['studios']['nodes'] 
            popularity = response_desc['popularity']
            meanScore = response_desc['meanScore']
            averageScore = response_desc['averageScore']
            # printa os dados 
            i += 1 
            print(">>>>>>>> ",i)
            print('id',id)
            print('title', title)
            print('episodes', episodes)
            print('description', description)
            print('genres', genres)
            print('studios', studios)
            print('popularity', popularity)
            print('meanScore', meanScore)
            print('averageScore', averageScore)
            print('_'*100)
            # monta na lista
            lista_animes.append({"id": i, "title": title, "episodes": episodes, "description": description, "genres": genres, "studios": studios,
                                 "popularity": popularity, "meanScore": meanScore, "averageScore": averageScore, "studios": studios})
        # caso aconteça algum erro
        except:
            # caso erros
            erros += 1
            print(traceback.format_exc())
            print(f" erros: {erros}")
            print("espera 1 segundos")
            sleep(1)
            # retorna os dados prontos
    return lista_animes


# função principal
if __name__ == "__main__":
    # pega os dados da função que faz os trabalho
    dados = request_animes()
    print("Feito")
    # salvo no json
    with open("AnimesDesc.json", "w") as json_file:
        # faz virar objeto do python
        json.dump(dados, json_file, indent=4)

# feito por Mateus Rodrigues
