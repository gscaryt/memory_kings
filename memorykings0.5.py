import pyinputplus as pyip
import logging as log
import random, termcolor, pygame

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)

class GameState:
    def __init__(self):
        self.players_vector = []
        self.cards_vector = []

    def players_vector_gen(self, player_total):
        for _ in range(player_total + 1):
            self.players_vector.append(
                Player([[None, None], [None, None]], [None, None], [None, None], None)
            )

class Board:
    def __init__(self, WIDTH, HEIGHT):
        self.all_cards = [
            "QQQ",
            "rBB",
            "rRB",
            "rKB",
            "bBB",
            "bRB",
            "bKB",
            "rBW",
            "rRW",
            "rKW",
            "bBW",
            "bRW",
            "bKW",
            "yBB",
            "yRB",
            "yKB",
            "gBB",
            "gRB",
            "gKB",
            "yBW",
            "yRW",
            "yKW",
            "gBW",
            "gRW",
            "gKW",
            # Extra Cards (p = Purple, m = Brown)
            "pBB",
            "pRB",
            "pKB",
            "pBW",
            "pRW",
            "pKW",
            "mBB",
            "mRB",
            "mKB",
            "mBW",
            "mRW",
            "mKW",
        ]
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def slice_shuffle(self):
        self.deck = self.all_cards[: self.WIDTH * self.HEIGHT]
        random.shuffle(self.deck)
        log.debug(f"The Deck has been shuffled: {self.deck}")

class Player:
    'Contains values refering to the Pawns of a Player and the Player Score.'
    def __init__(self, coordinates, positions, previous_positions, color=None):
        self.coordinates = coordinates
        self.positions = positions
        self.previous_positions = previous_positions
        self.color = color
        self.score = 0

    def coordinates_to_position(self, WIDTH, pawn_index):
        self.positions[pawn_index] = WIDTH * (self.coordinates[pawn_index][1] - 1) + (
            self.coordinates[pawn_index][0] - 1
        )

    def record_positions(self):
        self.previous_positions = list(self.positions)

class Deck:
    'Contains values refering to each Card of the Deck.'
    def __init__(self, number, code, color, rank, back, token=None):
        self.number = number
        self.color = color
        self.rank = rank
        self.back = back
        self.code = code
        self.token = token

    def record_coordinates(self, WIDTH):
        self.coordinates = [(self.number % WIDTH) + 1, (self.number // WIDTH) + 1]

class Clock:
    def __init__(self, counter_turns, round_number):
        self.counter_turns = counter_turns
        self.round_number = round_number

    def counter_tick(self):
        self.counter_turns += 1

    def round_tick(self):
        self.round_number += 1

class Validate:
    def __init__(self):
        self.who_recruited = None
        self.is_finished = False

# MAIN GAME LOOP

def run():
    """Puts everything together in an infinite loop of fun."""
    print("Hello!")
    print("This is Memory Kings in Python 3.")
    print("Do you wish to start a game? (y/n)")
    while True:
        menu_choice = input()
        if menu_choice.lower() == "n":
            print("Well Ok then... Bye.")
            break
        elif menu_choice.lower() == "y":
            player_total = pyip.inputNum(
                "How many Players will be playing? [1-4]\n", min=1, max=4
            )
            WIDTH = 5
            HEIGHT = 5
            board = Board(WIDTH, HEIGHT)
            validate = Validate()
            clock = Clock(0, 0)
            board.slice_shuffle()
            game_state = GameState()
            game_state.players_vector_gen(player_total)
            setup_board(board, game_state.cards_vector, game_state.players_vector)
            while True:
                ### PYGAME ###
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        validate.is_finished = True
                ### PYGAME ###
                if validate.is_finished:
                    break
                else:
                    game_round(
                        board,
                        game_state.cards_vector,
                        game_state.players_vector,
                        clock,
                        validate,
                    )
            print("Thanks for playing Memory Kings.")
            print("The final score is:")
            print(f"Number of Rounds: {clock.round_number}")
            if game_state.players_vector[0].color != None:
                print(f"Counter King: {game_state.players_vector[0].score}/6 pairs.")
                print(f"Counter King moved up to the card {clock.counter_turns+1}.")
            for i in range(1, len(game_state.players_vector)):
                print(
                    f"Player {game_state.players_vector[i].color}: "
                    f"{game_state.players_vector[i].score}/6 pairs."
                )
            print("Do you wish to play again? (y/n)")
        else:
            print("That's not a valid option. Choose y to start, and n to leave.")

# COMPONENTS SETUP

def create_cards(board, deck, cards_vector):
    """ Shuffle the deck, creates and appends all the Card Objects to the cards_vector. """
    for i in range(len(deck)):
        t = deck[i][0]
        if t == "b":
            color = "Blue"
        elif t == "y":
            color = "Yellow"
        elif t == "r":
            color = "Red"
        elif t == "g":
            color = "Green"
        elif t == "p":
            color = "Magenta"
        elif t == "m":
            color = "Grey"
        else:
            color = ""
        t = deck[i][1]
        if t == "R":
            rank = "Rook"
        elif t == "B":
            rank = "Bishop"
        elif t == "K":
            rank = "Knight"
        elif t == "Q":
            rank = "Queen"
        t = deck[i][2]
        if t == "W":
            back = "White"
        else:
            back = "Black"
        cards_vector.append(Deck(i, deck[i], color, rank, back))
        cards_vector[i].record_coordinates(board.WIDTH)
        log.debug(
            f"create_cards() - Card {cards_vector[i].color} {cards_vector[i].rank}"
            f" with {cards_vector[i].back} back and code {cards_vector[i].code} created."
            f" Position {cards_vector[i].coordinates}"
        )

def create_players(players_vector):
    """
    Creates and appends all the Player Objects to the players_vector.\n
    If 2+ players, still creates the Counter King (Player[0]) but keeps\n
    all attributes None so it doesn't interfere with the game.
    """
    selected_colors = []
    if len(players_vector) == 2:
        players_vector[0].color = "Counter King"
    log.debug(
        f"create_players(): The Counter (player[0]) is set with color {players_vector[0].color}"
        f" on {[players_vector[0].coordinates[0]]} and {[players_vector[0].coordinates[0]]}"
    )
    for i in range(1, len(players_vector)):
        while True:
            choice = pyip.inputChoice(
                ["Orange", "Purple", "White", "Black"],
                prompt=f"What color does Player {i} wishes to play with?\n"
                f"[Options: Orange, Purple, White, Black]\n",
            )
            log.debug(
                f"create_players(): Color taken: {choice.title() in str(selected_colors)}"
            )
            if choice.title() in selected_colors:
                print(
                    f"{choice.title()} was already selected. Please, select a different color."
                )
                continue
            else:
                selected_colors.append(choice.title())
                log.debug(f"create_players(): selected_colors: {selected_colors}.")
                break
        players_vector[i].color = choice
        log.debug(
            f"create_players(): Player player[{i}] chose the color {players_vector[i].color}."
        )

def place_pawns(board, cards_vector, players_vector):
    """Takes input for the starting coordinates of the players' pawns and attributes the coordinates."""
    if len(players_vector) == 2:
        players_vector[0].coordinates = [[1, 1], [None, None]]
        players_vector[0].positions = [0, None]
        print(
            "This is a Solitaire game."
            " Your pawns must start on cards with the same back as the Counter King."
        )
        print(
            f"The Counter King will start on a card with {cards_vector[0].back} back."
        )
        print("")
    else:
        print(
            f"This is Multiplayer game with {len(players_vector)-1} Players."
            f" Your pawns must start on cards with White backs."
        )
        print("")
    for i in range(1, len(players_vector)):
        pawns = players_vector[i]
        print(
            f"Player {players_vector[i].color}, please enter the starting coordinates for your Pawns:"
        )
        while True:
            x = pyip.inputNum(f"Enter X (1-5) for your 1st Pawn: ", min=1, max=5)
            y = pyip.inputNum(f"Enter Y (1-5) for your 1st Pawn: ", min=1, max=5)
            if place_pawns_check(board, cards_vector, players_vector, x, y):
                break
        pawns.record_positions()
        pawns.coordinates[0] = [x, y]
        pawns.coordinates_to_position(board.WIDTH, 0)
        print_board(board, cards_vector, players_vector) # TERMINAL PLAY
        while True:
            x = pyip.inputNum(f"Enter X (1-5) for your 2nd Pawn: ", min=1, max=5)
            y = pyip.inputNum(f"Enter Y (1-5) for your 2nd Pawn: ", min=1, max=5)
            if place_pawns_check(board, cards_vector, players_vector, x, y):
                break
        pawns.record_positions()
        pawns.coordinates[1] = [x, y]
        pawns.coordinates_to_position(board.WIDTH, 1)
        print_board(board, cards_vector, players_vector) # TERMINAL PLAY
        log.debug(
            f"place_pawns() - {pawns.color} Player:"
            f" 1st Pawn: {pawns.coordinates[0]} Card |"
            f" 2nd Pawn: {pawns.coordinates[1]} Card"
        )
        continue

def setup_board(board, cards_vector, players_vector):
    create_players(players_vector)
    create_cards(board, board.deck, cards_vector)
    print_board(board, cards_vector, players_vector) # TERMINAL PLAY
    place_pawns(board, cards_vector, players_vector)
    queen_check(board, cards_vector, players_vector)

# GAME FLOW

def game_round(board, cards_vector, players_vector, clock, validate):
    clock.round_tick()
    print(f"Rounds: {clock.round_number} | Counter: {clock.counter_turns}")
    print(" ")
    log.debug(
        f"game_round() - Player {players_vector[0].color} score = {players_vector[0].score}"
    )
    for player_index in range(1, len(players_vector)):
        log.debug(
            f"game_round() - Player {players_vector[player_index].color}"
            f" score = {players_vector[player_index].score}"
        )
        player_turn(board, cards_vector, players_vector, player_index, clock, validate)
        if validate.is_finished:
            return
        counter_turn(board, cards_vector, players_vector, clock, validate)
        if validate.is_finished:
            break

def player_turn(board, cards_vector, players_vector, player_index, clock, validate):
    while True:
        player_move(board, cards_vector, players_vector, player_index)
        print_board(board, cards_vector, players_vector) # TERMINAL PLAY
        queen_check(board, cards_vector, players_vector)
        recruit_check(cards_vector, players_vector, validate)
        end_game_check(cards_vector, players_vector, clock, validate)
        if validate.is_finished:
            break
        elif validate.who_recruited == 0:
            counter_turn(board, cards_vector, players_vector, clock, validate)
            break
        elif validate.who_recruited == player_index:
            continue
        else:
            break
        end_game_check(cards_vector, players_vector, clock, validate)

def counter_turn(board, cards_vector, players_vector, clock, validate):
    while True:
        counter_move(board, players_vector)
        clock.counter_tick()
        print_board(board, cards_vector, players_vector) # TERMINAL PLAY
        recruit_check(cards_vector, players_vector, validate)
        end_game_check(cards_vector, players_vector, clock, validate)
        if validate.is_finished:
            break
        elif validate.who_recruited == 0:
            continue
        else:
            break
        end_game_check(cards_vector, players_vector, clock, validate)

# MOVEMENTS

def player_move(board, cards_vector, players_vector, player_index):
    """Calls for move_check(...) and the Player() methods\n
    record_positions() and coordinates_to_position(...)."""
    while True:
        choice = pyip.inputNum(
            f"Player {players_vector[player_index].color}, choose a Pawn to move: ",
            min=1,
            max=2,
        )
        pawn_index = choice - 1  # choice-1 cause pawn indexes are 0 and 1.
        destination_x = pyip.inputNum(
            f"Enter X (1-5) to move your Pawn #{choice} to: ", min=1, max=5
        )
        destination_y = pyip.inputNum(
            f"Enter Y (1-5) to move your Pawn #{choice} to: ", min=1, max=5
        )
        if move_check(
            cards_vector,
            players_vector,
            player_index,
            pawn_index,
            destination_x,
            destination_y,
        ):
            players_vector[player_index].record_positions()
            if pawn_index == 0:
                players_vector[player_index].coordinates[0] = [
                    destination_x,
                    destination_y,
                ]
            elif pawn_index == 1:
                players_vector[player_index].coordinates[1] = [
                    destination_x,
                    destination_y,
                ]
            players_vector[player_index].coordinates_to_position(
                board.WIDTH, pawn_index
            )
            break

def counter_move(board, players_vector):
    """Calls the Player() methods record_positions() and coordinates_to_position(...)."""
    counter = players_vector[0]
    if counter.coordinates[0] != [-1, -1]:
        counter.record_positions()
        if (counter.coordinates[0][1] % 2 != 0) and not (
            counter.coordinates[0][0] == board.WIDTH
        ):
            counter.coordinates[0][0] += 1
        elif (counter.coordinates[0][1] % 2 == 0) and not (
            counter.coordinates[0][0] == 1
        ):
            counter.coordinates[0][0] -= 1
        else:
            counter.coordinates[0][1] += 1
        counter.coordinates_to_position(board.WIDTH, 0)
        log.debug(f"counter_move() - New Counter coordinates: counter.coordinates[0]")
        print("The Counter King moves.")

# CHECKS

def place_pawns_check(board, cards_vector, players_vector, x, y):
    for i in range(len(players_vector)):
        if [x, y] in players_vector[i].coordinates:
            print(
                "During the setup, your pawns cannot start on the same card as others. Try again."
            )
            return False
    if len(players_vector) == 2:
        if cards_vector[0].back != cards_vector[board.WIDTH * (y - 1) + (x - 1)].back:
            print(
                f"You must select a card with a {cards_vector[0].back} back to place your pawn. Try again."
            )
            return False
        else:
            return True
    elif len(players_vector) > 2:
        if cards_vector[board.WIDTH * (y - 1) + (x - 1)].back == "Black":
            print(
                f"You must select a card with a White back to place your pawn. Try again."
            )
            return False
        else:
            return True

def cards_state_check(cards_vector, players_vector):
    for i in range(len(cards_vector)):
        card = cards_vector[i]
        for j in range(len(players_vector)):
            pawn = players_vector[j]
            if (
                (card.coordinates == pawn.coordinates[0])
                or (card.coordinates == pawn.coordinates[1])
                or (card.token != None)
            ):
                card.open = True
                break
            elif j == len(players_vector) - 1 and card.back == "White":
                card.open = False
                continue
            elif j == len(players_vector) - 1 and card.back == "Black":
                card.open = False
                continue

def move_check(
    cards_vector, players_vector, player_index, pawn_index, destination_x, destination_y
    ):
    """Returns True for valid moves. False for invalid moves.\n
    Sequence of "If" checks: Start=End (False) > Pawn Move (True) > Opponent's Token (False) >
    Bishop (True) > Rook (True) > Knight (True) > Queen (True) > else (False)"""
    current_place = players_vector[player_index].coordinates[pawn_index]
    if current_place == [destination_x, destination_y]:
        print(f"The Pawn is already on {current_place}. Choose other coordinates.")
        log.debug("Same coordinates attempt.")
        return False
    elif (
        [destination_x, destination_y] == [current_place[0] + 1, current_place[1]]
        or [destination_x, destination_y] == [current_place[0] - 1, current_place[1]]
        or [destination_x, destination_y] == [current_place[0], current_place[1] + 1]
        or [destination_x, destination_y] == [current_place[0], current_place[1] - 1]
    ):
        log.debug("Valid Standard Pawn Move")
        return True
    else:
        for i in range(len(cards_vector)):
            if i == players_vector[player_index].positions[pawn_index]:
                if (cards_vector[i].token != None) and (
                    cards_vector[i].token != players_vector[player_index].color
                ):
                    print(
                        f"This Pawn is on a card of the {cards_vector[i].token} Player. "
                        f"You cannot use Escort on it anymore."
                    )
                    log.debug("Card with Opponent's Token.")
                    return False
                elif (cards_vector[i].rank == "Bishop") and (
                    abs(destination_x - current_place[0])
                    == abs(destination_y - current_place[1])
                ):
                    log.debug("Valid Bishop Escort")
                    return True
                elif (cards_vector[i].rank == "Rook") and (
                    (destination_x == current_place[0])
                    or (destination_y == current_place[1])
                ):
                    log.debug("Valid Rook Escort")
                    return True
                elif (cards_vector[i].rank == "Knight") and (
                    (
                        abs(destination_x - current_place[0]) == 2
                        and abs(destination_y - current_place[1]) == 1
                    )
                    or (
                        abs(destination_x - current_place[0]) == 1
                        and abs(destination_y - current_place[1]) == 2
                    )
                ):
                    log.debug("Valid Knight Escort")
                    return True
                elif (cards_vector[i].rank == "Queen") and (
                    abs(destination_x - current_place[0])
                    == abs(destination_y - current_place[1])
                    or (destination_x == current_place[0])
                    or (destination_y == current_place[1])
                ):
                    log.debug("Valid Queen Escort")
                    return True
                else:
                    print(
                        f"You cannot move to {[destination_x, destination_y]}."
                        f" Choose other coordinates."
                    )
                    log.debug("Invalid Move.")
                    return False

def recruit_check(cards_vector, players_vector, validate):
    f = players_vector[0].positions[0]
    for i in range(1, len(players_vector)):
        m = players_vector[i].positions[0]
        n = players_vector[i].positions[1]
        if (
            (f != m)
            and (cards_vector[f].token == None)
            and (cards_vector[f].color == cards_vector[m].color)
            and (cards_vector[f].rank == cards_vector[m].rank)
        ):
            cards_vector[m].token = players_vector[0].color
            cards_vector[f].token = players_vector[0].color
            players_vector[0].score += 1
            print(
                f"The Counter King recruited the pair of"
                f"{cards_vector[f].color} {cards_vector[f].rank}s"
                f" and makes an extra move."
            )
            validate.who_recruited = 0
            return
        elif (
            (f != n)
            and (cards_vector[f].token == None)
            and (cards_vector[f].color == cards_vector[n].color)
            and (cards_vector[f].rank == cards_vector[n].rank)
        ):
            cards_vector[n].token = players_vector[0].color
            cards_vector[f].token = players_vector[0].color
            players_vector[0].score += 1
            print(
                f"The Counter King recruited the pair of"
                f" {cards_vector[f].color} {cards_vector[f].rank}s"
                f" and makes an extra move."
            )
            validate.who_recruited = 0
            return
        elif (
            (m != n)
            and (cards_vector[m].token == None)
            and (cards_vector[m].color == cards_vector[n].color)
            and (cards_vector[m].rank == cards_vector[n].rank)
        ):
            cards_vector[m].token = players_vector[i].color
            cards_vector[n].token = players_vector[i].color
            players_vector[i].score += 1
            print(
                f"The Player {players_vector[i].color} recruited the"
                f" pair of {cards_vector[m].color} {cards_vector[m].rank}s"
                f" and can make an extra move."
            )
            validate.who_recruited = i
            return
        else:
            validate.who_recruited = None

def queen_check(board, cards_vector, players_vector):
    """Calls peek_card()"""
    cards_state_check(cards_vector, players_vector)
    for card in cards_vector:
        if (card.rank == "Queen") and card.open:
            for player_index in range(len(players_vector)):
                if players_vector[0].positions[0] == card.number:
                    return
                elif (
                    players_vector[player_index].previous_positions[0] == card.number
                ) or (
                    players_vector[player_index].previous_positions[1] == card.number
                ):
                    return
            peek_card(board, cards_vector, players_vector)

def end_game_check(cards_vector, players_vector, clock, validate):
    for player_index in range(1, len(players_vector)):
        if players_vector[0].score == 6:
            print(
                f"The Counter King got {players_vector[0].score}/6 pairs. You've lost!"
            )
            validate.is_finished = True
            break
        elif clock.counter_turns >= len(cards_vector) - 1:
            print("Time's up! You've lost!")
            validate.is_finished = True
            break
        elif players_vector[player_index].score == 6:
            print("Congratulations! You've beat the Counter King!")
            validate.is_finished = True
            break
        else:
            validate.is_finished = False
            break

# SPECIAL ACTIONS

def peek_card(board, cards_vector, players_vector):
    """Takes input for peeking a hidden card and prints the card."""
    while True:
        peek_x = pyip.inputNum(
            f"Enter X (1-5) for the hidden card you want to peek: ",
            min=1,
            max=board.WIDTH,
        )
        peek_y = pyip.inputNum(
            f"Enter Y (1-5) for the hidden card you want to peek: ",
            min=1,
            max=board.HEIGHT,
        )
        card_index = board.WIDTH * (peek_y - 1) + (peek_x - 1)
        if cards_vector[card_index].open:
            print(
                f"The card on [x, y] = {cards_vector[card_index].coordinates} is"
                f" already revealed. Try again."
            )
            continue
        else:
            print(
                f"The card on [x, y] = {cards_vector[card_index].coordinates} is"
                f" a {cards_vector[card_index].color} {cards_vector[card_index].rank}."
            )
            break

# PRINT TO TERMINAL

def hidden_board(board, cards_vector):
    '''Prints the Hidden Board \n CURRENTLY UNUSED'''
    for i in range(len(cards_vector)):
        card = cards_vector[i]
        if card.back == "White":
            termcolor.cprint("[     ]", end=" ")
        elif card.back == "Black":
            print("[     ]", end=" ")
        if (i + 1) % board.WIDTH == 0:
            print(" ")

def print_board(board, cards_vector, players_vector):
    ### PYGAME ###
    show_board(board, cards_vector, players_vector)
    ### PYGAME ###
    for i in range(len(cards_vector)):
        card = cards_vector[i]
        for j in range(len(players_vector)):
            pawn = players_vector[j]
            if (
                (card.coordinates == pawn.coordinates[0])
                or (card.coordinates == pawn.coordinates[1])
                or (card.token != None)
            ):
                print_colored_board(cards_vector, players_vector, i)
                break
            elif j == len(players_vector) - 1 and card.back == "White":
                termcolor.cprint("[     ]", "grey", "on_white", end=" ")
                continue
            elif j == len(players_vector) - 1 and card.back == "Black":
                print("[     ]", end=" ")
                continue
        if (i + 1) % board.WIDTH == 0:
            print(" ")

def print_colored_board(cards_vector, players_vector, card_index):
    card = cards_vector[card_index]
    pawn = " "
    token = " "
    counter = " "
    code = " "
    for i in range(len(players_vector)):
        if players_vector[0].positions[0] == card_index:
            counter = "C"
        else:
            counter = " "
        for j in range(2):
            if players_vector[i].positions[j] == card_index:
                if players_vector[i].color == "Orange":
                    pawn = "O"
                elif players_vector[i].color == "Purple":
                    pawn = "P"
                elif players_vector[i].color == "White":
                    pawn = "W"
                elif players_vector[i].color == "Black":
                    pawn = "B"
                else:
                    pawn = " "
    if card.token != None:
        if card.token == "Orange":
            token = "o"
        elif card.token == "Pueple":
            token = "p"
        elif card.token == "White":
            token = "w"
        elif card.token == "Black":
            token = "b"
        else:
            token = " "
        if card.token == "Counter King":
            counter_token = "c"
        else:
            counter_token = " "
    else:
        token = " "
        counter_token = " "
    if card.color == "Blue":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "grey",
            "on_blue",
        )
    elif card.color == "Red":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "grey",
            "on_red",
        )
    elif card.color == "Yellow":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "grey",
            "on_yellow",
        )
    elif card.color == "Green":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "grey",
            "on_green",
        )
    elif card.color == "Magenta":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "grey",
            "on_magenta",
        )
    elif card.color == "Grey":
        code = termcolor.colored(
            "[" + counter + counter_token + card.code[1] + token + pawn + "]",
            "white",
            "on_grey",
        )
    else:
        code = "[" + counter + counter_token + card.code[1] + token + pawn + "]"
    print(code, end=" ")

### PYGAME ###
    ''' Code is a mess from here, cause I'm still testing things and deciding what to do.
    The screen is working though, you can't click or interact,\n
    but it updates based on the terminal moves.
    Added stuff to: print_board() and run() '''

pygame.init()

screen_size = screen_width, screen_height = (800, 600)
corner = (150,50)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Memory Kings')
# clock = pygame.time.Clock()

class Image:
    '''Methods for getting and returning the images paths (strings).'''

    def card(self, cards_vector, card_index): # Cards = 100x100
        card = cards_vector[card_index]
        return pygame.image.load('images/' + card.color.lower() + '_' + card.rank.lower() + '.png')

    def pawn(self, players_vector, player_index): # Pawns = 30x30
        player = players_vector[player_index]
        return pygame.image.load('images/pawn_' + (player.color.lower()).replace(" ", "") + '.png')

    def token(self, cards_vector, card_index): # Tokens = 30x30
        card = cards_vector[card_index]
        return pygame.image.load('images/token_' + (card.token.lower()).replace(" ", "") + '.png')

class Button:
    '''For a button to have an "action_func()" with several arguments (action_arg),\n
     add them as a single tuple (e.g. action_func((a, b, c, d))) and separate it in the\n
     beginning of that function.\n I think I can clean this up a bit.'''
    def __init__(self, image, center_x, center_y, angle, scale, hover_image=None, action_func=None, action_arg=None):
        self.image = image
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.scale = scale
        self.hover_image = hover_image
        self.action_func = action_func
        self.action_arg = action_arg

    def button(self):
        image_path = 'images/' + self.image
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        original_image = pygame.image.load(image_path).convert()
        scaled_image = pygame.transform.rotozoom(original_image, self.angle, self.scale)
        self.image_rect = scaled_image.get_rect()
        self.image_rect.center = (self.center_x, self.center_y)
        if self.image_rect.collidepoint(mouse) and self.hover_image != None:
            hover_path = 'images/' + self.hover_image
            hover = pygame.image.load(hover_path).convert()
            scaled_hover = pygame.transform.rotozoom(hover, self.angle, self.scale)
            self.hover_rect = scaled_hover.get_rect()
            self.hover_rect.center = (self.center_x, self.center_y)
            screen.blit(scaled_hover, self.hover_rect)
        else:
            screen.blit(scaled_image, self.image_rect)
        if self.action_func != None and click[0] == 1:
            screen.blit(scaled_image, self.image_rect)
            if self.action_arg != None:
                self.action_func(self.action_arg)
            else:
                self.action_func()

def show_board(board, cards_vector, players_vector):
    cards_state_check(cards_vector, players_vector)
    get_image = Image()
    screen.fill(GREY)
    for x in range(5):
        for y in range(5):
            coordinates = corner[0]+100*x, corner[1]+100*y
            card_index = board.WIDTH*(y)+(x)
            if cards_vector[card_index].open:
                card_image = get_image.card(cards_vector, card_index)
                screen.blit(card_image, (coordinates))
            elif cards_vector[card_index].back == 'Black':
                screen.blit(pygame.image.load('images/black_back.png'), (coordinates))
            elif cards_vector[card_index].back == 'White':
                screen.blit(pygame.image.load('images/white_back.png'), (coordinates))
            if cards_vector[card_index].token != None:
                token_image = get_image.token(cards_vector, card_index)
                screen.blit(token_image, (coordinates[0]+66, coordinates[1]+66))
            for player_index in range(len(players_vector)):
                if players_vector[0].positions[0] == card_index:
                    pawn_image = get_image.pawn(players_vector, 0)
                    screen.blit(pawn_image, (coordinates[0]+4, coordinates[1]+4))
                elif players_vector[player_index].positions[0] == card_index:
                    pawn_image = get_image.pawn(players_vector, player_index)
                    screen.blit(pawn_image, (coordinates[0]+4, coordinates[1]+66))
                elif players_vector[player_index].positions[1] == card_index:
                    pawn_image = get_image.pawn(players_vector, player_index)
                    screen.blit(pawn_image, (coordinates[0]+66, coordinates[1]+4))
    pygame.display.update()

# SYSTEM

if __name__ == "__main__":
    run()