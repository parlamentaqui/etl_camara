from mongoengine import *

class Deputy(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    photo_url = StringField()
    initial_legislature_id = IntField(required=True)
    final_legislature_id = IntField()
    initial_legislature_year = IntField(required=True)
    final_legislature_year = IntField()
    last_activity_date = DateTimeField()
    full_name = StringField()
    sex = StringField()
    email = StringField()
    birth_date = DateTimeField()
    death_date = DateTimeField()
    federative_unity = StringField()
    party = StringField()
    instagram_username = StringField()
    twitter_username = StringField()
    facebook_username = StringField()
    twitter_id = StringField()
    website = StringField()
    office_number = StringField()
    office_name = StringField()
    office_premise = StringField()
    office_floor = StringField()
    office_phone = StringField()
    office_email = StringField()

    def to_json(self):
        return{
            'id':self.id,
            'name':self.name,
            'photo_url':self.photo_url,
            'initial_legislature_id':self.initial_legislature_id,
            'final_legislature_id':self.final_legislature_id,
            'initial_legislature_year':self.initial_legislature_year,
            'final_legislature_year':self.final_legislature_year,
            'last_activity_date':self.last_activity_date,
            'full_name':self.full_name,
            'sex':self.sex,
            'email':self.email,
            'birth_date':self.birth_date,
            'death_date':self.death_date,
            'federative_unity':self.federative_unity,
            'party':self.party,
            'instagram_username':self.instagram_username,
            'twitter_username':self.twitter_username,
            'facebook_username':self.facebook_username,
            'twitter_id':self.twitter_id,
            'website':self.website,
            'office_number':self.office_number,
            'office_name':self.office_name,
            'office_premise':self.office_premise,
            'office_floor':self.office_floor,
            'office_phone':self.office_phone,
            'office_email':self.office_email
        }


class Parlamentary_vote(Document):
    unique_id = StringField(primary_key=True)
    id_voting = StringField(required=True)
    id_deputy = IntField(required=True)
    deputy_name = StringField()
    party = StringField()
    federative_unity = StringField()
    id_legislature = StringField()
    date_time_vote = DateTimeField()
    vote = StringField()
    voted_accordingly = StringField()
    proposition_id = StringField()
    proposition_description = StringField()
    proposition_title = StringField()
    proposition_link = StringField()
        
    def to_json(self):
        return{
            'unique_id': self.unique_id,
            'id_voting': self.id_voting,
            'id_deputy': self.id_deputy,
            'deputy_name': self.deputy_name,
            'party': self.party,
            'federative_unity': self.federative_unity,
            'id_legislature': self.id_legislature,
            'date_time_vote': self.date_time_vote,
            'vote': self.vote,
            'voted_accordingly': self.voted_accordingly,
            'proposition_id': self.proposition_id,
            'proposition_description': self.proposition_description,
            'proposition_title': self.proposition_title,
            'proposition_link': self.proposition_link
        }

class Proposicao(Document):
    proposicao_id = IntField(primary_key=True)
    id_deputado_autor = IntField(required=True)
    uri = StringField()
    descricao_tipo = StringField()
    ementa = StringField(required=True)
    ementa_detalhada = StringField()
    keywords = StringField()
    data_apresentacao = DateTimeField()
    urlAutor = StringField()
    tipoAutor = StringField()
    nome_autor = StringField()
    sigla_UF_autor = StringField()
    tema_proposicao = StringField()
    sigla_orgao = StringField() # Comeca aqui as informacoes do objeto de status
    data_proposicao = DateTimeField() 
    descricao_situacao = StringField()
    despacho = StringField()
    uri_relator = StringField()
    sigla_tipo = StringField()
    cod_tipo = IntField()
    numero = IntField()
    ano = IntField()
    image_url = StringField()
    image_id = StringField()
        
    def to_json(self):
        return{
            'proposicao_id': self.proposicao_id,
            'id_deputado_autor': self.id_deputado_autor,
            'uri': self.uri,
            'descricao_tipo': self.descricao_tipo,
            'ementa': self.ementa,
            'ementa_detalhada': self.ementa_detalhada,
            'keywords': self.keywords,
            'urlAutor': self.urlAutor,
            'tipoAutor': self.tipoAutor,
            'nome_autor': self.nome_autor,
            'sigla_UF_autor': self.sigla_UF_autor,
            'tema_proposicao': self.tema_proposicao,
            'sigla_orgao': self.sigla_orgao,
            'data_proposicao': self.data_proposicao,
            'descricao_situacao': self.descricao_situacao,
            'despacho': self.despacho,
            'uri_relator': self.uri_relator,
            'sigla_tipo' : self.sigla_tipo,
            'cod_tipo' : self.cod_tipo,
            'numero' : self.numero,
            'ano' : self.ano,
            'image_url' : self.image_url,
            'image_id' : self.image_id
        }

class Expenses(Document):
    deputy_id = IntField(required=True)
    year = IntField(required=True)
    month = IntField(required=True)
    expenses_type = StringField()
    document_type = StringField()
    document_date = DateTimeField()
    document_num = IntField(primary_key=True)
    document_value = IntField()
    document_url = StringField()
    supplier_name = StringField()
    supplier_cnpj_cpf = StringField()
    liquid_value = IntField()
    glosa_value = IntField()
    refund_num = StringField()
    batch_cod = IntField()
    tranche = IntField()

    def to_json(self):
        return{
            'deputy_id':self.deputy_id,
            'year':self.year,
            'month':self.month,
            'expenses_type':self.expenses_type,
            'document_type':self.document_type,
            'document_date':self.document_date,
            'document_num':self.document_num,
            'document_value':self.document_value,
            'document_url':self.document_url,
            'supplier_name':self.supplier_name,
            'supplier_cnpj_cpf':self.supplier_cnpj_cpf,
            'liquid_value':self.liquid_value,
            'glosa_value':self.glosa_value,
            'refund_num':self.refund_num,
            'batch_cod':self.batch_cod,
            'tranche':self.tranche
        }
