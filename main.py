from war.game import Deck

if __name__ == '__main__':
    d = Deck()

    a, b = d.start_game()

    print(a.cards)

    print(a.cards.serve_card())
    print(a.cards.serve_card())
    print(a.cards.serve_card())

    print(a.cards)
