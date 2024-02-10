import os
from dotenv import load_dotenv
import telebot
from telebot import types
import django
django.setup()
from django.core.exceptions import AppRegistryNotReady 
from shop.models import Category, Product, Order
from user.models import User

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

praduct_data = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user_id = str(message.from_user.id)
        user_exists = User.objects.all()
        user_all = [str(i.user_id) for i in user_exists]
        if user_id not in user_all:
            new_user = User(user_id=user_id, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
            new_user.save()

        menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        categorys = Category.objects.all()

        for i in categorys:
            buttons.append(types.InlineKeyboardButton(text=i.name, callback_data=f"category_{i.id}"))
            if len(buttons) % 2 == 0:  # Qatorga tugmalar chiqarish uchun
                menu_keyboard.add(*buttons)
                buttons = []
        menu_keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum! Bo'limlardan birini tanlang:", reply_markup=menu_keyboard)
    except AppRegistryNotReady:
        pass

    
@bot.message_handler(commands=['add_product'])
def handle_add_product(message):
 
    user_id = str(message.from_user.id)
    try:
        user= User.objects.get(user_id=user_id)
        if user.position == "ADMIN" and user.is_identified == True:
            menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            categorys = Category.objects.all()
            for i in categorys:
                buttons.append(types.InlineKeyboardButton(text=i.name, callback_data=f"adproduct_{i.id}"))
                if len(buttons) % 2 == 0:  
                    menu_keyboard.add(*buttons)
                    buttons = []
            menu_keyboard.add(*buttons)
            bot.send_message(user_id, "Product qo'shmoqchi bo'lgan  bo'limni tanlang:", reply_markup=menu_keyboard)
        else:
            bot.send_message(user_id, "Siz admin emasiz!")
    except:
        
        bot.send_message(user_id, "Nimadir xato ketdi! ")

    
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    user_id = call.from_user.id

    if call.data.startswith('category'):
        category_id = call.data.split('_')[1]
        praducts = Product.objects.filter(category_id=category_id)
        bot.send_message(user_id, "Maxsulotni Tanlang:")
        for i in praducts:
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton("Sotib olish 📥", callback_data=f"order_{i.id}"),
                types.InlineKeyboardButton('⬅️ orqaga', callback_data="orqa"),
            ]
            markup.add(*buttons)
            bot.send_photo(user_id, photo=i.image, caption=f"Maxsulot: {i.name}\nTavsifi: {i.discrton}\nNarxi: {i.price} so'm", reply_markup=markup)
        
    elif call.data == "orqa":
        menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        categorys = Category.objects.all()

        for i in categorys:
            buttons.append(types.InlineKeyboardButton(text=i.name, callback_data=f"category_{i.id}"))
            if len(buttons) % 2 == 0: 
                menu_keyboard.add(*buttons)
                buttons = []
        menu_keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum! Bo'limlardan birini tanlang:", reply_markup=menu_keyboard)

    elif call.data.startswith('adproduct_'):
        category_id = call.data.split('_')[1]
        praduct_data[user_id]={"category":category_id}
        bot.send_message(user_id, "Produkt nomini kirting: ")
        bot.register_next_step_handler(call.message, get_praduct_name)
    
    elif call.data.startswith("order_"):
        product_id = call.data.split('_')[1]
        product = Product.objects.get(id=product_id)
        user = User.objects.get(user_id=user_id)
        order = Order.objects.create(
            product_id = product,
            user_id=user,
            price = product.price
        )
        order.save()
        bot.send_message(user_id, "Mahsulot muvofaqiyatli sotib olindi!!")

        menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        categorys = Category.objects.all()

        for i in categorys:
            buttons.append(types.InlineKeyboardButton(text=i.name, callback_data=f"category_{i.id}"))
            if len(buttons) % 2 == 0: 
                menu_keyboard.add(*buttons)
                buttons = []
        menu_keyboard.add(*buttons)
        bot.send_message(user_id, "Assalomu alaykum! Bo'limlardan birini tanlang:", reply_markup=menu_keyboard)
        
def get_praduct_name(message):
    user_id = message.from_user.id
    praduct_data[user_id]["name"]=message.text
    bot.send_message(user_id, "Product haqida ma'lumot kirting: ")
    bot.register_next_step_handler(message, get_praduct_tafsif)

def get_praduct_tafsif(message):
    user_id = message.from_user.id
    praduct_data[user_id]["tafsif"]=message.text
    bot.send_message(user_id, "Product narxini kirting: ")
    bot.register_next_step_handler(message, get_praduct_narx)

def get_praduct_narx(message):
    user_id = message.from_user.id
    praduct_data[user_id]["narx"]=message.text
    bot.send_message(user_id, "Product rasimini yuboring: ")
    bot.register_next_step_handler(message, get_product_rasim)  

def get_product_rasim(message):
    user_id = message.from_user.id

    # Rasmni tanlash
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = os.path.join("media","image", f"{file_id}.jpg")
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, "wb") as new_file:
            new_file.write(downloaded_file)
        
        category = Category.objects.get(id=praduct_data[int(user_id)]["category"])
        product = Product.objects.create(
            name=praduct_data[int(user_id)]["name"],
            discrton=praduct_data[int(user_id)]["tafsif"],
            price=float(praduct_data[int(user_id)]["narx"]),
            category_id=category,
            image=f"image/{file_id}.jpg"
        )
        product.save()
    else:
        print("Rasm topilmadi.")
    bot.send_message(user_id, "Produk muvofaqiyatli qo'shildi!")
    del praduct_data[int(user_id)]
    menu_keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    categorys = Category.objects.all()

    for i in categorys:
        buttons.append(types.InlineKeyboardButton(text=i.name, callback_data=f"category_{i.id}"))
        if len(buttons) % 2 == 0: 
            menu_keyboard.add(*buttons)
            buttons = []
    menu_keyboard.add(*buttons)
    bot.send_message(user_id, "Assalomu alaykum! Bo'limlardan birini tanlang:", reply_markup=menu_keyboard)

bot.polling()