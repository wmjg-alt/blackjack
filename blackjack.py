from cards import Game, Player, Deck, Card
from typing import List
import time
import sys

BJ_value_map = {"A": 11,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "J": 10,
                "Q": 10,
                "K": 10}


def hand_value(hand: List[Card]) -> int:
    '''
    Calculates the blackjack value of a hand
    with a special case for handling the duality of Aces: 11 -> 1
    '''
    tot: int = 0
    ranks = [c.rank for c in hand]
    for r in ranks:
        tot += BJ_value_map[r]
    if tot > 21 and "A" in ranks:
        tot = tot - 10
    return tot


class Blackjack:

    def __init__(self, n: int) -> None:
        '''
        A blackjack class contains a Card Game where the starting handsize is 2
        A dealer is added to the game as another player
        '''
        self.game = Game(players=n, handsize=2, deal=False)
        self.game.turn = self.game.players[0]
        self.game.players.append(Player("=Dealer="))
        self.game.deal()
        print(self.game.state())
        self.status("'s TURN", self.game.turn)

    def status(self, mess: str, name: Player) -> None:
        '''
        a printing method for outputting the latest event
        showing Dealer's face up card,
        and displaying the current player's hand & value
        '''
        print(name, mess)
        t: Player = self.game.turn
        if "Deal" not in str(t):
            print("Dealer shows:", self.game.players[-1].hand[-1])
        print(str(self.game.turn)+":    ", t.get_hand())
        print("\t", "Value:", hand_value(t.hand))
        print()

    def hitme(self) -> None:
        '''
        the hitme function deals a card to the current player [turn]
        and handles output for Busts [value > 21]
        '''
        self.game.draw2player(self.game.turn)
        self.status("HITS -> "+str(self.game.turn.hand[-1]), self.game.turn)
        if hand_value(self.game.turn.hand) > 21:
            print('-----BUST-----')
            time.sleep(1.5)
            if 'Deal' not in self.game.turn.num:
                self.stay()

    def stay(self) -> None:
        '''
        the stay function advances the turn to the next player
        '''
        last_player = self.game.turn
        self.game.next_player()
        self.status("STAYS", last_player)

    def dealer_stay(self) -> None:
        '''
        dealer_stay handles the end of a game,
        when the dealer's functionality resolves a stay or a bust
        '''
        self.status("STAYS, end", self.game.turn)
        self.display_all_values()

    def display_all_values(self):
        '''
        method for displaying the results at game end
        displays all players' hand values and whether they Won/Lost/Push/Bust
        '''
        print('------Done------')
        d = self.game.players[-1]
        dealer_v = hand_value(d.hand)
        print(str(d) + ": " + d.get_hand() + "\t-> " + str(dealer_v))
        for p in self.game.players[:-1]:
            v = hand_value(p.hand)
            stat = str(p) + ": " + p.get_hand() + "\t-> " + str(v)
            if v > 21:
                stat += "  BUST"
            elif v > dealer_v or dealer_v > 21:
                stat += "  WINR"
            elif v == dealer_v:
                stat += "  PUSH"
            else:
                stat += "  LOSE"
            print(stat)
        print()


if __name__ == "__main__":
    x = Blackjack(n=int(sys.argv[1]))
    flag = True
    while flag:
        if "Deal" not in x.game.turn.num:
            command = input("Hit or stay?\n")
            if 'hit' in command.lower():
                x.hitme()
            elif 'stay' in command.lower():
                x.stay()
            elif 'exit' in command.lower():
                flag = False
        else:
            time.sleep(1.5)
            if hand_value(x.game.turn.hand) > 16:
                x.dealer_stay()
                again = input('Another round? y/n\n')
                if again.lower() == 'y':
                    x.game.discard_all_hands()
                    x.game.deal()
                    x.game.next_player()
                    print(x.game)
                    x.status("'s TURN", x.game.turn)
                else:
                    x.game.state()
                    flag = False
            else:
                x.hitme()
