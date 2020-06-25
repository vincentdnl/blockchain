"""
Ce TP a pour but de comprendre les mécanismes de preuve de travail (Proof of Work, PoW) et de preuve d'enjeu (Proof of Stake, PoS).

_Pour simplifier l'exemple, nous ne créeront pas de connexion réseau. On passera directement des références d'objets._

Le but de l'exercice sera d'instancier 3 nodes, bob, alice et jack de la classe `Node` que nous allons implémenter.

_Pour cet exercice, le choix du langage est libre._

Chaque noeud possède un attribut `name` qui sera une chaine de caractère le définissant. Cet attribut n'entre pas dans le minage. Il nous permettra juste de repérer facilement quel noeud fait quoi.

Chaque noeud connait les autres noeuds, il possède comme attribut `other_nodes` qui est la liste des autres noeuds. On aimerait pouvoir connaître la liste des noeuds connus par un noeud spécifique via une methode `display_known_nodes` qui devra afficher quel noeuds lui sont connu (par exemple: "je suis bob et je connais: alice, jack).

Chaque noeud possède un attribut `blockchain` qui est une liste (Array) de Blocs (a créer, similaire à l'exemple montré précédemment en introduction). On aimerait que le noeud ait une methode `initialize_blockchain()` permettant d'ajouter d'initialiser le noeud avec une chaine de blocs

Les noeuds que l'on définit sont des noeuds mineurs. On peut leur ajouter des datas via une methode `add_data` (dans un attribut `data_for_next_block`) et déclencher le minage d'un bloc via la methode `start_mining`.

#### Proof of Work

La règle du jeu est la suivante, on va modifier la classe `Block` de manière à lui ajouter un attribut `nonce`. Ce nonce sera initialisé à la création du block et aura une valeur entière.
De la même manière que pour les autres attributs du block, nous allons modifier la méthode `hash()` afin que celle-ci ajoute le contenu du nonce au hash résultant.
Quand la méthode `start_mining` du node sera appelée, le node commencera à essayer de créer des blocs de la manière suivante:

* On choisit un incrément qui commence à 0
* On crée un block de manière à inclure cette valeur comme étant l'attribut "nonce" du bloc
Attention, il faut bien penser à ajouter le `last_block` de la blockchain courante du noeud à la création du noeud !
* Si le bloc hash du bloc résultant commence par `000`, on le considère comme valide et on le garde.
* Si le bloc ne commence pas par `000`, il n'est pas valide, on incrémente l'incrément et on continue.

Dans la pratique, chaque machine hébergant un noeud de minage a une puissance différente et le minage d'un bloc met aux alentours de 10 minutes !
Nous n'irons pas jusqu'à ajouter de la concurrence entre les noeuds de minage (cela peut être fait, facultativement à titre d'entraînement)
Dans le cas d'un bloc valide nous ajouterons juste le block à notre blockchain et appeleront la méthode `add_block` des autres noeuds en leur passant le nouveau bloc.
Cette methode `add_block` vérifiera que le hash commence bien par 000 avant de l'ajouter à leur blockchain

A la fin de l'exercice, on aimerait séquentiellement :

* créer 3 noeuds, bob, alice et jack.
* faire en sorte que chaque noeud connaisse les deux autres.
* initialiser leur blockchaine à une blockchaine de 3 blocs (ces blocs n'ont pas été minés, ils ne suivront donc pas la règle).
* bob sera le noeud mineur, on lui ajoute les données à miner pour le prochain bloc et on lance le start le minage
* on vérifie qu'à la fin du minage, bob, alice et jack ont bien 4 blocs dans leur blockchain. Le dernier bloc est identique pour chaque participant et a été créé par la même personne et contient bien les mêmes données. Le dernier bloc ayant été miné, devrait avoir un hash qui commence par `000`.

#### Proof of Stake

_Pour cette partie, il est conseillé de recréer une classe Node afin de ne pas tout mélanger..._

Pour la partie proof of stake, nous allons ajouter un attribut `tokens`, qui sera une liste d'entiers. Chaque entier représentera un jeton simplifié.

On distribuera les jetons comme suit : bob aura les jetons 1, 2, 3 et 4 (bob est très riche). alice aura les jetons 5 et 6, jack aura le jeton 7.

La règle du jeu est la suivante. Les règles du jeu seront différentes cette fois-ci:

* chaque participant regarde le hash du dernier bloc et en convertissant les trois dernier caractère en entier (hex vers int)
* Ce chiffre permettra de déterminer qui est le numéro gagnant, en utilisant ce numéro modulo le nombre de jetons par exemple.
* le participant qui possède le jeton ayant le bon numéro crée le bloc et le dispatch aux autres de manière similaire à ce qui a été fait dans la partie Proof of Work.

A la fin de l'exercice, on aimerait séquentiellement :

* créer 3 noeuds, bob, alice et jack.
* faire en sorte que chaque noeud connaisse les deux autres.
* initialiser leur blockchaine à une blockchaine de 3 blocs (ces blocs n'ont pas été minés, ils ne suivront donc pas la règle).
* ajouter des données à chaque noeud.
* chaque participant regarde s'il a gagné la lotterie du PoS.
* on vérifie qu'à la fin du minage, bob, alice et jack ont bien 4 blocs dans leur blockchain. Le dernier bloc est identique pour chaque participant et a été créé par la même personne et contient bien les mêmes données.
"""

import hashlib
from datetime import datetime
from typing import List


class Node:
    def __init__(self, name: str):
        self.blockchain = []
        self.name = name
        self.other_nodes = []
        self.data_for_next_block = ""

    def add_nodes(self, nodes_list: List["Node"]):
        self.other_nodes += nodes_list

    def display_known_nodes(self):
        print(f"Je suis {self.name} et je connais: {', '.join([node.name for node in self.other_nodes])}")

    def initialize_blockchain(self, blockchain: List["Block"]):
        self.blockchain = blockchain

    def add_data(self, data: str):
        self.data_for_next_block = data

    def start_mining(self):
        timestamp = datetime.timestamp(datetime.now())
        for i in range(1, 10000):
            new_block = Block(
                timestamp,
                self.data_for_next_block,
                last_block=self.blockchain[-1],
                nonce=i
            )
            if new_block.hash.startswith("000"):
                print(f"Je suis {self.name} et j'ai trouvé un nouveau bloc avec le hash suivant: {new_block.hash}")
                self.add_block(new_block)
                for other_node in self.other_nodes:
                    other_node.add_block(new_block)
                return new_block

    def add_block(self, new_block):
        if new_block.hash.startswith("000"):
            self.blockchain.append(new_block)


class NodePoS:
    def __init__(self, name: str, tokens: List[int]):
        self.blockchain = []
        self.name = name
        self.other_nodes = []
        self.data_for_next_block = ""
        self.tokens = tokens

    def add_nodes(self, nodes_list: List["NodePoS"]):
        self.other_nodes += nodes_list

    def display_known_nodes(self):
        print(f"Je suis {self.name} et je connais: {', '.join([node.name for node in self.other_nodes])}")

    def initialize_blockchain(self, blockchain: List["Block"]):
        self.blockchain = blockchain

    def add_data(self, data: str):
        self.data_for_next_block = data

    def start_mining(self):
        timestamp = datetime.timestamp(datetime.now())

        last_three_numbers_str = self.blockchain[-1].hash[-3:]
        last_three_numbers = int(last_three_numbers_str, 16)
        winning_ticket_number = last_three_numbers % 7

        if winning_ticket_number in self.tokens:
            new_block = Block(
                timestamp,
                self.data_for_next_block,
                last_block=self.blockchain[-1],
            )
            print(
                f"Je suis {self.name} et j'ai trouvé un nouveau bloc avec le hash suivant: {new_block.hash}")
            self.add_block(new_block)
            for other_node in self.other_nodes:
                other_node.add_block(new_block)
            return new_block

    def add_block(self, new_block):
        if new_block.hash.startswith("000"):
            self.blockchain.append(new_block)


class Block:
    def __init__(self, timestamp: float, data: str, last_block: "Block" = None, nonce: int = 0):
        self.timestamp = timestamp
        self.data = data
        self.last_block = last_block
        self.nonce = nonce

    @property
    def hash(self):
        m = hashlib.sha256()
        m.update(bytes(str(self.timestamp), "utf-8"))
        m.update(bytes(self.data, "utf-8"))
        if self.last_block:
            m.update(bytes(self.last_block.hash, "utf-8"))
        m.update(bytes(str(self.nonce), "utf-8"))
        return m.hexdigest()


def test_get_other_nodes():
    bob = Node("bob")
    alice = Node("alice")
    jack = Node("jack")

    bob.add_nodes([alice, jack])

    assert bob.other_nodes == [alice, jack]
    bob.display_known_nodes()


def test_start_mining():
    bob = Node("bob")
    alice = Node("alice")
    jack = Node("jack")

    block0 = Block(
        datetime.timestamp(datetime.now()),
        "block0",
    )
    block1 = Block(
        datetime.timestamp(datetime.now()),
        "block1",
        last_block=block0
    )
    block2 = Block(
        datetime.timestamp(datetime.now()),
        "block2",
        last_block=block1
    )

    bob.add_nodes([alice, jack])

    bob.initialize_blockchain([block0, block1, block2])
    alice.initialize_blockchain([block0, block1, block2])
    jack.initialize_blockchain([block0, block1, block2])

    assert bob.blockchain == [block0, block1, block2]

    bob.add_data("données du nouveau bloc qui sera miné")

    new_block = bob.start_mining()

    assert new_block.hash.startswith("000")
    assert bob.blockchain[-1] == new_block
    assert alice.blockchain[-1] == new_block
    assert jack.blockchain[-1] == new_block


def test_cant_add_invalid_block():
    bob = Node("bob")

    block0 = Block(
        datetime.timestamp(datetime.now()),
        "block0",
    )

    bob.add_block(block0)

    assert bob.blockchain == []


def test_start_mining_pos():
    bob = NodePoS("bob", [0, 1, 2, 3])
    alice = NodePoS("alice", [4, 5])
    jack = NodePoS("jack", [6])

    block0 = Block(
        datetime.timestamp(datetime.now()),
        "block0",
    )
    block1 = Block(
        datetime.timestamp(datetime.now()),
        "block1",
        last_block=block0
    )
    block2 = Block(
        datetime.timestamp(datetime.now()),
        "block2",
        last_block=block1
    )

    bob.add_nodes([alice, jack])
    alice.add_nodes([bob, jack])
    jack.add_nodes([alice, bob])

    bob.initialize_blockchain([block0, block1, block2])
    alice.initialize_blockchain([block0, block1, block2])
    jack.initialize_blockchain([block0, block1, block2])

    bob.add_data("données du nouveau bloc qui sera miné par bob")
    alice.add_data("données du nouveau bloc qui sera miné par alice")
    jack.add_data("données du nouveau bloc qui sera miné par jack")

    bob.start_mining()
    alice.start_mining()
    jack.start_mining()

    assert bob.blockchain[-1] == alice.blockchain[-1] == jack.blockchain[-1]
