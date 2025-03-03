import random
from collections import Counter
Blotkarz = [(str(i+2),sign) for i in range(9) for sign in ['Kier','Karo','Pik','Trefl']]
Figurant = [(Fig,sign) for Fig in ['J','Q','K','A'] for sign in ['Kier','Karo','Pik','Trefl']]

def IsPoker(card1,card2,card3,card4,card5):
    return IsStrit(card1,card2,card3,card4,card5) and IsColor(card1,card2,card3,card4,card5)

def IsKareta(card1,card2,card3,card4,card5):
    values = [c[0] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return 4 in counts.values()

def IsColor(card1,card2,card3,card4,card5):
    values = [c[1] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return 4 in counts.values()

def IsFull(card1,card2,card3,card4,card5):
    values = [c[0] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return 2 in counts.values() and 3 in counts.values()
def IsStrit(card1,card2,card3,card4,card5):
    rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    values = sorted([rank_map[c[0]] for c in [card1, card2, card3, card4, card5]])

    return all(values[i] + 1 == values[i + 1] for i in range(4))

def IsTriple(card1,card2,card3,card4,card5):
    values = [c[0] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return 3 in counts.values()

def IsTwoPair(card1,card2,card3,card4,card5):
    values = [c[0] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return list(counts.values()).count(2) == 2

def IsPair(card1,card2,card3,card4,card5):
    values = [c[0] for c in [card1, card2, card3, card4, card5]]
    counts = Counter(values)
    return 2 in counts.values()

def rate_hand(card1, card2, card3, card4, card5):
    if IsPoker(card1, card2, card3, card4, card5): return 8
    if IsKareta(card1, card2, card3, card4, card5): return 7
    if IsFull(card1, card2, card3, card4, card5): return 6
    if IsColor(card1, card2, card3, card4, card5): return 5
    if IsStrit(card1, card2, card3, card4, card5): return 4
    if IsTriple(card1, card2, card3, card4, card5): return 3
    if IsTwoPair(card1, card2, card3, card4, card5): return 2
    if IsPair(card1, card2, card3, card4, card5): return 1
    return 0

# stochiastic propabilty check
tries = 10000
wins=0
losses=1
for i in range(tries):
    card1,card2,card3,card4,card5 = random.sample(Blotkarz,5)
    blotkarz_hand=rate_hand(card1,card2,card3,card4,card5)
    card1, card2, card3, card4, card5 = random.sample(Figurant, 5)
    figurant_hand = rate_hand(card1, card2, card3, card4, card5)

    # Compare hands
    if blotkarz_hand > figurant_hand:
        wins += 1
    else:
        losses += 1

# Print probability results
print(f"Blotkarz win probability: {wins / tries:.2%}")
print(f"Figurant win probability: {losses / tries:.2%}")

Blotkarz=[(str(i+2),'Kier') for i in range(9)]
Blotkarz.append(('2','Pik'))
Blotkarz.append(('2','Trefl'))
Blotkarz.append(('2','Karo'))


tries = 10000
wins=0
losses=1
for i in range(tries):
    card1,card2,card3,card4,card5 = random.sample(Blotkarz,5)
    blotkarz_hand=rate_hand(card1,card2,card3,card4,card5)
    card1, card2, card3, card4, card5 = random.sample(Figurant, 5)
    figurant_hand = rate_hand(card1, card2, card3, card4, card5)

    # Compare hands
    if blotkarz_hand > figurant_hand:
        wins += 1
    else:
        losses += 1

print(f"Blotkarz win probability: {wins / tries:.2%}")
print(f"Figurant win probability: {losses / tries:.2%}")