from dataclasses import dataclass
import random
import logging

KICKUPS = {}

@dataclass
class Pairing():
    red_goal: str
    red_strike: str

    blue_goal: str
    blue_strike: str

OPEN = 'open'
RUNNING = 'running'
RESOLVED = 'resolved'
CANCELLED = 'cancelled'

def new_kickup():
    while True:
        num = random.randint(10000,1000000)
        if num not in KICKUPS: break
    KICKUPS[num] = KickUp(num)
    return KICKUPS[num]

def get_kickup(num):
    if not num in KICKUPS:
        return None
    return KICKUPS[num]

class KickUp():

    def __init__(self, num):
        self.num = num
        self.state = OPEN
        self.players = set()
        self.pairing = None
        self.warnings = set()
        self.score_blue = 0
        self.score_red = 0

    def add_player(self, player_id):
        if player_id in self.players:
            logging.info(f'Player "{ player_id }" is already part of kickup { self.num }')
            return False
        else:
            logging.info(f'Player "{ player_id }" joined kickup { self.num }')
            self.players.add(player_id)
            return True

    def start_match(self):
        if len(self.players) < 4:
            self.warnings.add('Need at least 4 players to start!')
            return
        logging.info(f'Kickup Match { self.num } has been started')
        self.pairing = Pairing(*random.sample(self.players, 4))
        self.state = RUNNING

    def resolve_match(self):
        if self.state == RESOLVED:
            logging.warning(f'Kickup { self.num } was resolved before!')
            return False
        if self.score_blue != 6 and self.score_red != 6:
            self.warnings.add('At least one team needs 6 goals!')
            return False
        if self.score_blue == 6 and self.score_red == 6:
            self.warnings.add('Both teams can\'t have score 6!')
            return False
        logging.info(f'Kickup { self.num } has been resolved RED { self.score_red }:{ self.score_blue } BLUE')
        self.state = RESOLVED
        return True

    def process_warnings(self):
        if not self.warnings:
            return None
        result = self.warnings.copy()
        self.warnings = set()
        return result

    def cancel(self):
        self.state = CANCELLED


