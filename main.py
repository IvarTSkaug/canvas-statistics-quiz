import random
from lib import calculate_variance_string, signLT12, sum_probabilities

random.seed(1232)
n = 24  # Number of question variants

# Oppgave 1
# Open a file to write and create the quiz with the first group of questions
with open('quiz.txt', 'w', encoding='utf-8') as file:
    file.write("Quiz title: Oblig 1\n")
    file.write("GROUP\npick: 1\npoints per question: 1\n")

    for i in range(n):
        # Generate a random range for the current question
        sample_size = random.choice([3, 4])
        selection = random.sample(range(1, 8), sample_size)

        # Calculate the variance
        Sxx = sum((xi - (sum(selection) / len(selection))) ** 2 for xi in selection)
        variance = round(Sxx / (len(selection) - 1), 2)

        # Create the feedback text using the same selection of numbers
        Sxx_string, variance_string = calculate_variance_string(selection)

        # Convert to LaTeX format and format feedback
        f_1 = f"${Sxx_string}$"
        f_2 = f"${variance_string}$"
        feedback = f"{f_1}\n     {f_2}"

        # Format question
        qt_1 = f"Vi observerer et tilfeldig utvalg bestående av tallene {', '.join(str(num) for num in selection)}."
        qt_2 = f"Angi utvalgets varians $(s^2)$ som en tallverdi med to desimaler:"
        question = f"{qt_1}\n\n\t{qt_2}"

        # Write question
        file.write(f"""
Title: Oppgave 1
{i + 1}. {question}
... {feedback}
= {variance} +- 0.01
        """)

    file.write("\nEND_GROUP\n")

# Oppgave 2
with open("quiz.txt", "a", encoding='utf-8') as file:
    file.write("GROUP\npick: 1\npoints per question: 2\n")

    # Loop to generate 3 question variants
    for i in range(n):

        # Creating boolean questions for each iteration
        q_1 = random.choice([True, False])
        q_2 = random.choice([True, False])
        q_3 = random.choice([True, False])

        # If all values are False, force Q_2 to be True
        if not (q_1 or q_2 or q_3):
            q_2 = True

        a,b,c = random.sample(["A","B","C"],3)

        event_1, event_2 = sorted([a, b])

        # Generating the variables for each iteration
        P_A = round(random.uniform(0.1, 0.4), 2)
        P_B = round(random.uniform(0.1, 0.4), 2)
        P_C_given_A = round(random.uniform(0.1, 0.5), 2)
        P_C_given_B = round(random.uniform(0.1, 0.5), 2)
        P_A_given_C = round(random.uniform(0.1, 0.5), 2)

        # Calculating necessary values without rounding
        P_intersect_B_C = P_B * P_C_given_B
        P_intersect_A_C = P_A * P_C_given_A
        P_C = (P_A * P_C_given_A) / P_A_given_C
        P_B_given_A_union_C = P_intersect_B_C/(P_A + P_C - P_intersect_A_C)

        # Creating copies of the correct values for feedback and round them
        P_intersect_B_C_feedback = round(P_intersect_B_C, 3)
        P_intersect_A_C_feedback = round(P_intersect_A_C, 3)
        P_C_feedback = round(P_C, 3)
        P_B_given_A_union_C_feedback = round(P_B_given_A_union_C, 3)

        i_1 = '*'
        i_2 = '*'
        i_3 = '*'

        # Compute the false statement
        noise = 0.05
        if not q_1:
            i_1 = ' '
            P_intersect_B_C = P_intersect_B_C + signLT12(P_intersect_B_C)*noise
        if not q_2:
            i_2 = ' '
            P_C = P_C + signLT12(P_C)*noise
        if not q_3:
            i_3 = ' '
            P_B_given_A_union_C = P_B_given_A_union_C + signLT12(P_B_given_A_union_C)*noise

        # Round statments
        P_intersect_B_C = round(P_intersect_B_C, 3)
        P_C = round(P_C, 3)
        P_B_given_A_union_C = round(P_B_given_A_union_C, 3)

        # Format feedback
        f_1 = f"$P({b} \\cap {c}) = P({b}) P({c}|{b}) = {P_B} \\times {P_C_given_B} = {P_intersect_B_C_feedback}$"
        f_2 = f"$P({c}) = \\frac{{P({a}) P({c}|{a})}}{{P({a}|{c})}} = \\frac{{{P_A} \\times {P_C_given_A}}}{{{P_A_given_C}}} = {P_C_feedback}$"
        f_3 = f"$P({b}|{a} \\cup {c}) = \\frac{{P({b} \\cap {c})}}{{P({a}) + P({c}) - P({a} \\cap {c})}} = \\frac{{{P_intersect_B_C_feedback}}}{{{P_A} + {P_C_feedback} - {P_intersect_A_C_feedback}}} = {P_B_given_A_union_C_feedback}$"
        feedback = f"{f_1}\n     {f_2}\n     {f_3}"

        # Format questions
        qt_1 = f"La $A$, $B$ og $C$ være tre hendelser i et utfallsrom $S$, der hendelsene ${event_1}$ og ${event_2}$ er disjunkte. La videre følgende sannsynligheter være gitt: $P({a}) = {round(P_A, 3)}$, $P({b}) = {round(P_B, 3)}$, $P({c}|{a}) = {round(P_C_given_A, 3)}$, $P({c}|{b}) = {round(P_C_given_B, 3)}$, $P({a}|{c}) = {round(P_A_given_C, 3)}$."
        qt_2 = f"Hvilke av følgende utsagn er korrekte?"
        question = f"{qt_1}\n\n\t{qt_2}"

        file.write(f"""
Title: Oppgave 2
{i + 1}. {question}
... {feedback}
[{i_1}] $P({b} \cap {c}) = {P_intersect_B_C}$
[{i_2}] $P({c}) = {P_C}$
[{i_3}] $P({b}|{a} \cup {c}) = {P_B_given_A_union_C}$
       """)
    # Write group end
    file.write("\nEND_GROUP\n")

with open("quiz.txt", "a", encoding='utf-8') as file:
    file.write("GROUP\npick: 1\npoints per question: 2\n")

    for i in range(n):
        q_1 = random.choice([True, False])
        q_2 = random.choice([True, False])
        q_3 = random.choice([True, False])

        if not (q_1 or q_2 or q_3):
            q_2 = True

        px_list = [round(random.uniform(0.1, 0.15), 2) for _ in range(5)]
        px_list.append(round(1 - sum(px_list), 2))
        s1_index = random.randint(0, 3)
        s2_first_index = random.randint(0, 3)
        s2_second_index = s2_first_index + 1

        computed_sum_prob, sum_string = sum_probabilities(px_list, start=s1_index+1)
        teller, string_A = sum_probabilities(px_list, start=s2_first_index, stop=s2_second_index + 1)
        nevner, string_B = sum_probabilities(px_list, start=s2_first_index, stop=6)
        conditional_prob = teller / nevner if nevner > 0 else 0
        expected_value = sum(index * px for index, px in enumerate(px_list))

        sum_prob_feedback = round(computed_sum_prob, 3)
        expected_value_feedback = round(expected_value, 3)
        conditional_prob_feedback = round(conditional_prob, 3)

        i_1 = '*'
        i_2 = '*'
        i_3 = '*'

        # Compute the false statement
        noise = 0.05
        if not q_1:
            i_1 = ' '
            computed_sum_prob = computed_sum_prob + signLT12(computed_sum_prob)*noise

        if not q_2:
            i_2 = ' '
            conditional_prob = conditional_prob + signLT12(conditional_prob)*noise

        if not q_3:
            i_3 = ' '
            expected_value = expected_value + signLT12(expected_value)*noise*3

        computed_sum_prob = round(computed_sum_prob, 3)
        expected_value = round(expected_value, 3)
        conditional_prob = round(conditional_prob, 3)

        # feedback for f_3
        inner_string = ' + '.join(f'{index} \\times {px}' for index, px in enumerate(px_list))

        # Format feedback
        f_1 = f"$P(X>{s1_index})={sum_string} = {sum_prob_feedback}$"
        f_2 = f"$P(X≤{s2_second_index}|X≥{s2_first_index})=({string_A})/({string_B}) = {conditional_prob_feedback}$"
        f_3 = f"$E[X] = {inner_string} = {expected_value_feedback}$"
        feedback = f"{f_1}\n     {f_2}\n     {f_3}\n"

        px_string = ',   '.join([f"$p({x})={px}$" for x, px in enumerate(px_list)])

        qt_1 = f"La $X$ være en diskret tilfeldig variabel med punktsannsynlighet $p(x)$ gitt som {px_string}."
        qt_2 = f"Hvilke av følgende utsagn er korrekte?"
        question = f"{qt_1}\n\n\t{qt_2}"

        file.write(f"""
Title: Oppgave 4
{i + 1}. {question}
... {feedback}
[{i_1}] $P(X>{s1_index})$ = ${computed_sum_prob}$
[{i_2}] $P(X≤{s2_second_index}|X≥{s2_first_index})$ = ${conditional_prob}$
[{i_3}] $E[X]$ = ${expected_value}$
        """)

    file.write("\nEND_GROUP\n")

# Oppgave 3
with open("quiz.txt", "a", encoding='utf-8') as file:
    # Write group start
    file.write("GROUP\npick: 1\npoints per question: 2\n")

    for i in range(n):

        r = i//8+1
        b = i%8+1
        x = random.randint(4, 8)
        y = x - random.randint(0, 1)  # Subtracts either 0 or 1 from x with equal probability.

        if y == x:
            # Compute number of ways to draw a red ball
            answer = (b**(x - 1)) * r  # (b^(y-1))*r
            f_1 = f"${b}^{{({x}-1)}} \\times {r} = {answer}$."
        else:
            # Compute number of ways to draw a red ball at (y-1)th draw and any color
            answer = (b**(x - 2)) * r * (r + b)
            f_1 = f"${b}^{{({y}-1)}} \\times {r} \\times ({r} + {b}) = {answer}$."

        f_2 = f"Forklaring: ${b}$ mulige blå kuler på første trekkning, osv"
        feedback = f"{f_1}\n\n     {f_2}\n"

        qt_1 = f"Anta at vi gjentatte ganger trekker en kule $\\textbf{{med tilbakelegging}}$ fra en urne med ${r}$ røde og ${b}$ blå kuler (nummerert fra $1$ til ${r+b}$). Anta at vi for hver trekning noterer oss nummer og fargen på kula vi trakk før vi legger kula tilbake i urna. På hvor mange forskjellige måter kan vi trekke ${x}$ ganger (kuler), slik at første røde kule kommer på trekning nummer ${y}$?" 
        qt_2 = f"Angi svaret som et heltall:"
        question = f"{qt_1}\n\n\t{qt_2}"

        file.write(f"""
Title: Oppgave 3
{i+1}. {question}
... {feedback}
= {answer} +- 0.01
        """)

    file.write("\nEND_GROUP\n")

# Oppgave 4
with open("quiz.txt", "a", encoding='utf-8') as file:
    file.write("GROUP\npick: 1\npoints per question: 1\n")

    for i in range(n):
        q_1 = random.choice([True, False])
        q_2 = random.choice([True, False])
        q_3 = random.choice([True, False])

        if not (q_1 or q_2 or q_3):
            q_2 = True

        # Set the given values
        P_positive_given_sick = round(random.uniform(0.72, 0.89), 3)
        P_positive_given_not_sick = round(random.uniform(0.01, 0.05), 3)
        P_sick = round(random.uniform(0.03, 0.11), 2)
        P_not_sick = 1 - round(P_sick, 2)

        # Calculate the probabilities
        P_not_sick_and_positive = P_not_sick * P_positive_given_not_sick
        # Calculate the total probability of a positive result
        P_positive = P_not_sick_and_positive + (P_positive_given_sick * P_sick)

        # Calculate the probability
        P_not_sick_given_positive = (P_not_sick * P_positive_given_not_sick) / P_positive

        P_not_sick_and_positive_feedback = round(P_not_sick_and_positive, 3)
        P_positive_feedback = round(P_positive, 3)
        P_not_sick_given_positive_feedback = round(P_not_sick_given_positive, 3)

        i_1 = '*'
        i_2 = '*'
        i_3 = '*'

        # Compute the false statement
        noise = 0.05
        if not q_1:
            i_1 = ' '
            P_not_sick_and_positive = P_not_sick_and_positive + signLT12(P_not_sick_and_positive)*noise

        if not q_2:
            i_2 = ' '
            P_positive = P_positive + signLT12(P_positive)*noise

        if not q_3:
            i_3 = ' '
            P_not_sick_given_positive = P_not_sick_given_positive + signLT12(P_not_sick_given_positive)*noise

        P_not_sick_and_positive = round(P_not_sick_and_positive, 3)
        P_positive = round(P_positive, 3)
        P_not_sick_given_positive = round(P_not_sick_given_positive, 3)

        qt_f = f"La $C$ være begivenheten at den tilfeldig valgte personen har covid og $T$ hendelsen at testen er positiv. Det gitt i oppgaven at $P(C) = {P_sick}$, $P(T|C) = {int(P_positive_given_sick*1000)}/1000 = {P_positive_given_sick}$, og $P(T|C') = {int(P_positive_given_not_sick*1000)}/1000 = {P_positive_given_not_sick}$."
        f_1 = f"$P(C' \cap T) = P(T|C')P(C') =  {P_positive_given_not_sick} \\times {P_not_sick} = {P_not_sick_and_positive_feedback}$"
        f_2 = f"$P(T) = P(T|C')P(C')+P(T|C)P(C) =  {P_not_sick_and_positive_feedback} + ({P_positive_given_sick} \\times {P_sick}) = {P_positive_feedback}$"
        f_3 = f"$P(C'|T) = \\frac{{P(C' \cap T)}}{{P(T)}} = {P_not_sick_given_positive_feedback}$ (regner eksakt i teller og nevner)"
        feedback = f"{qt_f}\n\n     {f_1}\n     {f_2}\n     {f_3}\n"

        qt_1 = f"Et legemiddelfirma prøver en ny Covid-19 hurtigtest på 1000 smittede personer, og finner at ${int(P_positive_given_sick*1000)}$ av disse tester positivt. Tilsvarende prøver firmaet hurtigtesten på 1000 ikke-smittede personer og finner at ${int(P_positive_given_not_sick*1000)}$ av disse tester positivt. I befolkningen er det ${int(P_sick*100)}$% som er smittet. Vi trekker en tilfeldig person fra befolkningen og lar denne bruke den nye hurtigtesten."
        qt_2 = f"Hvilke av følgende utsagn er korrekte?"
        question = f"{qt_1}\n\n\t{qt_2}"

        file.write(f"""
Title: Oppgave 4
{i + 1}. {question}
... {feedback}
[{i_1}] $P$(Personen er ikke smittet samtidig som testen er positiv) = ${P_not_sick_and_positive}$
[{i_2}] $P$(Testen er positiv) = ${P_positive}$
[{i_3}] $P$(Personen er ikke smittet gitt at testen er positiv) = ${P_not_sick_given_positive}$
            """)

    file.write("\nEND_GROUP\n")
