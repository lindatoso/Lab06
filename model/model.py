from database import DB_connect
from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        connessione=get_connection() # creo connessione con database
        cursore=connessione.cursor() # creo cursore per scorrere tra le istanze delle tabelle
        query=f"SELECT * FROM STRUMENTO" # scrivo query per ottenere tutti gli strumenti dalla tabella strumenti
        cursore.execute(query) # eseguo la query

        strumenti=[] # creo lista vuota per contenere gli strumenti

        for riga in cursore: # per ogni elemento del cursore
            nuovo=Strumento(riga[0], riga[1], riga[2], riga[3], riga[4]) # creo uno strumento con i vari campi
            strumenti.append(nuovo) # aggiungo lo strumento alla lista

        cursore.close() # chiudo cursore e connettore per terminare il collegamento
        connessione.close()

        return strumenti # restituisco al controller la lista con gli strumenti
        # TODO

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        if tipo is None or tipo.strip()=="": # se il textfield è vuoto scateno ValueError
            raise ValueError("Campo vuoto")

        connessione = get_connection() # come sopra
        cursore = connessione.cursor()
        query = f"""SELECT * 
                    FROM STRUMENTO
                    WHERE TIPO=%s""" # query per selezionare solo strumenti di un certo tipo (indicato con %s)
        cursore.execute(query, (tipo,)) # passo all'esecuzione il parametro tipo come tupla

        strumenti = [] # come sopra

        for riga in cursore:
            nuovo = Strumento(riga[0], riga[1], riga[2], riga[3], riga[4])
            strumenti.append(nuovo)

        cursore.close()
        connessione.close()

        if not strumenti: # se la lista strumenti è vuota, scateno ValueError
            raise ValueError(f"Nessuno strumento trovato per il tipo {tipo}")

        return strumenti
        # TODO
