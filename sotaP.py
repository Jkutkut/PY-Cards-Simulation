import random
from Classes.colorOutput import *
from Classes.deck import Deck
from Classes.card import Card, SpanishCard
from Classes.cardPlayer import CardPlayer
from Classes.deck import Deck

class SotaP:
    def __init__(self, nPlayers) -> None:
        if not isinstance(nPlayers, int) or nPlayers < 1:
            raise Exception("Number of players invalid")
        
        self._players = [] # Create player list
        for i in range(nPlayers):
            self.getPlayers().append(sotaP_player(f"Player{i+1}", i))

        deck = Deck(SpanishCard)

        # Give all cards to the players
        index = 0
        while len(deck.getStack()) > 0: # While there're cards left to give
            self.getPlayers()[index].takeCard(deck.takeCard()) # Give card to player
            index = (index + 1) % nPlayers # Select next player


        self._tableStack = []
        # self.scoreBoard = []
        self.gameStats = {
            "scoreBoard": [],
            "iAmThefastest": [0 for _ in range(nPlayers)]
        }


    
    # ########## GETTERS ##########
    
    def getPlayers(self) -> list:
        '''Returns a list with the players in the game'''
        return self._players


    def printPlayers(self):
        '''Prints the current status of the players'''
        for i in range(len(self.getPlayers())):
            print(self.getPlayers()[i])

    def getTableStack(self):
        '''Return a list of all the cards on the "table".'''
        return self._tableStack


    # ########## SETTERS ##########

    def giveTableCardsTo(self, playerIndex):
        if not isinstance(playerIndex, int) or playerIndex < 0 or playerIndex >= len(self.getPlayers()):
            raise Exception("The index of the player is not valid")
        while len(self.getTableStack()) > 0: # Give all cards to the player
            self.getPlayers()[playerIndex].takeCard(self.getTableStack().pop())
    

    # ########## GAME ##########
    def game(self):
        SPECIALCARDS = [10, 11, 12, 1]
        stack = self.getTableStack()
        players = self.getPlayers()
        playersLen = len(players)
        
        turnIndex = 0
        cardsMissingByPlayer = 0
        playerIndex = None

        while playersLen > 1: # While at least 2 players playing

            if len(players[turnIndex].getHand()) == 0: # If empty hand, remove player
                if playerIndex != None: # If cardsMissing on
                    cardsMissingByPlayer = -1
                    if playerIndex > turnIndex:
                        playerIndex = playerIndex - 1

                # yield f"  - {colorOutput('RED', players[turnIndex].getName())} has lost"
                self.gameStats["scoreBoard"].append(players.pop(turnIndex))
                playersLen = playersLen - 1
                turnIndex = turnIndex % playersLen
                continue

            currentCard = players[turnIndex].useCard()
            stack.append(currentCard)
            # yield f"{colorOutput('LIGHTBLUE', players[turnIndex].getName())} uses {colorOutput('YELLOW', currentCard)} => {len(players[turnIndex].getHand())} left"

            if currentCard.getRank() == stack[len(stack) - 2].getRank() and len(stack) > 1: # If card with same number twice
                fastest = [0, players[0].getReactionTime()] 
                for i in range(1, len(players)): # Get fastest reaction time
                    reaction = players[i].getReactionTime()
                    if reaction < fastest[1]:
                        fastest = [i, reaction]
                self.giveTableCardsTo(fastest[0]) # Give cards to the fastest
                pI = players[fastest[0]].index
                self.gameStats["iAmThefastest"][pI] = self.gameStats["iAmThefastest"][pI] + 1
                
                # Reset cardMissionPlayer
                playerIndex = None
                # yield(f"  - {colorOutput('GREEN', 'SAME')}: {players[fastest[0]].getName()} is the fastest and takes the stack.")

            elif currentCard.getRank() in SPECIALCARDS: # If special card
                extra = SPECIALCARDS.index(currentCard.getRank()) + 1
                
                cardsMissingByPlayer = extra
                playerIndex = turnIndex
                
                turnIndex = (turnIndex + 1) % playersLen # Go to the next player
                # yield f"  - {colorOutput('MAGENTA', 'Special card')} => {players[playerIndex].getName()} gets {extra} cards from {players[turnIndex].getName()}."


            if playerIndex == None:
                turnIndex = (turnIndex + 1) % playersLen # Go to the next player
            else:
                cardsMissingByPlayer = cardsMissingByPlayer - 1
                if cardsMissingByPlayer == -1:
                    self.giveTableCardsTo(playerIndex) # Give cards to the fastest
                    # yield f"  - {players[playerIndex].getName()} takes the stack"
                    playerIndex = None
        
        self.gameStats["scoreBoard"].append(players.pop()) # Add winner

        yield 0 # Ended without problem



class sotaP_player(CardPlayer):
    playerReactionTime = [200, 225, 250]

    def __init__(self, name, index) -> None:
        self._reactionTime = self.playerReactionTime[1] # Peak reactionTime
        self.index = index
        super().__init__(name=name)

    # ########## GETTERS ##########

    def getPeakReactionTime(self):
        '''Returns peak reaction time in milliseconds.'''
        return self._reactionTime
    
    def getReactionTime(self):
        '''Get a reaction time from the player. This value is pheudo-random in milliseconds.'''
        return self._reactionTime + random.randint(0, 90)

    # ########## SETTERS ##########
    