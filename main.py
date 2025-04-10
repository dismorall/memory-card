from random import choice, shuffle
from time import sleep

from PyQt5.QtWidgets import QApplication

app = QApplication([])

from main_window import *
from menu_window import *

class Question:
    def __init__(self, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3
        self.isAsking = True
        self.count_ask = 0
        self.count_right = 0
    def got_right(self):
        self.count_ask += 1
        self.count_right += 1
    def got_wrong(self):
        self.count_ask += 1

q1 = Question('Яблуко', 'apple', 'application', 'pinapple', 'apply')
q2 = Question('Дім', 'house', 'horse', 'hurry', 'hour')
q3 = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')
q4 = Question('Число', 'number', 'digit', 'amount', 'summary')

radio_buttons = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
questions = [q1, q2, q3, q4]

def new_question():
    global cur_q
    cur_q = choice(questions)
    lb_Question.setText(cur_q.question)
    lb_Correct.setText(cur_q.answer)
    shuffle(radio_buttons)

    radio_buttons[0].setText(cur_q.wrong_answer1)
    radio_buttons[1].setText(cur_q.wrong_answer2)
    radio_buttons[2].setText(cur_q.wrong_answer3)
    radio_buttons[3].setText(cur_q.answer)

new_question()

def check():
    RadioGroup.setExclusive(False)
    for answer in radio_buttons:
        if answer.isChecked():
            if answer.text() == lb_Correct.text():
                cur_q.got_right()
                lb_Result.setText('Вірно!')
                answer.setChecked(False)
                break
            else:
                lb_Result.setText('Не вірно!')
                answer.setChecked(False)
                cur_q.got_wrong()

    RadioGroup.setExclusive(True)

def click_ok():
    if btn_OK.text() == 'Відповісти':
        a = False
        for radio in radio_buttons:
            if radio.isChecked():
                a = True
                break
        if a:
            check()
            RadioGroupBox.hide()
            AnsGroupBox.show()

            btn_OK.setText('Наступне запитання')
    else:
        new_question()
        RadioGroupBox.show()
        AnsGroupBox.hide()

        btn_OK.setText('Відповісти')
        
btn_OK.clicked.connect(click_ok)

def rest():
    win_card.hide()
    n = box_Minutes.value() * 60
    sleep(n)
    win_card.show()

btn_Sleep.clicked.connect(rest)

def allStatistics():
    count_ans = 0
    count_right = 0
    for q in questions:
        count_ans += q.count_ask
        count_right += q.count_right
    if count_ans == 0:
        return [0, count_ans, count_right]
    elif count_right == 0:
        return [0, count_ans, count_right]
    else:
        return [(count_right / count_right) * 100, count_ans, count_right]

def menu_switch():
    c, count_ans, count_right = allStatistics()
    text = f'Разів відповіли: {count_ans}\n' \
            f'Вірних відповідей: {count_right}\n' \
            f'Успішність: {round(c, 2)}%'
    lb_statistic.setText(text)        
    
    win_card.hide()
    menu_win.show()

btn_Menu.clicked.connect(menu_switch)

def clear():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()

btn_clear.clicked.connect(clear)

def add_questions():
    new_q = Question(le_question.text(), le_right_ans.text(),
                    le_wrong_ans1.text(), le_wrong_ans2.text(),
                    le_wrong_ans3.text())
    questions.append(new_q)
    clear()
    print(len(questions))

btn_add_question.clicked.connect(add_questions)

def back_switch():
    menu_win.hide()
    win_card.show()
    
btn_back.clicked.connect(back_switch)

win_card.show()
app.exec_()