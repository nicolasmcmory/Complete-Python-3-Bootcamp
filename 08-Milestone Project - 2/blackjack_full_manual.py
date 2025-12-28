from __future__ import annotations
import random


class Deck:

    class Card:
        def __init__(self, suit, rank):
            """Card has suit, rank and value instance variables."""
            self.suit = suit
            self.rank = rank
            self.value = self.__assign_value(rank)
            self.hidden = True

        def __assign_value(self, rank):
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
            if self.hidden:
                return "Face-down card."
            return f"{self.rank} of {self.suit}."

        def show_card(self):
            """Change card visibility to visible (face up)"""
            self.hidden = False
            return self

        def hide_card(self):
            """Change card visibility to hidden (face down)"""
            self.hidden = True
            return self

    def __init__(self):
        """Deck has cards as instance variables and build_deck(),
        shuffle(), len() as instance methods."""
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
                card = Deck.Card(suit, rank)
                self.cards.append(card)

    def __len__(self):
        """Returns lenght of deck."""
        return len(self.cards)

    def __str__(self):
        deck_str = f"{len(self.cards)} cards in deck:\n"
        deck_str += "\n".join([f"{card}" for card in self.cards])
        return deck_str

    def shuffle(self) -> bool:
        """Shuffles deck."""
        random.shuffle(self.cards)
        return True

    def add_cards(self, cards: Deck.Card | list[Deck.Card]) -> None:
        """Accepts lists of cards and individual cards as long as they are cards"""
        try:
            # Is cards a list
            if isinstance(cards, list):

                # Is cards list empty and are all the items cards (part of Card class)
                if cards and all(isinstance(card, Deck.Card) for card in cards):
                    for card in cards:
                        card.hide_card()
                    self.cards.extend(cards)

            # cards is not a list, is the card a Card
            elif isinstance(cards, Deck.Card):
                card = cards
                card.hide_card()
                self.cards.append(card)

        # Handle exceptions
        except Exception as e:
            print(e)

    def remove_card(self) -> Deck.Card:
        """Removes a card from end of deck (back), deck is face down. Visibility is hidden."""
        return self.cards.pop()


class Player:
    def __init__(self, name: str = "Player", cash: int = 1000):
        """Player has a name as 'name' (defaults to 'Player'), cards in hand as 'hand', cash in hand as 'cash', current bet on table as 'bet'."""
        self.name = name
        self.hand = []
        self.cash = cash
        self.bet = 0

    # Utility method
    def __return_cards(self) -> list[Deck.Card]:
        """Return player cards, emptying hand. Visibility is not managed here, it is managed at the deck level as cards hould be hidden by default in a deck."""
        cards = []
        while self.hand:
            cards.append(self.hand.pop())
        return cards

    def receive_card(self, card: Deck.Card) -> None:
        """Receive 1 card in hand. Visibility is managed by dealer."""
        self.hand.append(card)

    def place_bet(self, bet) -> int:
        """Place bet as long as funds are sufficient. Dealer uses method but as a mathc bet."""
        if bet <= self.cash:
            self.bet = bet
            return bet
        print("Insufficient funds, no bet placed.")
        return bet

    def win(self, winnings: int) -> list[Deck.Card]:
        """Winning implies that player receives their bet with matched bet from other players including the dealer and clears player's bet. Empties hand and returns cards from the hand."""
        self.cash += winnings
        print(f"{self.name} wins!")

        # Reveal cards
        for card in self.hand:
            card.show_card()
        print(self)

        # Reset bet
        self.bet = 0

        return self.__return_cards()

    def lose(self) -> list[Deck.Card]:
        """Loosing implies removing the bet from the players cash. Empties hand and returns cards from the hand."""
        self.cash -= self.bet
        self.bet = 0
        print(f"{self.name} looses!")
        print(self)
        return self.__return_cards()

    def tie(self) -> list[Deck.Card]:
        """Tie implies the player returns their cards and the bet is reset. No other changes."""
        self.bet = 0
        print(self)
        return self.__return_cards()

    def __str__(self):
        """Player name, cash, bet, hand."""
        return f"Player: {self.name}\n\nCash: {self.cash}\n\nBet: {self.bet}\n\nHand:{'\n'.join(str(card) for card in self.hand)}\n"


class Dealer(Player):

    def __init__(self):
        super().__init__("Dealer")
        self.deck = Dealer.new_deck()

    @staticmethod
    def new_deck() -> Deck:
        """Instantiates a new deck."""
        return Deck()

    def deal(self, hidden: bool = False) -> Deck.Card:
        """Hands out a card from deck."""
        card = self.deck.remove_card()
        if hidden:
            card.hide_card()
        else:
            card.show_card()
        return card

    def return_cards_to_deck(self, cards) -> str:
        """Dealer takes cards from players and returns them to deck. Returns the deck string dunder."""
        self.deck.add_cards(cards)
        self.deck.shuffle()
        return f"{self.deck}"


class Game:

    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.winner = self.dealer
        self.looser = self.player
        self.playing = True

    def __sum_cards(self, player: Player | Dealer) -> int:
        """Check hand to see if over 21, account for Ace's dual value (1 or 11)."""
        total_sum = sum(card.value for card in player.hand)
        aces = sum(1 for card in player.hand if card.rank == "Ace")

        # Check if over 21 and adjust aces as needed until under 21
        while total_sum > 21 and aces > 0:
            total_sum -= 10
            aces -= 1

        return total_sum

    def __handle_winnings(self) -> None:
        """Handle rad return and bets to cash."""
        # Organise card return according to winning logic
        winnings = self.dealer.bet + self.player.bet
        cards = self.looser.lose()
        cards.extend(self.winner.win(winnings))

        # Return cards to deck
        self.dealer.return_cards_to_deck(cards)

    def __handle_tie(self) -> None:
        """Handle logic for tie between players."""
        print("It's a tie!")
        cards = self.player.tie()
        cards.extend(self.dealer.tie())

        # Return cards to deck
        self.dealer.return_cards_to_deck(cards)

    def __bust_check(self) -> None:
        """Check for bust (over 21) win, loose or tie."""

        # Get player card sums
        player_sum = self.__sum_cards(self.player)
        dealer_sum = self.__sum_cards(self.dealer)

        # Tie, close round
        if player_sum == 21 and dealer_sum == 21:
            self.__handle_tie()
            return

        # Player bust, dealer wins
        if player_sum > 21:
            self.winner = self.dealer
            self.looser = self.player
            self.__handle_winnings()
            return

        # Dealer bust, player wins
        if dealer_sum > 21:
            self.winner = self.player
            self.looser = self.dealer
            self.__handle_winnings()
            return

    def __first_deal(self) -> None:
        """First handout of cards at game start, after win, tie or loose."""
        # Hand out to player and dealer
        for card in range(2):
            self.player.receive_card(self.dealer.deal())
        # Hand out to dealer, one face up and one face down
        self.dealer.receive_card(self.dealer.deal(True))
        self.dealer.receive_card(self.dealer.deal(False))

    def __handle_hit(self) -> None:
        """Handle logic for player hit move."""
        self.player.receive_card(self.dealer.deal())
        self.__bust_check()

    def __handle_stand(self) -> None:
        """Handle logic for player stand move."""
        player_sum = self.__sum_cards(self.player)
        dealer_sum = self.__sum_cards(self.dealer)

        # Reveal dealers hand
        print("Dealer's hand: ")
        for card in self.dealer.hand:
            card.show_card()
        # Dealer is receiving
        while self.__sum_cards(self.dealer) < 17:
            self.dealer.receive_card(self.dealer.deal())
            self.__bust_check()

        # Player card sum is closer to 21, player wins
        if 21 - player_sum < 21 - dealer_sum:
            self.winner = self.player
            self.looser = self.dealer
            self.__handle_winnings()
            return
        # Dealer card sum is closer to 21
        self.winner = self.dealer
        self.looser = self.player
        self.__handle_winnings()

    def __handle_bets(self):
        """Place bets, handles logic."""
        bet = 0
        while bet == 0:
            bet = int(input("Place bet: "))

        # Player is receiving, dealer does not
        self.player.place_bet(bet)
        self.dealer.place_bet(bet)  # Dealer matches bet

    def __continue_game(self, choice: str) -> None:
        choice = choice.lower()
        if choice == "y":
            print("Ok let's continue!")
            self.playing = True
        elif choice == "n":
            print("Thanks for playing!")
            self.playing = False

    def start_game(self):
        """Start game."""
        # Get user name and start game
        self.player.name = input("Welcome to balckjack!\nEnter your name: ")

        while self.playing:
            # Want to continue playing and place bets
            if self.player.bet == 0:
                self.__handle_bets()
                print("=" * 50)

            # Dealing out the first hand
            if len(self.player.hand) == 0 and len(self.dealer.hand) == 0:
                self.__first_deal()
                print(self.player)
                print("=" * 50)
                print(self.dealer)

            # Player's move
            hit_or_stand = input(" Hit (h) or Stand (s)?: ")
            if hit_or_stand == "h":
                self.__handle_hit()
                print(self.player)
                print("=" * 50)
                print(self.dealer)
            elif hit_or_stand == "s":
                self.__handle_stand()
                print(self.player)
                print("=" * 50)
                print(self.dealer)
                self.__continue_game(input("Continue playing? Y/N"))

    def get_player(self):
        """Return player."""
        return self.player

    def get_dealer(self):
        """Return dealer."""
        return self.dealer


if __name__ == "__main__":
    game = Game()
    game.start_game()
