---PEP8 formatted, mypy type tested---

cards.py includes class definitions of:
	a Card 	[with rank and suit]
	a Deck	[with a list of cards]
	a Player	[with a name and hand]
	a Game	[with a Deck, players, discard pile, hand size, and winner]
methods include: 
	dealing to players the handsize number of cards
	drawing 1 card from a deck
	discarding a card to a discard
	playing a card [effects of playing a card not implemented]
	sorting a deck
	shuffling a deck
	more
MAIN DEMONSTRATES VARIOUS EXAMPLES AND USAGES



blackjack.py uses the cards classes to make a class:
	Blackjack which contains: 
		a Game with Dealer added
		a current player
methods include:
	hitme [ draw a card to a player's visible hand ]
	stay   [ move to next player without taking card]
	dealer stay [ end round ]
	display results [ show all hands, calculate winners/losers]
MAIN demonstates a  running game
	use command: python blackjack.py x <-x is the number of players
	type hit/stay/exit to take cards and move through players
	type y/n at end of round to continue indefinitely 
		[discard pile is reshuffled if empty, card counting is possible]
	
	


