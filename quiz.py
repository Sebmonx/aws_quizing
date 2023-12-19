import pandas as pd
import random as ran

def select_question(bank, used_questions, question_amount):
    ran.seed()
    
    question_number = ran.randint(1, bank.shape[0])
    
    while question_number in used_questions:
        question_number = ran.randint(1, bank.shape[0])

    used_questions.append(question_number)
    question = bank['Pregunta'].loc[bank.index[question_number-1]]

    return question, question_number

def save_options(bank, question_number):

    columns = list(bank.columns.values)
    columns.pop(0)
    columns.pop(-1)
    options = {}
    for index,i in zip(columns, range(1, len(columns)+1)): 
        valor = str(bank[index].loc[bank.index[question_number-1]])
        if valor == 'nan':
            pass
        else:
            options[f'{i}'] = valor
    return options
    
def print_options(options):
    for key, value in options.items():
        print(key + ' ' + value)

def save_answer(options):
    while True:
        answer_key = input('Ingrese el número de la respuesta correcta: ')
        if answer_key.isnumeric() and str(answer_key) in options.keys():
            return answer_key
        else:
            print('Por favor elegir un número válido')

def check_answer(bank, answer, question_number):
    right_answer = str(bank['Respuestas'].loc[bank.index[question_number - 1]])
    if answer in right_answer:
        return True
    else:
        return False

def question_cicle(bank, score, used_questions, question_amount):

    question, question_number = select_question(bank, used_questions, question_amount)
    print(question)

    options = save_options(bank, question_number)
    print_options(options)

    answer = save_answer(options)

    if check_answer(bank, answer, question_number):
        score = score + 1
    
    bank = bank.drop(question_number - 1)
    return score

def questions_selection():
    while True:
        print("Elige la cantidad de preguntas")
        print("1. Estándar de AWS, 65 preguntas.")
        print("2. Yo elijo la cantidad.")
        print("3. Utilizar todo el banco de forma aleatoria")
        choice = int(input())
        if choice in [1, 2, 3]:
            return choice

def user_question_selection(bank):
    while True:
        quantity = int(input("Ingresa la cantidad de preguntas: "))
        if quantity in range(1, bank.shape[0]):
            return quantity

def question_amount(bank):
    
    choice = questions_selection()
    
    if choice == 1:
        return 65
    elif choice == 2:
        choice = user_question_selection(bank)
        return choice
    else:
        choice = bank.shape[0]
        return choice



def main():

    score = 0
    used_questions = []
    path = 'Question_bank.csv' 
    sheet = 'Test'
    bank = pd.read_csv(path, delimiter=";")
    number_of_questions = question_amount(bank)

    for i in range(1, number_of_questions + 1):
        score = question_cicle(bank, score, used_questions, number_of_questions)

    print(f'Obtuviste {score}/{number_of_questions} correctas')



main()




