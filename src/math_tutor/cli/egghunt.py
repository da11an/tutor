import time
from math_tutor.cli import egghunt_banner
from math_tutor.core.mathfacts import MathFact
from math_tutor.core.factlibrary import MultiplicationFactLibrary, AdditionFactLibrary, SubtractionFactLibrary, DivisionFactLibrary
from math_tutor.logs.leaderboard import Leaderboard
from math_tutor.logs.historian import Historian
from math_tutor.cli.utils import UserChoiceList, UserChoiceDict, count_down

leaderboard = Leaderboard("egghunt_leaders.json")
history = Historian("history.json")

def main():
    egghunt_banner()

    print("Hi! My name is Diddio! Let's hunt for hidden easter eggs.")

    print("\nWhat's your name?")
    user = UserChoiceList(leaderboard.users + ['New User!']).get_choice()
    if user == 'New User!':
        user = input("\nWhat's your name? ").title()

    leaderboard.display_streak(user)

    print("\nLet's review some challenge problems:")
    [MathFact.from_problem(problem).quiz(user=user) for problem in history.challenge_problems(user)[:3]]
    
    print("\nWhat kind of math facts?")
    fact_library_choices = {
            'addition (+)': AdditionFactLibrary,
            'subtraction (-)': SubtractionFactLibrary,
            'multiplication (x)': MultiplicationFactLibrary,
            'division (/)': DivisionFactLibrary
        }
    fact_type, fact_library_class = UserChoiceDict(fact_library_choices).get_choice()

    operator = fact_type.split('(')[1].split(')')[0]
    suggested_max_operand = history.suggest_level(user=user, operator=operator)
    print(f"\nYou are ready for level {suggested_max_operand}!")
    max_operand = suggested_max_operand

    print(f"\nHi {user}! Here's how it works. I have baskets of {fact_type} problems.")
    print("(Don't you?!) Each basket should only have matching problems that are equal.")
    print("But I accidentally dropped in an extra problem that doesn't match.")
    print("Your job is to find the one that doesn't belong and tell me what it equals.")
    print(f"\nEnter the answer to the problem that is different than the others ", end='')
    count_down(5)

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
        basket = sampled_library.fact_library[-1].sample(4)
        bad_egg = sampled_library.fact_library[0].sample_fact(1)
        basket.append(bad_egg)
        basket.shuffle()

        print(f"\n({i+1}) +{round(points[-1]) if len(points) > 0 else 0} feathers", end='')
        count_down(delay=3)
        print("")
        basket.print_problems
        print("")
        bad_egg.quiz(show_problem=False, user=user)

        p = bad_egg.performance
        feathers = p.correct + p.correct / p.timing * basket.len * max_operand

        points.append(feathers)
        if p.correct:
            print(f"\n    Good! {bad_egg.problem} = {bad_egg.answer}")
        else:
            print(f"\n    Try that again:\n")
            bad_egg.quiz(show_problem=True, user=user)
            if not bad_egg.performance.correct:
                print(f"\n    No: {bad_egg.problem} = {bad_egg.answer}")
                time.sleep(3)
            else:
                print(f"\n    Good! {bad_egg.problem} = {bad_egg.answer}")
                points.append(1)


    print(f"\nYou earned {round(sum(points))} feathers! Excellent! Feathers were awarded based on correctness, complexity, and speed.")
    leaderboard.add_entry(user, round(sum(points)), max_operand, fact_type)
    leaderboard.user_dashboard(user, fact_type)
    history.load()
    print(f"You're ready for level: {history.suggest_level(user=user, operator=operator)}")

if __name__ == "__main__":
    main()
