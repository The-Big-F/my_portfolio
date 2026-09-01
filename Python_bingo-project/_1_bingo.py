import random
from _1_students import *

def generate_bingo_list():
    bingo_list = random.sample(range(1, 49), 16)
    return bingo_list

student_cards = {}

for classroom_id, students in school.items():
    for student_id, student_info in students.items():
        name = student_info['first_name']
        card = generate_bingo_list()
        student_cards[name] = card

        # students assigned have a card assigned to them
        # print(f"{name}'s card: {sorted(list(card))}")


print (f"Bingo game is ready! Good luck to all students! Bingo cards have humbers from 1 to 48. Each student has a card with 16 numbers. The first student to have all 16 numbers drawn wins!\n")
draw_order = random.sample(range(1, 49), 48)
# pulling up to 40 bingo numbers
# print(draw_order)


drawn_numbers = []
winner = None
round_number = 0

for number in draw_order:
    round_number = round_number + 1
    drawn_numbers.append(number)

    # Show current list of drawn numbers
    # print(f"Round {round_number} | Drawn so far: {drawn_numbers}")

    # Check each student
    for name, card in student_cards.items():
        # Count how many numbers from the student's card have been drawn
        matches = 0
        for card_number in card:
            if card_number in drawn_numbers:
                matches = matches + 1

        # If all 16 numbers matched, we have a winner!
        if matches == 16:
            winner = name
            print (f"Drawn numbers: {drawn_numbers}")
            break

    # Stop drawing balls once someone wins
    if winner:
        break

print(f"\nBINGO! {winner} won on round {round_number}!")