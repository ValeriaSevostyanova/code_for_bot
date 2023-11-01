import telebot
from telebot import types
import token_bot
from funcs_for_bot import *

import logging

import requests

import html
import time

bot = telebot.TeleBot(token_bot.TOKEN)
text_dict = {}

@bot.message_handler(commands=['start']) 
def start(message):

    print('/start', '                             ', f'TIME: {time.asctime()}')

    kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Информатика', callback_data='инфа')
    btn2 = types.InlineKeyboardButton(text='Математика', callback_data='мат')
    btn3 = types.InlineKeyboardButton(text='Химия', callback_data='химия')
    btn4 = types.InlineKeyboardButton(text='Физика', callback_data='физика')
    kb.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, reply_markup=kb, text='Выберите предмет.')    
   
@bot.message_handler(commands=['get_instruction']) 
def do(message):
    print('/get_instruction', '                   ', f'TIME: {time.asctime()}')
    try:
        bot.send_photo(message.chat.id, open('img/howtoanswer.jpg', 'rb'), caption="Как отвечать на вопросы?")

    except requests.exceptions.ConnectionError:
        
        try:
            bot.send_message(message.chat.id, text='Что-то пошло не так. Повторите запрос.\nЕсли ошибка повторяется более 2 раз, сообщите об этом администратору.')

        except requests.exceptions.ConnectionError:
            bot.send_message(message.chat.id, text='Похоже, сервер telegram разорвал соединение, бот будет приостановлен. Сообщите администратору об ошибке.')
            bot.stop_polling()

@bot.message_handler(content_types=['text'])
def handle_message(message):
    global text_dict
    text_dict[message.chat.id] = message.text


@bot.callback_query_handler(func=lambda callback : callback.data)
def check_callback_data(callback):
    print(callback.data, '                   ', f'ID: {callback.message.chat.id} TIME:', time.asctime())
    try:
        if 'химия' in callback.data:
                global temp, message_id
                if 'химия/вышка' in callback.data: # готово! 

                    if 'химия/вышка/11' in callback.data: # сделано идеально!
                        
                        if callback.data == 'химия/вышка/11/ответ/да':
                            global res_a
                            res_a = QA_11_vi(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/вышка/11/вперед')
                            kb.add(btn12, btn5)
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                        elif callback.data == 'химия/вышка/11/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/вышка/11/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/вышка/11/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/вышка/11/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn3 = types.InlineKeyboardButton(text='9-10', callback_data='химия/вышка/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/вышка/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/вышка/назад')
                            kb.add(btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                        
                        elif callback.data == 'химия/вышка/11/вперед':
                            try:
                                res_q = QA_11_vi(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/11/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/11/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/11/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text=res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/11/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/вышка/11/ответ/нет':
                            res_q = QA_11_vi(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/11/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text=res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                
                        elif callback.data == 'химия/вышка/11':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text=QA_11_vi(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')  

                    elif 'химия/вышка/10' in callback.data: # готово!

                        if callback.data == 'химия/вышка/10/ответ/да':
                            res_a = QA_10_vi(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/вышка/10/вперед')
                            kb.add(btn12, btn5)
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                        elif callback.data == 'химия/вышка/10/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/вышка/10/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/вышка/10/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/вышка/10/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn3 = types.InlineKeyboardButton(text='9-10', callback_data='химия/вышка/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/вышка/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/вышка/назад')
                            kb.add(btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                        
                        elif callback.data == 'химия/вышка/10/вперед':
                            try:
                                res_q = QA_10_vi(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/10/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/10/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/10/ответ')
                                kb.add(btn1, btn5, btn3)

                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text=res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/10/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/вышка/10/ответ/нет':
                            res_q = QA_10_vi(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/10/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text=res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                
                        elif callback.data == 'химия/вышка/10':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/вышка/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/вышка/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/вышка/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text=QA_10_vi(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')  

                    elif 'химия/вышка/назад' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                        btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                        btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                        btn4 = types.InlineKeyboardButton(text='Газпром', callback_data='химия/газпром')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                        kb.add(btn1, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                            message_id=callback.message.id)

                    elif 'химия/вышка' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn3 = types.InlineKeyboardButton(text='9-10', callback_data='химия/вышка/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/вышка/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/вышка/назад')
                        kb.add(btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                
                elif 'химия/всош' in callback.data:

                    if 'химия/всош/11' in callback.data:
                        
                        if callback.data == 'химия/всош/11/ответ/да':
                            res_a = QA_11_vs(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/всош/11/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/всош/11/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/всош/11/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/всош/11/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/11/назад':
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='8-9', callback_data='химия/всош/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/всош/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/всош/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/всош/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/11/вперед':
                            try:
                                res_q = QA_11_vs(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/11/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/11/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/11/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/11/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/всош/11/ответ/нет':
                            res_q = QA_11_vs(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/11/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/всош/11':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_vs(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/всош/10' in callback.data:

                        if callback.data == 'химия/всош/10/ответ/да':
                            res_a = QA_10_vs(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/всош/10/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/всош/10/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/всош/10/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/всош/10/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/10/назад':
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='8-9', callback_data='химия/всош/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/всош/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/всош/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/всош/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/10/вперед':
                            try:
                                res_q = QA_10_vs(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/10/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/10/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/10/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/10/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/всош/10/ответ/нет':
                            res_q = QA_10_vs(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/10/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/всош/10':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_vs(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/всош/9' in callback.data:
                        
                        if callback.data == 'химия/всош/9/ответ/да':
                                res_a = QA_9_vs(callback)[0]
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/9/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/всош/9/вперед')
                                kb.add(btn12, btn5)
                                if '\n' in res_a[temp]:
                                    try:
                                        bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                        chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                    except:
                                        bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                        chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                else:
                                    try:
                                        bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                        chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                    except:
                                        bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                        chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                
                        elif callback.data == 'химия/всош/9/ответ':
                                kb = types.InlineKeyboardMarkup(row_width=1)
                                btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/всош/9/ответ/да')
                                btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/всош/9/ответ/нет')
                                kb.add(btn1, btn5)
                                bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/9/назад':
                                kb = types.InlineKeyboardMarkup(row_width=3)
                                btn2 = types.InlineKeyboardButton(text='8-9', callback_data='химия/всош/9')
                                btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/всош/10')
                                btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/всош/11')
                                btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/всош/назад')
                                kb.add(btn2, btn3, btn4, btn5)
                                bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/всош/9/вперед':
                                try:
                                    res_q = QA_9_vs(callback)[-1]
                                    temp += 1

                                    kb = types.InlineKeyboardMarkup(row_width=2)
                                    btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/9/назад')
                                    btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/9/вперед')
                                    btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/9/ответ')
                                    kb.add(btn1, btn5, btn3)
                                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                        message_id=callback.message.id, parse_mode='HTML')
                                    
                                except IndexError:
                                    kb = types.InlineKeyboardMarkup(row_width=2)
                                    btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/9/назад')
                                    kb.add(btn1)
                                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                        'наступает время, когда задачи исчерпываются. ' 
                                                        'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                        'что делать дальше.',
                                                        message_id=callback.message.id)
                            
                        elif callback.data == 'химия/всош/9/ответ/нет':
                                res_q = QA_9_vs(callback)[-1] 

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/9/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/9/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/9/ответ')
                                kb.add(btn1, btn5, btn3)

                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/всош/9':
                                temp = 0            
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/всош/9/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/всош/9/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/всош/9/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_vs(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                    
                        elif 'химия/всош/назад' in callback.data:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                            btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                            btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                            btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='химия/газпром')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                            kb.add(btn1, btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                                message_id=callback.message.id)

                        elif 'химия/всош' in callback.data:
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='8-9', callback_data='химия/всош/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/всош/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/всош/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/всош/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                    
                    elif 'химия/всош/назад' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                        btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                        btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                        btn4 = types.InlineKeyboardButton(text='Газпром', callback_data='химия/газпром')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                        kb.add(btn1, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                            message_id=callback.message.id)

                    elif 'химия/всош' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='8-9', callback_data='химия/всош/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/всош/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/всош/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                
                elif 'химия/лом' in callback.data:

                    if 'химия/лом/11' in callback.data:

                        if callback.data == 'химия/лом/11/ответ/да':
                            res_a = QA_11_lom(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/лом/11/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/лом/11/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/лом/11/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/лом/11/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/лом/11/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn2 = types.InlineKeyboardButton(text='5-9', callback_data='химия/лом/9')
                            btn4 = types.InlineKeyboardButton(text='10-11', callback_data='химия/лом/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/лом/назад')
                            kb.add(btn2, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/лом/11/вперед':
                            try:
                                res_q = QA_11_lom(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/11/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/11/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/11/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/11/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/лом/11/ответ/нет':
                            res_q = QA_11_lom(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/11/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/лом/11':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_lom(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/лом/9' in callback.data:

                        if callback.data == 'химия/лом/9/ответ/да':
                            res_a = QA_9_lom(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/лом/9/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/лом/9/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/лом/9/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/лом/9/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/лом/9/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn2 = types.InlineKeyboardButton(text='5-9', callback_data='химия/лом/9')
                            btn4 = types.InlineKeyboardButton(text='10-11', callback_data='химия/лом/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/лом/назад')
                            kb.add(btn2, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/лом/9/вперед':
                            try:
                                res_q = QA_9_lom(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/9/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/9/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/9/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/9/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/лом/9/ответ/нет':
                            res_q = QA_9_lom(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/9/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/лом/9':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/лом/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/лом/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/лом/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_lom(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/лом/назад' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                        btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                        btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                        btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='химия/газпром')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                        kb.add(btn1, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                            message_id=callback.message.id)

                    elif 'химия/лом' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn2 = types.InlineKeyboardButton(text='5-9', callback_data='химия/лом/9')
                        btn4 = types.InlineKeyboardButton(text='10-11', callback_data='химия/лом/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/лом/назад')
                        kb.add(btn2, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
                
                elif 'химия/газпром' in callback.data:

                    if 'химия/газпром/11' in callback.data:
                        
                        if callback.data == 'химия/газпром/11/ответ/да':
                            res_a = QA_11_gaz(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/газпром/11/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/газпром/11/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/газпром/11/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/газпром/11/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/11/назад':
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='9', callback_data='химия/газпром/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/газпром/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/газпром/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/газпром/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/11/вперед':
                            try:
                                res_q = QA_11_gaz(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/11/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/11/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/11/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/11/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/газпром/11/ответ/нет':
                            res_q = QA_11_gaz(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/11/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/газпром/11':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_gaz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/газпром/10' in callback.data:
                        
                        if callback.data == 'химия/газпром/10/ответ/да':
                            res_a = QA_10_gaz(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/газпром/10/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/газпром/10/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/газпром/10/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/газпром/10/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/10/назад':
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='9', callback_data='химия/газпром/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/газпром/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/газпром/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/газпром/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/10/вперед':
                            try:
                                res_q = QA_10_gaz(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/10/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/10/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/10/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/10/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/газпром/10/ответ/нет':
                            res_q = QA_10_gaz(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/10/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/газпром/10':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_gaz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/газпром/9' in callback.data:
                        
                        if callback.data == 'химия/газпром/9/ответ/да':
                            res_a = QA_9_gaz(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='химия/газпром/9/вперед')
                            kb.add(btn12, btn5)
                            if '\n' in res_a[temp]:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            else:
                                try:
                                    bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                except:
                                    bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                    chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'химия/газпром/9/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='химия/газпром/9/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='химия/газпром/9/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/9/назад':
                            kb = types.InlineKeyboardMarkup(row_width=3)
                            btn2 = types.InlineKeyboardButton(text='9', callback_data='химия/газпром/9')
                            btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/газпром/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/газпром/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/газпром/назад')
                            kb.add(btn2, btn3, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'химия/газпром/9/вперед':
                            try:
                                res_q = QA_9_gaz(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/9/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/9/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/9/ответ')
                                kb.add(btn1, btn5, btn3)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/9/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'химия/газпром/9/ответ/нет':
                            res_q = QA_9_gaz(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/9/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')

                        elif callback.data == 'химия/газпром/9':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='химия/газпром/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='химия/газпром/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='химия/газпром/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_gaz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'химия/газпром/назад' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                        btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                        btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                        btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='химия/газпром')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                        kb.add(btn1, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                            message_id=callback.message.id)

                    elif 'химия/газпром' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='химия/газпром/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='химия/газпром/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='химия/газпром/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/вышка/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                elif 'химия/назад' in callback.data: 
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='Информатика', callback_data='инфа')
                    btn2 = types.InlineKeyboardButton(text='Математика', callback_data='мат')
                    btn3 = types.InlineKeyboardButton(text='Химия', callback_data='химия')
                    btn4 = types.InlineKeyboardButton(text='Физика', callback_data='физика')
                    kb.add(btn1, btn2, btn3, btn4)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите предмет.',
                                                message_id=callback.message.id)
                
                else:          
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='химия/всош')
                    btn2 = types.InlineKeyboardButton(text='«Ломоносов»', callback_data='химия/лом')
                    btn3 = types.InlineKeyboardButton(text='«Высшая проба»', callback_data='химия/вышка')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='химия/газпром')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='химия/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

        elif 'физика' in callback.data:

            if 'физика/газпром' in callback.data:
                
                if 'физика/газпром/11' in callback.data:
                    
                    if callback.data == 'физика/газпром/11/ответ/да':
                        res_a = QA_11_gaz_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/газпром/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/газпром/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/газпром/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/газпром/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/газпром/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/газпром/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/газпром/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/газпром/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/11/вперед':
                        try:
                            res_q = QA_11_gaz_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/газпром/11/ответ/нет':
                        res_q = QA_11_gaz_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/газпром/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_gaz_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                    
                elif 'физика/газпром/10' in callback.data:
                                    
                    if callback.data == 'физика/газпром/10/ответ/да':
                        res_a = QA_10_gaz_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/газпром/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/газпром/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/газпром/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/газпром/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/газпром/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/газпром/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/газпром/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/газпром/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/10/вперед':
                        try:
                            res_q = QA_10_gaz_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/газпром/10/ответ/нет':
                        res_q = QA_10_gaz_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/газпром/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_gaz_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'физика/газпром/9' in callback.data:
                    
                    if callback.data == 'физика/газпром/9/ответ/да':
                        res_a = QA_9_gaz_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/газпром/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/газпром/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/газпром/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/газпром/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/газпром/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/газпром/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/газпром/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/газпром/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/газпром/9/вперед':
                        try:
                            res_q = QA_9_gaz_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/газпром/9/ответ/нет':
                        res_q = QA_9_gaz_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/газпром/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/газпром/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/газпром/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/газпром/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_gaz_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'физика/газпром/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='физика/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='физика/шаг')
                    btn3 = types.InlineKeyboardButton(text='«Физтех»', callback_data='физика/физтех')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='физика/газпром')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'физика/газпром' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=3)
                    btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/газпром/9')
                    btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/газпром/10')
                    btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/газпром/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/газпром/назад')
                    kb.add(btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'физика/всош' in callback.data:
                
                if 'физика/всош/11' in callback.data:
                    
                    if callback.data == 'физика/всош/11/ответ/да':
                        res_a = QA_11_vs_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/всош/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/всош/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/всош/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/всош/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/всош/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/всош/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/всош/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/всош/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/11/вперед':
                        try:
                            res_q = QA_11_vs_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/всош/11/ответ/нет':
                        res_q = QA_11_vs_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/всош/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_vs_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                    
                elif 'физика/всош/10' in callback.data:
                                    
                    if callback.data == 'физика/всош/10/ответ/да':
                        res_a = QA_10_vs_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/всош/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/всош/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/всош/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/всош/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/всош/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/всош/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/всош/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/всош/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/10/вперед':
                        try:
                            res_q = QA_10_vs_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/всош/10/ответ/нет':
                        res_q = QA_10_vs_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/всош/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_vs_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'физика/всош/9' in callback.data:
                    
                    if callback.data == 'физика/всош/9/ответ/да':
                        res_a = QA_9_vs_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/всош/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/всош/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/всош/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/всош/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/всош/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/всош/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/всош/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/всош/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/9/вперед':
                        try:
                            res_q = QA_9_vs_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/всош/9/ответ/нет':
                        res_q = QA_9_vs_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/всош/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_vs_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'физика/всош/8' in callback.data:
                    
                    if callback.data == 'физика/всош/8/ответ/да':
                        res_a = QA_8_vs_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/всош/8/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/всош/8/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/всош/8/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/всош/8/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/8/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/всош/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/всош/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/всош/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/всош/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/всош/8/вперед':
                        try:
                            res_q = QA_8_vs_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/8/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/8/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/8/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/8/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/всош/8/ответ/нет':
                        res_q = QA_8_vs_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/8/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/всош/8':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/всош/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/всош/8/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_8_vs_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'физика/всош/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='физика/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='физика/шаг')
                    btn3 = types.InlineKeyboardButton(text='«Физтех»', callback_data='физика/физтех')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='физика/газпром')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'физика/всош' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=4)
                    btn = types.InlineKeyboardButton(text='8', callback_data='физика/всош/8')
                    btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/всош/9')
                    btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/всош/10')
                    btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/всош/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/всош/назад')
                    kb.add(btn, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'физика/шаг' in callback.data:

                if 'физика/шаг/11' in callback.data:
                    
                    if callback.data == 'физика/шаг/11/ответ/да':
                        res_a = QA_11_shag(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/шаг/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/шаг/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/шаг/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/шаг/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/шаг/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/шаг/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/шаг/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/шаг/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/шаг/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/11/вперед':
                        try:
                            res_q = QA_11_shag(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/шаг/11/ответ/нет':
                        res_q = QA_11_shag(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/шаг/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_shag(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                    
                elif 'физика/шаг/10' in callback.data:
                                    
                    if callback.data == 'физика/шаг/10/ответ/да':
                        res_a = QA_10_shag(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/шаг/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/шаг/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/шаг/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/шаг/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/шаг/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/шаг/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/шаг/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/шаг/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/шаг/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/10/вперед':
                        try:
                            res_q = QA_10_shag(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/шаг/10/ответ/нет':
                        res_q = QA_10_shag(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/шаг/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_shag(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'физика/шаг/9' in callback.data:
                    
                    if callback.data == 'физика/шаг/9/ответ/да':
                        res_a = QA_9_shag(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/шаг/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/шаг/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/шаг/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/шаг/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/шаг/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/шаг/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/шаг/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/шаг/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/шаг/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/9/вперед':
                        try:
                            res_q = QA_9_shag(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/шаг/9/ответ/нет':
                        res_q = QA_9_shag(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/шаг/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_shag(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'физика/шаг/8' in callback.data:
                    
                    if callback.data == 'физика/шаг/8/ответ/да':
                        res_a = QA_8_shag(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/шаг/8/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/шаг/8/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/шаг/8/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/шаг/8/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/8/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn = types.InlineKeyboardButton(text='8', callback_data='физика/шаг/8')
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/шаг/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/шаг/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/шаг/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/шаг/назад')
                        kb.add(btn, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/шаг/8/вперед':
                        try:
                            res_q = QA_8_shag(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/8/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/8/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/8/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/8/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/шаг/8/ответ/нет':
                        res_q = QA_8_shag(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/8/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/шаг/8':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/шаг/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/шаг/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/шаг/8/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_8_shag(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'физика/шаг/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='физика/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='физика/шаг')
                    btn3 = types.InlineKeyboardButton(text='«Физтех»', callback_data='физика/физтех')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='физика/газпром')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'физика/шаг' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=4)
                    btn = types.InlineKeyboardButton(text='8', callback_data='физика/шаг/8')
                    btn2 = types.InlineKeyboardButton(text='9', callback_data='физика/шаг/9')
                    btn3 = types.InlineKeyboardButton(text='10', callback_data='физика/шаг/10')
                    btn4 = types.InlineKeyboardButton(text='11', callback_data='физика/шаг/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/шаг/назад')
                    kb.add(btn, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'физика/физтех' in callback.data:

                if 'физика/физтех/11' in callback.data:
                    
                    if callback.data == 'физика/физтех/11/ответ/да':
                        res_a = QA_11_tech_fiz(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='физика/физтех/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'физика/физтех/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='физика/физтех/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='физика/физтех/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'физика/физтех/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn4 = types.InlineKeyboardButton(text='9-11', callback_data='физика/физтех/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/физтех/назад')
                        kb.add(btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'физика/физтех/11/вперед':
                        try:
                            res_q = QA_11_tech_fiz(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/физтех/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/физтех/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/физтех/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/физтех/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'физика/физтех/11/ответ/нет':
                        res_q = QA_11_tech_fiz(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/физтех/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/физтех/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'физика/физтех/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='физика/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='физика/физтех/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='физика/физтех/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_tech_fiz(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                                
                elif 'физика/физтех/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='физика/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='физика/шаг')
                    btn3 = types.InlineKeyboardButton(text='«Физтех»', callback_data='физика/физтех')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='физика/газпром')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'физика/физтех' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=1)
                    btn4 = types.InlineKeyboardButton(text='9-11', callback_data='физика/физтех/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/физтех/назад')
                    kb.add(btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)
    
            elif 'физика/назад' in callback.data: 
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='Информатика', callback_data='инфа')
                    btn2 = types.InlineKeyboardButton(text='Математика', callback_data='мат')
                    btn3 = types.InlineKeyboardButton(text='Химия', callback_data='химия')
                    btn4 = types.InlineKeyboardButton(text='Физика', callback_data='физика')
                    kb.add(btn1, btn2, btn3, btn4)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите предмет.',
                                                message_id=callback.message.id)
                    
            else:          
                kb = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='физика/всош')
                btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='физика/шаг')
                btn3 = types.InlineKeyboardButton(text='«Физтех»', callback_data='физика/физтех')
                btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='физика/газпром')
                btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='физика/назад')
                kb.add(btn1, btn2, btn3, btn4, btn5)
                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                    message_id=callback.message.id) 

        elif 'инфа' in callback.data:

            if 'инфа/спб' in callback.data:
                
                if 'инфа/спб/11' in callback.data: # 7-11
                    
                    if callback.data == 'инфа/спб/11/ответ/да':
                        res_a = QA_11_SPB(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/спб/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='инфа/спб/11/вперед')
                        kb.add(btn12, btn5)
                        try:
                            bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        except:
                            bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'инфа/спб/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='инфа/спб/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='инфа/спб/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'инфа/спб/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/спб/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/спб/назад')
                        kb.add(btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'инфа/спб/11/вперед':
                        try:
                            res_q = QA_11_SPB(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/спб/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/спб/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/спб/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            try:
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except telebot.apihelper.ApiTelegramException:
                                res_q[temp] = html.escape(res_q[temp])
                                for i in range(0, len(res_q[temp]), 4098):
                                    bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp][i:i+4098], parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/спб/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'инфа/спб/11/ответ/нет':
                        res_q = QA_11_SPB(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/спб/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/спб/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/спб/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'инфа/спб/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/спб/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/спб/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/спб/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_SPB(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'инфа/спб/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='инфа/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='инфа/шаг')
                    btn3 = types.InlineKeyboardButton(text='СПбГУ', callback_data='инфа/спб')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='инфа/газ')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'инфа/спб' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=1)
                    btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/спб/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/спб/назад')
                    kb.add(btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'инфа/всош' in callback.data:
                
                if 'инфа/всош/11' in callback.data: # 7-11
                    
                    if callback.data == 'инфа/всош/11/ответ/да':
                        res_a = QA_11_vs_inf(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='инфа/всош/11/вперед')
                        kb.add(btn12, btn5)
                        try:
                            bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        except:
                            bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'инфа/всош/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='инфа/всош/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='инфа/всош/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'инфа/всош/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/всош/назад')
                        kb.add(btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'инфа/всош/11/вперед':
                        try:
                            res_q = QA_11_vs_inf(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/всош/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/всош/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            try:
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except telebot.apihelper.ApiTelegramException:
                                res_q[temp] = html.escape(res_q[temp])
                                for i in range(0, len(res_q[temp]), 4098):
                                    bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp][i:i+4098], parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/всош/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'инфа/всош/11/ответ/нет':
                        res_q = QA_11_vs_inf(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'инфа/всош/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_vs_inf(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'инфа/всош/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='инфа/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='инфа/шаг')
                    btn3 = types.InlineKeyboardButton(text='СПбГУ', callback_data='инфа/спб')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='инфа/газ')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'инфа/всош' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=1)
                    btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/всош/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/всош/назад')
                    kb.add(btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'инфа/шаг' in callback.data:
                    
                    if 'инфа/шаг/11' in callback.data: # 11
                        
                        if callback.data == 'инфа/шаг/11/ответ/да':
                            res_a = QA_11_shag_inf(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='инфа/шаг/11/вперед')
                            kb.add(btn12, btn5)
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'инфа/шаг/11/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='инфа/шаг/11/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='инфа/шаг/11/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'инфа/шаг/11/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn34 = types.InlineKeyboardButton(text='8-10', callback_data='инфа/шаг/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='инфа/шаг/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/шаг/назад')
                            kb.add(btn34, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'инфа/шаг/11/вперед':
                            try:
                                res_q = QA_11_shag_inf(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/11/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/11/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/11/ответ')
                                kb.add(btn1, btn5, btn3)
                                try:
                                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                        message_id=callback.message.id, parse_mode='HTML')
                                    
                                except telebot.apihelper.ApiTelegramException:
                                    res_q[temp] = html.escape(res_q[temp])
                                    for i in range(0, len(res_q[temp]), 4098):
                                        bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp][i:i+4098], parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/11/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                        'наступает время, когда задачи исчерпываются. ' 
                                                        'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                        'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'инфа/шаг/11/ответ/нет':
                            res_q = QA_11_shag_inf(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/11/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                    
                        elif callback.data == 'инфа/шаг/11':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_shag_inf(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'инфа/шаг/10' in callback.data: # 8-10
                        
                        if callback.data == 'инфа/шаг/10/ответ/да':
                            res_a = QA_10_shag_inf(callback)[0]
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='инфа/шаг/10/вперед')
                            kb.add(btn12, btn5)
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            
                        elif callback.data == 'инфа/шаг/10/ответ':
                            kb = types.InlineKeyboardMarkup(row_width=1)
                            btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='инфа/шаг/10/ответ/да')
                            btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='инфа/шаг/10/ответ/нет')
                            kb.add(btn1, btn5)
                            bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                        elif callback.data == 'инфа/шаг/10/назад':
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn34 = types.InlineKeyboardButton(text='8-10', callback_data='инфа/шаг/10')
                            btn4 = types.InlineKeyboardButton(text='11', callback_data='инфа/шаг/11')
                            btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/шаг/назад')
                            kb.add(btn34, btn4, btn5)
                            bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                        elif callback.data == 'инфа/шаг/10/вперед':
                            try:
                                res_q = QA_10_shag_inf(callback)[-1]
                                temp += 1

                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/10/назад')
                                btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/10/вперед')
                                btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/10/ответ')
                                kb.add(btn1, btn5, btn3)
                                try:
                                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                        message_id=callback.message.id, parse_mode='HTML')
                                    
                                except telebot.apihelper.ApiTelegramException:
                                    res_q[temp] = html.escape(res_q[temp])
                                    for i in range(0, len(res_q[temp]), 4098):
                                        bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp][i:i+4098], parse_mode='HTML')
                                
                            except IndexError:
                                kb = types.InlineKeyboardMarkup(row_width=2)
                                btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/10/назад')
                                kb.add(btn1)
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                        'наступает время, когда задачи исчерпываются. ' 
                                                        'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                        'что делать дальше.',
                                                    message_id=callback.message.id)
                        
                        elif callback.data == 'инфа/шаг/10/ответ/нет':
                            res_q = QA_10_shag_inf(callback)[-1] 

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/10/ответ')
                            kb.add(btn1, btn5, btn3)

                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                    
                        elif callback.data == 'инфа/шаг/10':
                            temp = 0            
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/шаг/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/шаг/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/шаг/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_shag_inf(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                    elif 'инфа/шаг/назад' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='инфа/всош')
                        btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='инфа/шаг')
                        btn3 = types.InlineKeyboardButton(text='СПбГУ', callback_data='инфа/спб')
                        btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='инфа/газ')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/назад')
                        kb.add(btn1, btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                            message_id=callback.message.id) 

                    elif 'инфа/шаг' in callback.data:
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn34 = types.InlineKeyboardButton(text='8-10', callback_data='инфа/шаг/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='инфа/шаг/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/шаг/назад')
                        kb.add(btn34, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'инфа/газ' in callback.data:
                
                if 'инфа/газ/11' in callback.data: # 7-11
                    
                    if callback.data == 'инфа/газ/11/ответ/да':
                        res_a = QA_11_gaz_inf(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/газ/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='инфа/газ/11/вперед')
                        kb.add(btn12, btn5)
                        try:
                            bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        except:
                            bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>К сожалению, конкретного правильного ответа на олимпиаду по информатике нет, так как участники пишут на разных языках программирования.(</b>',
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'инфа/газ/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='инфа/газ/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='инфа/газ/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'инфа/газ/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/газ/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/газ/назад')
                        kb.add(btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'инфа/газ/11/вперед':
                        try:
                            res_q = QA_11_gaz_inf(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/газ/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/газ/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/газ/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            try:
                                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                    message_id=callback.message.id, parse_mode='HTML')
                                
                            except telebot.apihelper.ApiTelegramException:
                                res_q[temp] = html.escape(res_q[temp])
                                for i in range(0, len(res_q[temp]), 4098):
                                    bot.send_message(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp][i:i+4098], parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/газ/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'инфа/газ/11/ответ/нет':
                        res_q = QA_11_gaz_inf(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/газ/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/газ/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/газ/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                
                    elif callback.data == 'инфа/газ/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='инфа/газ/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='инфа/газ/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='инфа/газ/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_gaz_inf(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
    
                elif 'инфа/газ/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='инфа/всош')
                    btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='инфа/шаг')
                    btn3 = types.InlineKeyboardButton(text='СПбГУ', callback_data='инфа/спб')
                    btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='инфа/газ')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id) 

                elif 'инфа/газ' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=1)
                    btn4 = types.InlineKeyboardButton(text='7-11', callback_data='инфа/газ/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/газ/назад')
                    kb.add(btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'инфа/назад' in callback.data: 
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='Информатика', callback_data='инфа')
                    btn2 = types.InlineKeyboardButton(text='Математика', callback_data='мат')
                    btn3 = types.InlineKeyboardButton(text='Химия', callback_data='химия')
                    btn4 = types.InlineKeyboardButton(text='Физика', callback_data='физика')
                    kb.add(btn1, btn2, btn3, btn4)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите предмет.',
                                                message_id=callback.message.id)
                    
            else:          
                kb = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(text='ВсОШ', callback_data='инфа/всош')
                btn2 = types.InlineKeyboardButton(text='«Шаг в будущее»', callback_data='инфа/шаг')
                btn3 = types.InlineKeyboardButton(text='СПбГУ', callback_data='инфа/спб')
                btn4 = types.InlineKeyboardButton(text='«Газпром»', callback_data='инфа/газ')
                btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='инфа/назад')
                kb.add(btn1, btn2, btn3, btn4, btn5)
                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                    message_id=callback.message.id)

        elif 'мат' in callback.data:

            if 'мат/росатом' in callback.data:
                
                if 'мат/росатом/11' in callback.data:
                    
                    if callback.data == 'мат/росатом/11/ответ/да':
                        res_a = QA_11_ros(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/росатом/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/росатом/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/росатом/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/росатом/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='мат/росатом/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='мат/росатом/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='мат/росатом/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/росатом/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/11/вперед':
                        try:
                            res_q = QA_11_ros(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/росатом/11/ответ/нет':
                        res_q = QA_11_ros(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/росатом/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_ros(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/росатом/10' in callback.data:
                    
                    if callback.data == 'мат/росатом/10/ответ/да':
                        res_a = QA_10_ros(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/росатом/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/росатом/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/росатом/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/росатом/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='мат/росатом/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='мат/росатом/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='мат/росатом/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/росатом/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/10/вперед':
                        try:
                            res_q = QA_10_ros(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/росатом/10/ответ/нет':
                        res_q = QA_10_ros(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/росатом/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_ros(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/росатом/9' in callback.data:
                    
                    if callback.data == 'мат/росатом/9/ответ/да':
                        res_a = QA_9_ros(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/росатом/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/росатом/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/росатом/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/росатом/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn2 = types.InlineKeyboardButton(text='9', callback_data='мат/росатом/9')
                        btn3 = types.InlineKeyboardButton(text='10', callback_data='мат/росатом/10')
                        btn4 = types.InlineKeyboardButton(text='11', callback_data='мат/росатом/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/росатом/назад')
                        kb.add(btn2, btn3, btn4, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/росатом/9/вперед':
                        try:
                            res_q = QA_9_ros(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/росатом/9/ответ/нет':
                        res_q = QA_9_ros(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/росатом/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/росатом/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/росатом/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/росатом/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_ros(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/росатом/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='«Росатом»', callback_data='мат/росатом')
                    btn2 = types.InlineKeyboardButton(text='«Физтех»', callback_data='мат/физтех')
                    btn3 = types.InlineKeyboardButton(text='ММО', callback_data='мат/ммо')
                    btn4 = types.InlineKeyboardButton(text='ВсОШ', callback_data='мат/всош')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id)

                elif 'мат/росатом' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=3)
                    btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/росатом/9')
                    btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/росатом/10')
                    btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/росатом/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/росатом/назад')
                    kb.add(btn9, btn10, btn11, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'мат/всош' in callback.data:
            
                if 'мат/всош/11' in callback.data:
                    
                    if callback.data == 'мат/всош/11/ответ/да':
                        res_a = QA_11_vs_mat(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/всош/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/всош/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/всош/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/всош/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn19 = types.InlineKeyboardButton(text='8', callback_data='мат/всош/8')
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/всош/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/всош/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/всош/назад')
                        kb.add(btn19, btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/11/вперед':
                        try:
                            res_q = QA_11_vs_mat(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/всош/11/ответ/нет':
                        res_q = QA_11_vs_mat(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/всош/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_vs_mat(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/всош/10' in callback.data:
                    
                    if callback.data == 'мат/всош/10/ответ/да':
                        res_a = QA_10_vs_mat(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/всош/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/всош/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/всош/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/всош/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn19 = types.InlineKeyboardButton(text='8', callback_data='мат/всош/8')
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/всош/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/всош/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/всош/назад')
                        kb.add(btn19, btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/10/вперед':
                        try:
                            res_q = QA_10_vs_mat(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/всош/10/ответ/нет':
                        res_q = QA_10_vs_mat(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/всош/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_vs_mat(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/всош/9' in callback.data:
                    
                    if callback.data == 'мат/всош/9/ответ/да':
                        res_a = QA_9_vs_mat(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/всош/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/всош/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/всош/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/всош/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn19 = types.InlineKeyboardButton(text='8', callback_data='мат/всош/8')
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/всош/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/всош/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/всош/назад')
                        kb.add(btn19, btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/9/вперед':
                        try:
                            res_q = QA_9_vs_mat(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/всош/9/ответ/нет':
                        res_q = QA_9_vs_mat(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/всош/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_vs_mat(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'мат/всош/8' in callback.data:
                    
                    if callback.data == 'мат/всош/8/ответ/да':
                        res_a = QA_8_vs_mat(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/всош/8/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/всош/8/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/всош/8/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/всош/8/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/8/назад':
                        kb = types.InlineKeyboardMarkup(row_width=4)
                        btn19 = types.InlineKeyboardButton(text='8', callback_data='мат/всош/8')
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/всош/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/всош/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/всош/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/всош/назад')
                        kb.add(btn19, btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/всош/8/вперед':
                        try:
                            res_q = QA_8_vs_mat(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/8/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/8/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/8/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/8/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/всош/8/ответ/нет':
                        res_q = QA_8_vs_mat(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/8/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/всош/8':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/8/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/всош/8/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/всош/8/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_8_vs_mat(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/всош/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='«Росатом»', callback_data='мат/росатом')
                    btn2 = types.InlineKeyboardButton(text='«Физтех»', callback_data='мат/физтех')
                    btn3 = types.InlineKeyboardButton(text='ММО', callback_data='мат/ммо')
                    btn4 = types.InlineKeyboardButton(text='ВсОШ', callback_data='мат/всош')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id)

                elif 'мат/всош' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=4)
                    btn19 = types.InlineKeyboardButton(text='8', callback_data='мат/всош/8')
                    btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/всош/9')
                    btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/всош/10')
                    btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/всош/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/всош/назад')
                    kb.add(btn19, btn9, btn10, btn11, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'мат/физтех' in callback.data:
                
                if 'мат/физтех/11' in callback.data:
                    
                    if callback.data == 'мат/физтех/11/ответ/да':
                        res_a = QA_11_fiztech(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/физтех/11/вперед')
                        kb.add(btn12, btn5)
                        try:
                            bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        except:
                            bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                            chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                        
                    
                    elif callback.data == 'мат/физтех/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/физтех/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/физтех/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/физтех/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/физтех/9')
                        btn11 = types.InlineKeyboardButton(text='10-11', callback_data='мат/физтех/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/физтех/назад')
                        kb.add(btn9, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/физтех/11/вперед':
                        try:
                            res_q = QA_11_fiztech(callback)[-1]
                            temp += 1
                            r = html.escape(res_q[temp])
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + r,
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/физтех/11/ответ/нет':
                        res_q = QA_11_fiztech(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/физтех/11':
                        temp = 0 
                        r = html.escape(QA_11_fiztech(callback)[1][0])           
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + r, chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/физтех/9' in callback.data:
                    
                    if callback.data == 'мат/физтех/9/ответ/да':
                        res_a = QA_9_fiztech(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/всош/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/всош/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/физтех/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/физтех/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/физтех/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/физтех/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/физтех/9')
                        btn11 = types.InlineKeyboardButton(text='10-11', callback_data='мат/физтех/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/физтех/назад')
                        kb.add(btn9, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/физтех/9/вперед':
                        try:
                            res_q = QA_9_fiztech(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/физтех/9/ответ/нет':
                        res_q = QA_9_fiztech(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/физтех/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/физтех/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/физтех/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/физтех/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_fiztech(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/физтех/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='«Росатом»', callback_data='мат/росатом')
                    btn2 = types.InlineKeyboardButton(text='«Физтех»', callback_data='мат/физтех')
                    btn3 = types.InlineKeyboardButton(text='ММО', callback_data='мат/ммо')
                    btn4 = types.InlineKeyboardButton(text='ВсОШ', callback_data='мат/всош')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id)

                elif 'мат/физтех' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/физтех/9')
                    btn11 = types.InlineKeyboardButton(text='10-11', callback_data='мат/физтех/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/физтех/назад')
                    kb.add(btn9, btn11, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'мат/ммо' in callback.data:
                
                if 'мат/ммо/11' in callback.data:
                    
                    if callback.data == 'мат/ммо/11/ответ/да':
                        res_a = QA_11_MMO(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/ммо/11/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/ммо/11/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/ммо/11/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/ммо/11/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/11/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/ммо/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/ммо/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/ммо/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/ммо/назад')
                        kb.add(btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/11/вперед':
                        try:
                            res_q = QA_11_MMO(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/11/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/11/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/11/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/11/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/ммо/11/ответ/нет':
                        res_q = QA_11_MMO(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/11/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/ммо/11':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/11/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/11/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/11/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_11_MMO(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/ммо/10' in callback.data:
                    
                    if callback.data == 'мат/ммо/10/ответ/да':
                        res_a = QA_10_MMO(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/ммо/10/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/ммо/10/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/ммо/10/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/ммо/10/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/10/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/ммо/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/ммо/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/ммо/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/ммо/назад')
                        kb.add(btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/10/вперед':
                        try:
                            res_q = QA_10_MMO(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/10/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/10/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/10/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/10/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/ммо/10/ответ/нет':
                        res_q = QA_10_MMO(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/10/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/ммо/10':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/10/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/10/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/10/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_10_MMO(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')

                elif 'мат/ммо/9' in callback.data:
                    
                    if callback.data == 'мат/ммо/9/ответ/да':
                        res_a = QA_9_MMO(callback)[0]
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn12 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️ ', callback_data='мат/ммо/9/вперед')
                        kb.add(btn12, btn5)
                        if '\n' in res_a[temp]:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильные ответы :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        else:
                            try:
                                bot.send_message(text=f'<b>Ваш ответ : </b>{text_dict[callback.message.chat.id]}\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                            except:
                                bot.send_message(text=f'<b>Ваш ответ : </b> Oтвета нет\n' + '<b>Правильный ответ :</b>' + res_a[temp],
                                                chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                        
                    elif callback.data == 'мат/ммо/9/ответ':
                        kb = types.InlineKeyboardMarkup(row_width=1)
                        btn1 = types.InlineKeyboardButton(text='Абсолютно', callback_data='мат/ммо/9/ответ/да')
                        btn5 = types.InlineKeyboardButton(text='Не очень', callback_data='мат/ммо/9/ответ/нет')
                        kb.add(btn1, btn5)
                        bot.send_message(text='Вы уверены?', chat_id=callback.message.chat.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/9/назад':
                        kb = types.InlineKeyboardMarkup(row_width=3)
                        btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/ммо/9')
                        btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/ммо/10')
                        btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/ммо/11')
                        btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/ммо/назад')
                        kb.add(btn9, btn10, btn11, btn5)
                        bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

                    elif callback.data == 'мат/ммо/9/вперед':
                        try:
                            res_q = QA_9_MMO(callback)[-1]
                            temp += 1

                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/9/назад')
                            btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/9/вперед')
                            btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/9/ответ')
                            kb.add(btn1, btn5, btn3)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                                message_id=callback.message.id, parse_mode='HTML')
                            
                        except IndexError:
                            kb = types.InlineKeyboardMarkup(row_width=2)
                            btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/9/назад')
                            kb.add(btn1)
                            bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Среди серых облаков дней, '
                                                    'наступает время, когда задачи исчерпываются. ' 
                                                    'Все, что остается - пустое пространство, заполненное бездействием и неведением о том, '
                                                    'что делать дальше.',
                                                message_id=callback.message.id)
                    
                    elif callback.data == 'мат/ммо/9/ответ/нет':
                        res_q = QA_9_MMO(callback)[-1] 

                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/9/ответ')
                        kb.add(btn1, btn5, btn3)

                        bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='<b>Вопрос : \n</b>' + res_q[temp],
                                            message_id=callback.message.id, parse_mode='HTML')
                    
                    elif callback.data == 'мат/ммо/9':
                        temp = 0            
                        kb = types.InlineKeyboardMarkup(row_width=2)
                        btn1 = types.InlineKeyboardButton(text='Назад ⬅️', callback_data='мат/ммо/9/назад')
                        btn5 = types.InlineKeyboardButton(text='Вперед ➡️', callback_data='мат/ммо/9/вперед')
                        btn3 = types.InlineKeyboardButton(text='Ответить', callback_data='мат/ммо/9/ответ')
                        kb.add(btn1, btn5, btn3)
                        bot.send_message(text='<b>Вопрос : \n</b>' + QA_9_MMO(callback)[1][0], chat_id=callback.message.chat.id, reply_markup=kb, parse_mode='HTML')
                
                elif 'мат/ммо/назад' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='«Росатом»', callback_data='мат/росатом')
                    btn2 = types.InlineKeyboardButton(text='«Физтех»', callback_data='мат/физтех')
                    btn3 = types.InlineKeyboardButton(text='ММО', callback_data='мат/ммо')
                    btn4 = types.InlineKeyboardButton(text='ВсОШ', callback_data='мат/всош')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/назад')
                    kb.add(btn1, btn2, btn3, btn4, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                        message_id=callback.message.id)

                elif 'мат/ммо' in callback.data:
                    kb = types.InlineKeyboardMarkup(row_width=3)
                    btn9 = types.InlineKeyboardButton(text='9', callback_data='мат/ммо/9')
                    btn10 = types.InlineKeyboardButton(text='10', callback_data='мат/ммо/10')
                    btn11 = types.InlineKeyboardButton(text='11', callback_data='мат/ммо/11')
                    btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/ммо/назад')
                    kb.add(btn9, btn10, btn11, btn5)
                    bot.edit_message_text(chat_id=callback.message.chat.id, text='Выберите класс участия.', message_id=callback.message.id, reply_markup=kb)

            elif 'мат/назад' in callback.data: 
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton(text='Информатика', callback_data='инфа')
                    btn2 = types.InlineKeyboardButton(text='Математика', callback_data='мат')
                    btn3 = types.InlineKeyboardButton(text='Химия', callback_data='химия')
                    btn4 = types.InlineKeyboardButton(text='Физика', callback_data='физика')
                    kb.add(btn1, btn2, btn3, btn4)
                    bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите предмет.',
                                                message_id=callback.message.id)
                    
            else:          
                kb = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(text='«Росатом»', callback_data='мат/росатом')
                btn2 = types.InlineKeyboardButton(text='«Физтех»', callback_data='мат/физтех')
                btn3 = types.InlineKeyboardButton(text='ММО', callback_data='мат/ммо')
                btn4 = types.InlineKeyboardButton(text='ВсОШ', callback_data='мат/всош')
                btn5 = types.InlineKeyboardButton(text='⬅️', callback_data='мат/назад')
                kb.add(btn1, btn2, btn3, btn4, btn5)
                bot.edit_message_text(chat_id=callback.message.chat.id, reply_markup=kb, text='Выберите олимпиаду.',
                                    message_id=callback.message.id)

    except Exception as e:
        logging.error(e)




       

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        time.sleep(15)