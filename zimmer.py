from peewee import *
import os
from playhouse.shortcuts import model_to_dict

arq = "Magic.db"
db = SqliteDatabase(arq)


'''
- Tipo de Carta
- Carta
- Grimório
- Cemitério
- Exilio
- Campo de batalha
- Jogador (mão, vida, contadores)
- Etapa
- Formato
- Jogo

'''


class BaseModel(Model):
    class Meta():
        database = db


class TipoDeCarta(BaseModel):
    nome = CharField()
    subtipo = CharField()

    def __str__(self):
        return self.nome + " - " + self.subtipo


class Carta(BaseModel):
    nome = CharField()
    desc = CharField()
    tipo_de_carta = ForeignKeyField(TipoDeCarta)
    custo = CharField(null=True)
    raridade = CharField()
    ataque = IntegerField(null=True)
    defesa = IntegerField(null=True)

    def __str__(self):
        resultado = "Nome: " + self.nome + "\n"
        resultado += "Desc: " + self.desc + "\n"
        resultado += "Tipo: " + str(self.tipo_de_carta) + "\n"
        resultado += "Custo: " + self.desc + "\n"
        resultado += "Raridade: " + self.desc + "\n"
        resultado += "Ataque: " + str(self.ataque) + "\n"
        resultado += "Defesa: " + str(self.defesa) + "\n"

        return resultado


# O peewee não permite que uma tabela tenha somente chaves primárias ou estrangeiras, por isso os campos 'nome'!
class Grimorio(BaseModel):
    nome = CharField()
    cartas = ManyToManyField(Carta)

    def __str__(self):
        resultado = ""
        for carta in self.cartas:
            resultado += str(carta) + "\n"

        return resultado


class Cemiterio(BaseModel):
    nome = CharField()
    cartas = ManyToManyField(Carta)

    def __str__(self):
        resultado = ""
        for carta in self.cartas:
            resultado += str(carta) + "\n"

        return resultado

class Exilio(BaseModel):
    nome = CharField()
    cartas = ManyToManyField(Carta)

    def __str__(self):
        resultado = ""
        for carta in self.cartas:
            resultado += str(carta) + "\n"

        return resultado

class CampoDeBatalha(BaseModel):
    nome = CharField()
    cartas = ManyToManyField(Carta)

    def __str__(self):
        resultado = ""
        for carta in self.cartas:
            resultado += str(carta) + "\n"

        return resultado

class Jogador(BaseModel):
    nome = CharField()
    vida = IntegerField()
    grimorio = ForeignKeyField(Grimorio)
    cemiterio = ForeignKeyField(Cemiterio)
    exilio = ForeignKeyField(Exilio)
    campo_de_batalha = ForeignKeyField(CampoDeBatalha)

    def __str__(self):
        resultado = "Nome: " + self.nome + "\n"
        resultado += "Vida: " + str(self.vida) +"\n\n"
        resultado += "Grimório:\n"
        resultado += str(self.grimorio)
        resultado += "------------------------------------\n\n"
        resultado += "Cemitério:\n"
        resultado += str(self.cemiterio)
        resultado += "------------------------------------\n\n"
        resultado += "Campo de Batalha:\n"
        resultado += str(self.campo_de_batalha)
        resultado += "------------------------------------\n\n"

        return resultado

class Turno(BaseModel):
    jogador = ForeignKeyField(Jogador)
    etapa = CharField()

    def __str__(self):
        return self.etapa + " de " + self.jogador.nome + "\n"


class Formato(BaseModel):
    nome = CharField()
    numero_cartas = IntegerField()
    desc = CharField()

    def __str__(self):
        resultado = "Nome: " + self.nome + "\n"
        resultado += "Nº de cartas: " + str(self.numero_cartas) + "\n"
        resultado += "Descrição: " + self.desc + "\n"

        return resultado


class Jogo(BaseModel):
    jogadores = ManyToManyField(Jogador)
    turno = ForeignKeyField(Turno)
    formato = ForeignKeyField(Formato)

    def __str__(self):
        resultado = "Formato:\n" + str(self.formato)
        resultado += "------------------------------------\n\n"
        resultado += "Turno:\n" + str(self.turno)
        resultado += "------------------------------------\n\n"
        for jogador in self.jogadores:
            resultado += str(jogador)

        return resultado

if __name__ == '__main__':
    if os.path.exists(arq):
        os.remove(arq)

    db.connect()
    db.create_tables([
        TipoDeCarta,
        Carta,
        Grimorio,
        Grimorio.cartas.get_through_model(),
        Cemiterio,
        Cemiterio.cartas.get_through_model(),
        Exilio,
        Exilio.cartas.get_through_model(),
        CampoDeBatalha,
        CampoDeBatalha.cartas.get_through_model(),
        Jogador,
        Turno,
        Formato,
        Jogo,
        Jogo.jogadores.get_through_model()
    ])

    formato = Formato.create(
        nome="Modern",
        numero_cartas=60,
        desc="Jogo normal, regras básicas.")
    Formatolist = list(map(model_to_dict, Formato.select()))

    terreno_montanha = TipoDeCarta.create(nome="Terreno básico", subtipo="Montanha")
    TipoDeCartalist = list(map(model_to_dict, TipoDeCarta.select()))

    criatura_lobo = TipoDeCarta.create(nome="Criatura", subtipo="Lobo")
    criatura_humano = TipoDeCarta.create(nome="Criatura", subtipo="Humano guerreiro")

    encantamento_aura = TipoDeCarta.create(nome="Encantamento", subtipo="Aura")
    artefato_veiculo = TipoDeCarta.create(nome="Artefato", subtipo="Veículo")
    instant_machado = TipoDeCarta.create(nome="Mágica instantanea", subtipo="Machado de Lava")

    carta1 = Carta.create(
        nome="Montanha",
        desc="Molde a vida como quiser.",
        tipo_de_carta=terreno_montanha,
        raridade="comum"
    )
    Cartalist = list(map(model_to_dict, Carta.select()))

    carta2 = Carta.create(
        nome="Cerberus",
        desc="A morte está sempre ao seu lado.",
        tipo_de_carta=criatura_lobo,
        custo="3(preta)",
        raridade="incomum",
        ataque=3,
        defesa=3
    )

    carta3 = Carta.create(
        nome="Assas divinas",
        desc="Seja livre como um passaro.",
        tipo_de_carta=encantamento_aura,
        custo="4(branca)",
        raridade="comum",
        ataque=1,
        defesa=1
    )

    carta4 = Carta.create(
        nome="Aeroesquife",
        desc="Bons ventos.",
        tipo_de_carta=artefato_veiculo,
        custo="2()",
        raridade="raro",
        ataque=4,
        defesa=2
    )
    carta5 = Carta.create(
        nome="Bola de Fogo",
        desc="O fogo arde mais durante o dia.",
        tipo_de_carta=instant_machado,
        custo="4(vermelha)",
        raridade="comum",
        ataque=4,
        defesa=0
    )

    grimorio_j1 = Grimorio.create(nome="Grimório do Jogador1")
    grimorio_j1.cartas.add([carta1, carta2, carta3, carta4, carta5])
    Grimoriolist = list(map(model_to_dict, Grimorio.select()))

    cemiterio_j1 = Cemiterio.create(nome="Cemitério do Jogador1")
    cemiterio_j1.cartas.add([carta2, carta4])
    Cemiteriolist = list(map(model_to_dict, Cemiterio.select()))

    exilio_j1 = Exilio.create(nome="Exílio do Jogador1")
    exilio_j1.cartas.add([carta5])
    Exiliolist = list(map(model_to_dict, Exilio.select()))

    campo_j1 = CampoDeBatalha.create(nome="Campo de Batalha do Jogador1")
    CampoDeBatalhalist = list(map(model_to_dict, CampoDeBatalha.select()))

    jogador1 = Jogador.create(
        nome="Zimmer",
        vida=20,
        grimorio=grimorio_j1,
        cemiterio=cemiterio_j1,
        exilio=exilio_j1,
        campo_de_batalha=campo_j1
    )
    Jogadorlist = list(map(model_to_dict, Jogador.select()))

    turno = Turno.create(jogador=jogador1, etapa="Primeira Etapa Principal")
    Tunolist = list(map(model_to_dict, Turno.select()))
    
    jogo = Jogo.create(turno=turno, formato=formato)
    jogo.jogadores.add([jogador1])
    Jogolist = list(map(model_to_dict, Jogo.select()))

    print(jogo)

def lista():
    programacao = [Formatolist,TipoDeCartalist,Cartalist,Grimoriolist,Cemiteriolist,Exiliolist,CampoDeBatalhalist,Jogadorlist,Tunolist,Jogolist]
    return programacao    
