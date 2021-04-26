import sqlite3
import random

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import TOKEN


class Bot:
    def __init__(self):
        self.updater = Updater(TOKEN, use_context=True)
        self.dp = self.updater.dispatcher

    def start(self, update, context):
        reply_keyboard = [['Давай начнём!']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Привет! Я ПепеБот. Я могу предложить тебе незабываемое путешествие, в котором будет полно опасностей и "
            "препятствий, но, проявив смекалку, выдержку и здравомыслие, ты сможешь пройти до конца и получить "
            "достойную награду!\nНу что, начнём?", reply_markup=markup)

    def help(self, update, context):
        update.message.reply_text(
            "Я отправлю тебя в захватывающее приключение, где ты встретишься со смертельными головоломками, "
            "опаснейшими ловушками и нелёгким выбором. Только рассудительный и хдаднокровный сможет дойти до главной "
            "цели, получив то, что он заслуживает!")

    def close_keyboard(self, update, context):
        update.message.reply_text(
            "",
            reply_markup=ReplyKeyboardRemove()
        )

    def set_timer(self, update, context):
        chat_id = update.message.chat_id
        try:
            due = 30

            job_removed = self.remove_job_if_exists(
                str(chat_id),
                context
            )
            context.job_queue.run_once(
                self.task,
                due,
                context=chat_id,
                name=str(chat_id)
            )

            text = 'Время пошло!'
            update.message.reply_text(text)

        except (IndexError, ValueError):
            update.message.reply_text('Ошибка: использование: /set <секунд>')

    def unset_timer(self, update, context):
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)

    def remove_job_if_exists(self, name, context):
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    def first_level(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question, name FROM levels WHERE level = 0""").fetchall()

        random_n = random.randint(0, 4)
        question, question_name = result[random_n][0], result[random_n][1]

        tips = self.cursor.execute("""SELECT tip FROM tips WHERE name = ?""", (question_name,)).fetchall()

        reply_keyboard = [tips[0][0].split(',')]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(question, reply_markup=markup)

        self.db.close()

    def second_level(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question, name FROM levels WHERE level = 1""").fetchall()

        random_n = random.randint(0, 2)
        question, question_name = result[random_n][0], result[random_n][1]

        tips = self.cursor.execute("""SELECT tip FROM tips WHERE name = ?""", (question_name,)).fetchall()

        reply_keyboard = [tips[0][0].split(',')]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(question, reply_markup=markup)

        self.db.close()

    def third_level(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question, name FROM levels WHERE level = 2""").fetchall()

        random_n = random.randint(0, 2)
        question, question_name = result[random_n][0], result[random_n][1]

        tips = self.cursor.execute("""SELECT tip FROM tips WHERE name = ?""", (question_name,)).fetchall()

        reply_keyboard = [tips[0][0].split(',')]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(question, reply_markup=markup)

        self.db.close()

    def fourth_level(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question, name FROM levels WHERE level = 3""").fetchall()

        random_n = 0
        question, question_name = result[random_n][0], result[random_n][1]

        tips = self.cursor.execute("""SELECT tip FROM tips WHERE name = ?""", (question_name,)).fetchall()

        reply_keyboard = [tips[0][0].split(',')]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(question, reply_markup=markup)

        self.db.close()

    def ending(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question FROM levels WHERE level = 5""").fetchall()

        text = result[0][0]

        reply_keyboard = [['Начать заново']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(text, reply_markup=markup)

        self.db.close()

    def death(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        random_n = random.randint(0, 5)

        result = self.cursor.execute("""SELECT answer FROM dead_answers""").fetchall()
        text = result[random_n][0]

        reply_keyboard = [['Начать заново']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(text, reply_markup=markup)

        self.db.close()

    def task(self, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        job = context.job
        random_n = random.randint(0, 5)

        result = self.cursor.execute("""SELECT answer FROM dead_answers""").fetchall()
        text = 'Время вышло! ' + result[random_n][0]

        context.bot.send_message(job.context, text=text)

        self.db.close()

    def exit(self, update, context):
        self.db = sqlite3.connect("questions.db")
        self.cursor = self.db.cursor()

        result = self.cursor.execute("""SELECT question FROM levels WHERE level = 6""").fetchall()

        text = result[0][0]

        reply_keyboard = [['Начать заново']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(text, reply_markup=markup)

        self.db.close()


if __name__ == "__main__":
    bot = Bot()

    bot.dp.add_handler(CommandHandler("start", bot.start))
    bot.dp.add_handler(CommandHandler("help", bot.help))
    bot.dp.add_handler(CommandHandler("close", bot.close_keyboard))
    bot.dp.add_handler(CommandHandler("first_level", bot.first_level))
    bot.dp.add_handler(CommandHandler("second_level", bot.second_level))
    bot.dp.add_handler(CommandHandler("third_level", bot.third_level))
    bot.dp.add_handler(CommandHandler("fourth_level", bot.fourth_level))
    bot.dp.add_handler(CommandHandler("exit", bot.exit))
    bot.dp.add_handler(CommandHandler("ending", bot.ending))
    bot.dp.add_handler(CommandHandler("death", bot.death))
    bot.dp.add_handler(CommandHandler("set", bot.set_timer,
                                      pass_args=True,
                                      pass_job_queue=True,
                                      pass_chat_data=True))
    bot.dp.add_handler(CommandHandler("unset", bot.unset_timer,
                                      pass_chat_data=True))

    bot.updater.start_polling()
    bot.updater.idle()
