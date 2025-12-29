import random


# Card class with rank, suit, and value
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.assign_value()

    def assign_value(self):
        """Assign numeric value based on card rank"""
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        elif self.rank == "Ace":
            return 11  # Ace can be 11 or 1, handled in hand calculation
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Deck class with cards list
class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        """Create a standard 52-card deck"""
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

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)


# Player class with name, bank, cards, and bet
class Player:
    def __init__(self, name, bank=1000):
        self.name = name
        self.bank = bank
        self.cards = []
        self.bet = 0

    def place_bet(self, amount):
        """Place a bet if player has enough funds"""
        if amount > self.bank:
            print(f"Insufficient funds! You only have ${self.bank}")
            return False
        self.bet = amount
        self.bank -= amount
        return True

    def win(self):
        """Player wins - add winnings to bank"""
        winnings = self.bet * 2
        self.bank += winnings
        print(f"\n{self.name} wins ${winnings}!")
        self.bet = 0

    def lose(self):
        """Player loses - bet is already deducted"""
        print(f"\n{self.name} loses ${self.bet}!")
        self.bet = 0

    def push(self):
        """Tie - return bet to player"""
        self.bank += self.bet
        print(f"\nPush! Bet of ${self.bet} returned.")
        self.bet = 0

    def add_card(self, card):
        """Add a card to player's hand"""
        self.cards.append(card)

    def clear_hand(self):
        """Clear player's cards"""
        self.cards = []

    def __str__(self):
        return f"{self.name} - Bank: ${self.bank}"


# Dealer class with cards
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        self.deck = Deck()

    def deal(self):
        """Deal one card from the deck"""
        return self.deck.cards.pop()


# Helper functions
def calculate_hand_value(cards):
    """Calculate the value of a hand, handling Aces"""
    value = sum(card.value for card in cards)
    aces = sum(1 for card in cards if card.rank == "Ace")

    # Adjust for Aces if hand value is over 21
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def display_hands(player, dealer, hide_dealer_card=True):
    """Display player and dealer hands"""
    print("\n" + "=" * 50)
    print(f"\n{dealer.name}'s Hand:")
    if hide_dealer_card and len(dealer.cards) > 1:
        print(f"  {dealer.cards[0]}")
        print("  [Hidden Card]")
    else:
        for card in dealer.cards:
            print(f"  {card}")
        print(f"Total: {calculate_hand_value(dealer.cards)}")

    print(f"\n{player.name}'s Hand:")
    for card in player.cards:
        print(f"  {card}")
    print(f"Total: {calculate_hand_value(player.cards)}")
    print("=" * 50)


def player_turn(player, dealer):
    """Handle player's turn - hit or stand"""
    while True:
        player_value = calculate_hand_value(player.cards)

        if player_value > 21:
            print("\nBUST! You went over 21!")
            return False

        choice = input("\nWould you like to [H]it or [S]tand? ").lower()

        if choice == "h":
            player.add_card(dealer.deal())
            print(f"\nYou drew: {player.cards[-1]}")
            print(f"Your hand total: {calculate_hand_value(player.cards)}")
        elif choice == "s":
            print(f"\n{player.name} stands with {player_value}")
            return True
        else:
            print("Invalid choice. Please enter 'H' or 'S'.")


def dealer_turn(dealer):
    """Handle dealer's turn - must hit until 17 or higher"""
    print(f"\n{dealer.name}'s turn...")

    while calculate_hand_value(dealer.cards) < 17:
        dealer.add_card(dealer.deal())
        print(f"{dealer.name} draws: {dealer.cards[-1]}")
        print(f"{dealer.name}'s total: {calculate_hand_value(dealer.cards)}")

    dealer_value = calculate_hand_value(dealer.cards)

    if dealer_value > 21:
        print(f"\n{dealer.name} BUSTS with {dealer_value}!")
        return False

    print(f"\n{dealer.name} stands with {dealer_value}")
    return True


def determine_winner(player, dealer):
    """Determine the winner and handle payouts"""
    player_value = calculate_hand_value(player.cards)
    dealer_value = calculate_hand_value(dealer.cards)

    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print(f"{player.name}: {player_value}")
    print(f"{dealer.name}: {dealer_value}")
    print("=" * 50)

    if player_value > dealer_value:
        player.win()
    elif player_value < dealer_value:
        player.lose()
    else:
        player.push()


def play_blackjack():
    """Main game loop"""
    print("\n" + "=" * 50)
    print("WELCOME TO BLACKJACK!")
    print("=" * 50)

    player_name = input("\nEnter your name: ")
    player = Player(player_name)
    dealer = Dealer()  # Dealer has deck

    while True:
        # Check if player has money
        if player.bank <= 0:
            print("\n" + "=" * 50)
            print("You're out of money! Game Over.")
            print("=" * 50)
            break

        print(f"\n{player}")

        # Place bet
        while True:
            try:
                bet_amount = int(input(f"\nPlace your bet (or 0 to quit): $"))
                if bet_amount == 0:
                    print("\nThanks for playing!")
                    print(f"Final bank: ${player.bank}")
                    return
                if player.place_bet(bet_amount):
                    break
            except ValueError:
                print("Please enter a valid number.")

        # Clear hands
        player.clear_hand()
        dealer.clear_hand()

        # Deal initial cards
        player.add_card(dealer.deal())
        dealer.add_card(dealer.deal())
        player.add_card(dealer.deal())
        dealer.add_card(dealer.deal())

        # Display initial hands
        display_hands(player, dealer, hide_dealer_card=True)

        # Check for player blackjack
        if calculate_hand_value(player.cards) == 21:
            print(f"\n🎉 BLACKJACK! {player.name} wins! 🎉")
            player.bank += int(player.bet * 2.5)  # Blackjack pays 3:2
            player.bet = 0
            continue

        # Player's turn
        if not player_turn(player, dealer):
            player.lose()
            continue

        # Dealer's turn
        display_hands(player, dealer, hide_dealer_card=False)

        if not dealer_turn(dealer):
            player.win()
            continue

        # Determine winner
        determine_winner(player, dealer)

        # Ask to play again
        play_again = input("\nPlay another round? [Y/N]: ").lower()
        if play_again != "y":
            print("\nThanks for playing!")
            print(f"Final bank: ${player.bank}")
            break


# Run the game
if __name__ == "__main__":
    play_blackjack()
