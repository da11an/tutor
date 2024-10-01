import time
from random import sample, shuffle
from copy import deepcopy
from math_tutor.core.factlibrary import FactLibrary, MultiplicationFactLibrary, AdditionFactLibrary, SubtractionFactLibrary, DivisionFactLibrary
from math_tutor.logs.leaderboard import Leaderboard
from math_tutor.cli.utils import get_user_choice

leaderboard = Leaderboard("egghunt_leaders.json")

def main():
    print("Hi! My name is Diddio! Let's hunt for hidden easter eggs.")

    user = input("\nWhat's your name? ").title()

    fact_library_choices = {
            'addition (+)': AdditionFactLibrary,
            'subtraction (-)': SubtractionFactLibrary,
            'multiplication (x)': MultiplicationFactLibrary,
            'division (/)': DivisionFactLibrary
        }
    fact_type, fact_library_class = get_user_choice(fact_library_choices)
    print(f"\nHi {user}! Here's how it works. I have bags of {fact_type} problems.")
    print("(Don't you?!) Each bag should only have matching problems that are equal.")
    print("But I accidentally dropped in an extra problem that doesn't match.")
    print("Your job is to find the one that doesn't belong and tell me what it equals.")
    print("------------------------------------------------------------------------------\n")
    max_operand = int(input(f"How high would you like to practice your {fact_type} tables? "))
    min_operands = {'addition (+)': 1, 'subtraction (-)': 1, 'multiplication (x)': 2, 'division (/)': 2}
    min_operand = min_operands[fact_type]
    points = []
    fact_library = fact_library_class(min_operand, max_operand)
    for i in range(10):
        j = 0
        while True:
            j += 1
            sampled_library = fact_library.sample(2)
            sampled_library.sort_by_length()
            if sampled_library.fact_library[-1].len > 1:
                break
            elif j > 1000:
                raise ValueError("Sampled library doesn't contain a fact family with more than one fact. Please increase your max operand.")
        bag = sampled_library.fact_library[-1].sample(4)
        bad_egg = sampled_library.fact_library[0].sample_fact(1)
        bag.append(bad_egg)
        bag.shuffle()

        input(f"\n-- Press ENTER to inspect 'bag' {i+1}/10 -- Feathers: {round(sum(points))} --\n")
        bag.print_problems
        print("")
        bad_egg.quiz(show_problem=False)

        p = bad_egg.performance
        feathers = p.correct + p.correct / p.timing * bag.len * max_operand

        points.append(feathers)
        print(f"\n    Good!" if p.correct else f"\n    Actually, {bad_egg.problem} = {bad_egg.answer}.")
    print(f"\nYou earned {round(sum(points))} feathers! Excellent! Feathers were awarded based on correctness, complexity, and speed.")
    leaderboard.add_entry(user, round(sum(points)), max_operand, fact_type)
    leaderboard.display_leaderboard()
    leaderboard.display_all_time_leaders()
    leaderboard.display_personal_bests_by_fact_type(user)

if __name__ == "__main__":
    main()
