from random import choice, shuffle, randint
from typing import List, Union

suits = ['heart', 'club', 'diamond', 'spade']
suit_order = {'spade': 3, 'diamond': 2, 'club': 1, 'heart': 0}
ranks = [str(i) for i in range(2, 11)] + list("JQKA")


class Card:
    def __init__(self, rank: str = "", suit: str = "") -> None:
        '''
        a Card has a rank and a suit
        randomize, if parameters are not set
        '''
        self.rank = rank if rank != "" else choice(ranks)
        self.suit = suit if suit != "" else choice(suits)

    def __str__(self) -> str:
        '''
        string of Card is the rank and the suit (first letter) uppercased
        '''
        return self.rank + self.suit[0].upper()


class Deck:
    def __init__(self, pile=[]) -> None:
        '''
        a Deck is a list of Cards
        if the specific cards to include in the deck are not specified
        generate the standard 52 card 4 suit deck
        '''
        if not pile:
            self.cards = [Card(rank=r, suit=s) for r in ranks for s in suits]
        else:
            self.cards = pile

    def __len__(self) -> int:
        '''
        the len of a Deck is the len of the list of cards
        '''
        return len(self.cards)

    def __getitem__(self, pos: int) -> Card:
        '''
        Deck[x] is the list of cards[x]
        '''
        return self.cards[pos]

    def __str__(self) -> str:
        '''
        the string of a Deck is the str of the cards in order,
        separated by spaces
        '''
        s = ""
        for c in self.cards:
            s += str(c) + " "
        return s

    def state(self) -> str:
        '''
        state returns a string of reading how many cards are left in it
        '''
        return "Deck has "+str(len(self))+" cards.\n"

    def shuffle(self, n: int = 1) -> None:
        '''
        shuffle uses random.shuffle n times on the deck
        '''
        for _ in range(n):
            shuffle(self.cards)

    def draw(self) -> Card:
        '''
        take a card from the 'top' of the deck
        popping the last item in the list off
        returning it
        '''
        return self.cards.pop()

    def peek(self) -> Card:
        '''
        return the top card of the deck, without removing
        last in list of cards
        '''
        return self[-1]

    def put(self, x: Card) -> None:
        '''
        put appends a card to the top of the Deck
        '''
        self.cards.append(x)


class Player():
    def __init__(self, n: str) -> None:
        '''
        a Player has a num string e.g. name
        and a hand, list of Cards
        [TODO: make a hand a Deck?]
        '''
        self.num = n
        self.hand: List[Card] = []

    def state(self) -> str:
        '''
        state returns a string of the form:
        PLAYER 1 has 5 cards.
        '''
        return self.num+" has "+str(len(self.hand))+" cards.\n"

    def __str__(self) -> str:
        '''
        string of a Player is their 'name' or num
        '''
        return self.num

    def draw(self, c: Card) -> None:
        '''
        draw, takes a specified card into the hand
        '''
        self.hand.append(c)

    def discard(self, c) -> Card:
        '''
        discard removes the Card from the hand list
        and returns the removed card
        '''
        self.hand.remove(c)
        return c

    def play(self, n: int) -> Union[Card, int]:
        '''
        returns the nth card in hand, if that card exists in hand
        -1 indicates failure to retrieve card
        '''
        if 0 > n or n >= len(self.hand):
            return -1
        c = self.hand[n]
        if c in self.hand:
            self.hand.remove(c)
            print(c)
            return c
        else:
            return -1

    def get_hand(self) -> str:
        '''
        returns a strings of each card in the hand
        '''
        handstr = ""
        for c in self.hand:
            handstr += str(c) + " "
        return handstr

    def cheat(self, c: Card) -> None:
        '''
        cheat is just a wrapper for draw,
        allowing drawing the card desired
        '''
        self.draw(c)


class Game:
    def __init__(self, players: int = 2, handsize: int = 5, deal=True) -> None:
        '''
        A Game has:
        players: a list of players of length players
        turn: a Player representing the current player
        deck: a Deck of 52 cards
        discard: a list of cards or Deck for cards removed from game
        handsize: set by handsize parameter
        winner: int for winning player
        the deck is shuffled and players dealt to IF deal==True
        '''
        self.players = [Player("Player "+str(i)) for i in range(1, players+1)]
        self.turn = choice(self.players)
        self.deck = Deck()
        self.discard: Union[List[Card], Deck] = []
        self.handsize = handsize
        self.deck.shuffle(2)
        self.winner = -1
        if deal:
            self.deal()

    def deal(self) -> None:
        '''
        deal draws a cards from deck and gives to players
        based on handsize and number of players
        '''
        for _ in range(self.handsize):
            for p in self.players:
                self.draw2player(p)

    def draw2player(self, p: Player) -> None:
        '''
        draw2player is the Game level draw mechanic
        draw top card from Deck, draw that card TO the player
        if deck is ever empty, shuffle discard into deck and shuffle
        '''
        if not self.deck.cards:
            self.discard_2_deck()
            print("Deck empty, discard shuffled in")
            self.deck.shuffle(2)
        p.draw(self.deck.draw())

    def next_player(self) -> None:
        '''
        move turn's pointer from turn Player to the next Player in players
        '''
        now = self.players.index(self.turn) + 1
        self.turn = self.players[(now) % (len(self.players))]

    def dis_card(self, x: Card) -> None:
        '''
        2 ways to handle discarding, move card to discard
        making the discard into a Deck once 1 card has been discarded
        '''
        if isinstance(self.discard, list):
            self.discard.append(x)
            self.discard = Deck(pile=self.discard)
        else:
            self.discard.put(x)

    def state(self) -> str:
        '''
        the state displayer for a Game:
        generates a string of all players, number of cards in deck
        and displays which player's turn it is
        '''
        playerstr = ""
        for p in self.players:
            playerstr += p.state()
        full = self.deck.state() + "There are "
        full += str(len(self.players))+" players. \nIt is "
        full += str(self.turn)+"'s turn.\n" + playerstr
        return full

    def __str__(self) -> str:
        '''
        the string of a game is the state string
        '''
        return self.state()

    def play(self, n: int) -> Union[Card, str]:
        '''
        play wraps Player's play. returns the nth Card of turn's hand
        if that Card is not error -1 return it, discard it, move to next player
        return 'try again' if error -1
        '''
        tmp = self.turn.play(n)
        if isinstance(tmp, Card):
            self.next_player()
            self.dis_card(tmp)
            return tmp
        else:
            return "try again"

    def discard_2_deck(self) -> None:
        '''
        moves all cards in discard pile to deck
        discard is reset to empty
        '''
        if isinstance(self.discard, Deck):
            dc = self.discard.cards
        else:
            dc = self.discard
        self.deck = Deck(self.deck.cards + dc)
        self.discard = []

    def discard_all_hands(self) -> None:
        '''
        discards all players' cards and dis_cards them to the discard
        '''
        for p in self.players:
            for c in reversed(p.hand):
                c = p.discard(c)
                self.dis_card(c)

    def sort_deck(self) -> None:
        '''
        orders the Deck into sorted order by highcard function's valuation
        '''
        self.deck = Deck(pile=sorted(self.deck.cards, key=highcard))


def highcard(card: Card) -> int:
    '''
    ranks cards by rank and suit with suit_order values:
    Ace of Spades   = 12 * 4 + 3 = 51
    Ten of Spades   =  8 * 4 + 3 = 35
    Ace of Diamonds = 12 * 4 + 2 = 50
    Ten of Clubs    =  8 * 4 + 1 = 33
    Ace of Hearts   = 12 * 4 + 0 = 48
    '''
    rankt = ranks.index(card.rank)
    return rankt * len(suits) + suit_order[card.suit]


if __name__ == "__main__":
    x = Game(players=5, handsize=2)
    while True:
        print(x)
        print(x.turn.get_hand())
        y = input("enter the number of the card you want to play, 1-" +
                  str(len(x.turn.hand))+"\n")
        if y == "exit":
            break
        played = x.play(int(y)-1)
        print("===== "+str(played)+" =====")
        print()

    print(x.deck)
    print(x.discard)

    x.discard_2_deck()
    print(x.deck)
    x.sort_deck()
    print(x.deck)
    print()
    x.discard_all_hands()
    print(x.deck)
    print(x.discard)

    x.discard_2_deck()
    print(x.deck)
    print(x.discard)

    x.sort_deck()
    print(x.deck)
