import json
import requests
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import *
from operator import attrgetter

api = Blueprint('api', __name__, url_prefix='/api')

#Retornar o json dos deputados pra aparecer na home
@api.route('/deputies-home')
def deputados():
    s_list = sorted(Deputy.objects, reverse=True, key=attrgetter('last_activity_date'))
    all_deputies = []
    for deputy in s_list:
        depu_json= deputy.to_json()
        all_deputies.append(depu_json)
    return jsonify(all_deputies[:6])

# Rota que retorna um deputado em específico usando um id
@api.route('/deputado_especifico/<id>')
def ver_deputado(id):
    r = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id}")

    json_deputy = r.json()

    return json_deputy["dados"]

# Rota que retorna um json com todos os jsons de deputados ordenados por nome
@api.route('/deputies')
def index():
    full_json = []
    sorted_list = sorted(Deputy.objects, key=attrgetter('name'))

    for deputy in sorted_list:
        temp_json = deputy.to_json()
        full_json.append(temp_json)

    return jsonify(full_json)

# Rota que retorna o resultado de uma busca de acordo com os filtros no corpo da requsisçao POST
@api.route('/resultado', methods=['POST'])
def resultado():
    #recebemos um json do request com {nome, uf e partido}
    requested_json = request.get_json()
    name_filter = str.lower(requested_json["nome"])
    uf_filter = str.lower(requested_json["uf"])
    party_filter = str.lower(requested_json["partido"])

    # Cria uma lista vazia e preenche com os objetos salvos de Deputy
    all_deputies = []
    for item in Deputy.objects:
        all_deputies.append(item)
 

    # Filtra os resultados da pesquisa
    for deputy in Deputy.objects:
        if str.lower(deputy.name).find(name_filter) != -1 or name_filter == "":
            if str.lower(deputy.federative_unity) ==  uf_filter or uf_filter == "":
                if str.lower(deputy.party) == party_filter or party_filter == "":
                    continue
                else:
                    all_deputies.remove(deputy)
            else:
                all_deputies.remove(deputy)
        else:
            all_deputies.remove(deputy)

    # Ordena os deputados por nome
    sorted_list = sorted(all_deputies, key=attrgetter('name'))

    # Cria um json com todos os deputados encontrados e já ordenados
    full_json = []

    for deputy in sorted_list:
        temp_json = deputy.to_json()
        full_json.append(temp_json)

    # Retorna no formato JSON a lista de objetos full_json
    return jsonify(full_json)

@api.route('/deputies/<id>')
def profile(id):
    for profile in Deputy.objects:
      #Adicionar informacoes que estao comentadas
        if int(id) == int(profile.id):
            return profile.to_json()
        
    return {} 
        

@api.route('/federative_unities')
def federative_unities():
    r = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados')
    all_federative_unities_json = r.json()
    custom_federative_unities_json = []
    for federative_unity in all_federative_unities_json:
        federative_unity_temp = {}
        federative_unity_temp["uf"] = federative_unity["sigla"]
        federative_unity_temp["name"] = federative_unity["nome"]
        custom_federative_unities_json.append(federative_unity_temp)
    
    custom_federative_unities_json = sorted(custom_federative_unities_json,key=lambda k: k['name'])
    return jsonify(custom_federative_unities_json)


@api.route('/parties')
def parties():
    parties_list = []
    for deputy in Deputy.objects:
      #Adicionar informacoes que estao comentadas
        parties_list.append(deputy.party)
    used = set()
    unique = [x for x in parties_list if x not in used and (used.add(x) or True)]
    return jsonify(sorted(unique)) 
        

# Rota para apagar os todos os deputados do DB (USAR SOMENTE PARA TESTES) 
@api.route('/remover_deputados')
def apagar_deputados():
    Deputy.objects.all().delete()
    return "Deputados apagados com sucesso"


# Rota que popula no DB os dados dos deputados registrados nos dados abertos da câmara
@api.route('/atualizar_deputados')
def atualizar_deputados():
    r = requests.get(f'https://dadosabertos.camara.leg.br/arquivos/deputados/json/deputados.json')
    all_deputies_basic_json = r.json()
    filtered_list = filter(lambda deputado : deputado["idLegislaturaFinal"] == 56, all_deputies_basic_json["dados"])

    #criar uma lista com todos os deputados
    all_deputies = []

    #Iterar por todos os deputados que se encontram no basic json
    for item in filtered_list:
        all_deputies.append(create_deputy(item))  

    return jsonify(all_deputies)


def create_deputy(deputy_json):
    #Criar uma nova requisição desse deputado para pegar as informações específicas
    request_full_deputy_info = requests.get(deputy_json["uri"])
    real_json = request_full_deputy_info.json()["dados"]

    #2-criar uma lógica que popule corretamente as redes sociais 
    #3-verificar se o deputado já existe para não atualizar desnecessariamente 

    # Lógica que popula corretamente o ano inicial e final da legislatura
    request_initial_legistaure = requests.get(f'https://dadosabertos.camara.leg.br/api/v2/legislaturas/{deputy_json["idLegislaturaInicial"]}')
    initial_legislature_json = request_initial_legistaure.json()["dados"]

    request_final_legistaure = requests.get(f'https://dadosabertos.camara.leg.br/api/v2/legislaturas/{deputy_json["idLegislaturaFinal"]}')
    final_legislature_json = request_final_legistaure.json()["dados"]
   
    # Aqui se cria uma variavel que ira definir o ultimo status do deputado
    real_last_activity_date = real_json["ultimoStatus"]["data"]
    last_activity_date = str(real_last_activity_date)

    # Lógica para verificar se a informação de ultimo status está vazia ou não e corrigi-la para o formato correto
    if real_last_activity_date is None:
        last_activity_date = None

    elif len(real_last_activity_date) < 8:
        real_last_activity_date = None
        last_activity_date = None

    else:
        last_activity_date = last_activity_date[0:10]
        last_activity_date = datetime.strptime(last_activity_date, '%Y-%m-%d')

    # Popular a nova classe de acordo com as infos recebidas do objeto deputy_json
    new_deputy = Deputy(
        birth_date=datetime.strptime(str(real_json["dataNascimento"]), '%Y-%m-%d') if real_json["dataNascimento"] is not None else None,
        death_date= datetime.strptime(str(real_json["dataFalecimento"]), '%Y-%m-%d') if real_json["dataFalecimento"] is not None else None,
        email=real_json["ultimoStatus"]["email"],
        facebook_username=None,
        federative_unity=real_json["ufNascimento"],
        final_legislature_id=deputy_json["idLegislaturaFinal"],
        final_legislature_year=datetime.strptime(str(final_legislature_json["dataFim"]), '%Y-%m-%d').year,
        full_name=real_json["nomeCivil"],
        id=real_json["id"], 
        instagram_username=None,  
        initial_legislature_id=deputy_json["idLegislaturaInicial"],
        initial_legislature_year=datetime.strptime(str(initial_legislature_json["dataInicio"]), '%Y-%m-%d').year,
        last_activity_date=last_activity_date,
        name=real_json["ultimoStatus"]["nomeEleitoral"],
        party=real_json["ultimoStatus"]["siglaPartido"],
        photo_url=real_json["ultimoStatus"]["urlFoto"],
        sex=real_json["sexo"],
        twitter_username=None,
        ).save()

    return new_deputy.to_json(new_deputy)

# Rota que popula no DB os dados das votacoes dos deputados
@api.route('/atualizar_votos')
def atualizar_votos():
    #request para api da câmara que retorna todos os votos em projetos em ordem de data
    r = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro")
    # r = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio=2020-01-01&dataFim=2020-12-31&ordem=DESC&ordenarPor=dataHoraRegistro")
    all_votes_json = r.json()

    all_parlamentary_votes = []

    #para cada voto desse, encontrar os deputados responsáveis, quem votou ou não
    for vote in all_votes_json["dados"]:
        
        vote_uri = vote["uri"] + "/votos"
        r2 = requests.get(vote_uri)
        specific_vote_list = r2.json()["dados"]

        #caso a lista nao seja vazia, verificar e/ou popular esse voto no banco de dados
        if specific_vote_list:
            #pegar o json da proposição desse voto
            proposition_json = get_proposition_json_by_vote(vote)
            
            #para cada voto dentro da lista, atualizar o banco 
            for this_vote in specific_vote_list:
                deputy_json = this_vote["deputado_"]

                # Verificar se esse voto já foi populado/criado corretamente, caso nao tenha sido, criar um novo.
                need_create_vote = True
                for item in Parlamentary_vote.objects:
                    if (str(item.id_voting) is str(vote["id"])) and (int(item.id_deputy) is int(deputy_json["id"])):
                        need_create_vote = False
                        print('Não precisa criar o voto do : ' + deputy_json["nome"])
                        break
                        
                
                #passou da verificação e precisa criar um voto
                if need_create_vote:
                    vote_date = datetime.strptime(str(this_vote["dataRegistroVoto"]), '%Y-%m-%dT%H:%M:%S') if len(this_vote["dataRegistroVoto"]) > 5 else None

                    #lógica se votou de acordo com o partido:
                    voted_accordingly_party = voted_accordingly_party_method(this_vote["tipoVoto"], deputy_json["siglaPartido"], vote["uri"])

                    #Criar o novo voto parlamentar e salvar no banco com o métodos .save() 
                    new_vote = Parlamentary_vote(
                        id_voting = vote["id"],
                        id_deputy = deputy_json["id"],
                        deputy_name = deputy_json["nome"],
                        party = deputy_json["siglaPartido"],
                        federative_unity = deputy_json["siglaUf"],
                        id_legislature = str(deputy_json["idLegislatura"]),
                        date_time_vote = vote_date,
                        vote = this_vote["tipoVoto"],
                        voted_accordingly = voted_accordingly_party,
                        proposition_id = str(proposition_json["id"]),
                        proposition_description = proposition_json["ementa"],
                        proposition_title = proposition_json["descricaoTipo"],
                        proposition_link = proposition_json["urlInteiroTeor"]
                    )

                    all_parlamentary_votes.append(new_vote)

    all_parlamentary_votes_json = []
    for item in all_parlamentary_votes:
        item.save()
        all_parlamentary_votes_json.append(item.to_json())
    
    #esse return ta estranho, tem que ver o Parlamentary_vote.objects
    return jsonify(all_parlamentary_votes_json) 

def voted_accordingly_party_method(vote_type, party, vote_uri):
    orientation_uri = vote_uri + "/orientacoes"
    r = requests.get(orientation_uri)

    orientation_json = r.json()["dados"]

    #para todo json dentro, encontrar o partido desse deputado
    for item in orientation_json:
        deputy_party_lower = party.lower()
        item_party_lower = item["siglaPartidoBloco"].lower()

        if item_party_lower in deputy_party_lower:
            vote_type_lower = vote_type.lower()
            party_vote_type_lower = item["orientacaoVoto"].lower()
            if party_vote_type_lower in vote_type_lower:
                return "Sim" 

    #Essa função vai retornar Sim ou Não 
    return "Não"

def get_proposition_json_by_vote(vote_json):
    #Pegar qual proposição é de acordo com a votação
    r3 = requests.get(vote_json["uri"])
    proposition_vote_json = r3.json()["dados"]

    if proposition_vote_json["proposicoesAfetadas"]:
        #caso tenha uma proposição afetada, pegar o json dessa proposição
        r4 = requests.get(proposition_vote_json["proposicoesAfetadas"][0]["uri"])

        proposition_full_json = r4.json()["dados"]
        return proposition_full_json
    
    #caso nao encontre nenhuma proposição, criar um json temporario com os mesmos nomes do json utilizados na criação de elemntos do banco de dados
    temp_json = {
        'id':None,
        'ementa':None,
        'descricaoTipo':None,
        'urlInteiroTeor':None
    }
    
    return temp_json


@api.route('/deletar_votos')
def deletar_votos():
    Parlamentary_vote.objects.all().delete()

    return "Deletou todos os votos do banco de dados"

@api.route('/get_votes')
def get_votes():
    #printar todos os valores dos banco de dados
    all_parlamentary_votes = []

    for item in Parlamentary_vote.objects:
        all_parlamentary_votes.append(item.to_json()) 

    return jsonify(all_parlamentary_votes)