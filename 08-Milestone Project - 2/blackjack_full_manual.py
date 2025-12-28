import random


class Player:
    def __init__(self, name: str = "Player", cash: int = 1000):
        """Player has a name as 'name' (defaults to 'Player'), cards in hand as 'hand', cash in hand as 'cash', current bet on table as 'bet'."""
        self.name = name
        self.hand = []
        self.cash = cash
        self.bet = 0

    def receive_card(self, card):
        """Receive 1 card in hand."""
        self.hand.append(card)

    def __return_cards(self) -> list:
        """Return player cards, emptying hand."""
        cards = []
        while self.hand:
            cards.append(self.hand.pop())
        return cards

    def place_bet(self, bet):
        """Place bet as long as funds are sufficient."""
        if bet <= self.cash:
            self.bet = bet
            return True
        return False

    def win(self, winnings: int):
        """Winning implies that player receives their bet with matched bet from other players including the dealer and clears player's bet. Empties hand and returns cards from the hand."""
        self.cash += winnings
        self.bet = 0
        return self.__return_cards()

    def loose(self):
        """Loosing implies removing the bet from the players cash. Empties hand and returns cards from the hand."""
        self.cash -= self.bet
        return self.__return_cards()

    def tie(self):
        """Tie implies the player returns their cards and the bet is reset. No other changes."""
        self.bet = 0
        return self.__return_cards()


class Dealer(Player):

    class Deck:

        class Card:
            def __init__(self, suit, rank):
                """Card has suit, rank and value instance variables."""
                self.suit = suit
                self.rank = rank
                self.value = self.assign_value(rank)

            def assign_value(self, rank):
                """Assigns value to a card based on common values for blackjack."""
                values_by_rank = {
                    "2": 2,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6": 6,
                    "7": 7,
                    "8": 8,
                    "9": 9,
                    "10": 10,
                    "Jack": 10,
                    "Queen": 10,
                    "King": 10,
                    "Ace": 11,
                }
                return values_by_rank[rank]

            def __str__(self):
                return f"{self.rank} of {self.suit}"

        def __init__(self):
            """Deck has cards as instance variables and build_deck(), shuffle(), len() as instance methods."""
            self.cards = []
            self.build_deck()
            self.shuffle()

        def build_deck(self):
            """Builds a deck from common features."""
            suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
            ranks = [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
                "Ace",
            ]
            # Build deck
            for suit in suits:
                for rank in ranks:
                    card = Dealer.Deck.Card(suit, rank)
                    self.cards.append(card)

        def shuffle(self):
            """Shuffles deck."""
            random.shuffle(self.cards)
            return True

        def remove_card(self):
            """Removes a card from end of deck (back), deck is face down."""
            return self.cards.pop()

        def add_cards(self, cards) -> list:
            """Accepts lists of cards and individual cards as long as they are cards"""
            try:
                # List of cards
                if type(cards) == list and type(cards[0]) == Dealer.Deck.Card:
                    return self.cards.extend(cards)

                # Individual card
                if type(cards) == Dealer.Deck.Card:
                    return self.cards.append(cards)

            except Exception as e:
                print(e)

        def __len__(self):
            """Returns lenght of deck."""
            return len(self.cards)

        def __str__(self):
            deck_str = f"{len(self.cards)} cards in deck:\n"
            deck_str += "\n".join([f"{card}" for card in self.cards])
            return deck_str

    def __init__(self):
        super().__init__("Dealer")
        self.deck = Dealer.new_deck()

    @staticmethod
    def new_deck():
        """Instantiates a new deck."""
        deck = Dealer.Deck()
        print(deck)
        return Dealer.Deck()

    def deal(self):
        """Hands out a card from deck."""
        return self.deck.remove_card()

    def return_cards(self, cards):
        """Dealer takes cards from players and returns them to deck. Returns the deck string dunder."""
        self.deck.add_cards(cards)
        self.deck.shuffle()
        return f"{self.deck}"


class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.dealer = Dealer()

    def first_deal(self):
        """First handout of cards at game start, after win, tie or loose."""
        

    def compare_hands(self):
        """Check for bust (over 21) win, loose or tie."""
        pass

    def handle_deal(self):
        """Handle deal"""

    def handle_stand(self):
        """Handle logic for player stand move."""
        pass

    def handle_hit(self):
        """Handle logic for player hit move."""
        pass

    def handle_tie(self):
        """Handle logic for tie between players."""
        pass

    def start_game(self):
        """Start game."""
        
        self.first_deal()
