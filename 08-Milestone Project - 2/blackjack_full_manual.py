import random


class Card:
    def __init__(self, suit, rank):
        """Card has suit, rank and value instance variables."""
        self.suit = suit
        self.rank = rank
        self.value = self.assign_value(rank)

    def assign_value(self, rank):
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


# %% Deck class
class Deck:
    def __init__(self):
        """Deck has cards as instance variables and build_deck(), shuffle(), len() as instance methods."""
        self.cards = []
        self.build_deck()
        self.shuffle()

    def build_deck(self):
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
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)
        return True

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        deck_str = f"{len(self.cards)} cards in deck:\n"
        deck_str += "\n".join([f"{card}" for card in self.cards])
        return deck_str


# %% Deck class
class Player:
    def __init__(self, name: str, cash: int = 1000):
        self.name = name
        self.cards = []
        self.cash = cash
        self.bet = 0
        self.hit()
        self.stand()
        self.win()
        self.loose()
        self.tie()


class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        self.deck = self.new_deck()

    def deal(self):
        pass

    def new_deck():
        deck = Deck()
        print(deck)
        return Deck()


class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.dealer = Dealer()

    def first_deal(self):
        """First handout of cards at game start, after win, tie or loose."""
        pass

    def handle_deal(self):
        """Handle deal"""

    def compare_hands(self):
        """Check for bust (over 21) win, loose or tie."""
        pass

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
