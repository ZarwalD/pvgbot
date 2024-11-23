import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
from vk_api.utils import get_random_id
import sqlite3
import random
from datetime import datetime, timedelta
import re
import configparser
import math
import pytz
import os.path
import sys
import traceback
import matplotlib.pyplot as plt
from SVOFinder import SVOFinder

print('=====\nPVG Mining Bot')

config = configparser.ConfigParser()
config.read(r'config.ini', encoding='utf-8')

ADMMA = None
MINE_WAIT_HOURS = None
MINE_LVL_SAFRYLUS = None
WORK_WAIT_HOURS = None
FACTORIES_AMOUNT_RESOURCES = None
COUNTRIES_LIST_MAX = None
MINERS_LIST_MAX = None
WORKERS_LIST_MAX = None
MINE_PRICES = None
FACTORY_PRICE = None
CITIES_PRICES = None
AUCTION_LIST_MAX = None
ECONOMICS_LIST_MAX = None
WAR_LIST_MAX = None
SANCTIONS_TO_LIST_MAX = None
SANCTIONS_FROM_LIST_MAX = None
MAPS_MAX_AMOUNT = None
EASTER = None
WAR_MOVE_COOLDOWN_HOUR = None
EXCHANGE_UPDATE_COOLDOWN_HOUR = None
CITIES_LIMITS_AREAS = None

random.seed(datetime.now().timestamp())
db = None # type: sqlite3.Connection
try:
	db = sqlite3.connect(r'pvg.db')
except:
	sys.exit('database connection failed')
print('database connected')
cur = db.cursor() # type: sqlite3.Cursor
cur.execute # type: sqlite3.Cursor

sqlite3.enable_callback_tracebacks(True)

def functionRegex(value, pattern):
	c_pattern = re.compile(pattern)
	result = c_pattern.search(str(value))
	if result != None:
		return result.group()
	return ''

db.create_function("REGEXP", 2, functionRegex)

cur.execute('')
db.commit()
bot_about_db = cur.execute('').fetchall()

print(f'Version: {bot_about_db[0][0]}.{bot_about_db[0][1]}.{bot_about_db[0][2]}.{bot_about_db[0][3]}')

token = config['Secrets']['token']
id = config['Secrets']['id']
vk_session = vk_api.VkApi(token=token)
print('vk session connected')
longpoll = VkBotLongPoll(vk_session, id)
print('vk bot longpoll connected')
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)
print('=====')

def text_to_bool(text):
	return text.lower() in ('true')

def sendm(peer_id, message):
	vk.messages.send(
		random_id=get_random_id(),
		peer_id=peer_id,
		message=message
	)

def sendr(peer_id, forward, message):
	vk.messages.send(
		random_id=get_random_id(),
		peer_id=peer_id,
		forward=forward,
		message=message
	)

def sendma(peer_id, message, attachment):
	vk.messages.send(
		random_id=get_random_id(),
		peer_id=peer_id,
		attachment=attachment,
		message=message
	)
	
def sendu(user_id, message):
	vk.messages.send(
		random_id=get_random_id(),
		user_id=user_id,
		message=message
	)

def is_admin_of_bot(from_id) -> bool:
	bot_admins = vk.groups.getById(group_id = 'vcplanet', fields='contacts')[0]['contacts']
	for user in bot_admins:
		if user['user_id'] == from_id:
			try:
				if user['desc'] == '[БОТ] Администратор':
					return True
			except:
				return False
	return False

def is_admin(peer_id: int, from_id: int) -> bool:
	users = vk.messages.getConversationMembers(peer_id=peer_id)['items']
	for user in users:
		if user['member_id'] == from_id:
			if user.get('is_admin', False):
				return True
			else:
				return False
	return False

def is_moder(peer_id: int, from_id: int) -> bool:
	return bool(cur.execute('').fetchall())

def miner_exists(peer_id: int, from_id: int) -> bool:
	user_data = cur.execute('').fetchall()
	if user_data == []:
		return False
	return True

def get_now_string():
	return datetime.strftime(datetime.now(pytz.timezone('Europe/Moscow')), '%d/%m/%Y')

def get_now_date():
	return datetime.strptime(get_now_string(), '%d/%m/%Y').date()
	
def get_now_time_string():
	result = datetime.now(pytz.timezone('Europe/Moscow'))
	result = result.replace(tzinfo=None, microsecond=0)
	result = result.isoformat(timespec='seconds')
	return result
def get_now_time_nondate():
	return datetime.fromisoformat(get_now_time_string()).replace(microsecond=0)

def get_name(uid) -> str:
	data = vk.users.get(user_ids = uid)[0]
	name = data['first_name'].replace('\'', '')
	last = data['last_name'].replace('\'', '')
	return f"{name} {last}"

def get_country_name(cid) -> str:
	name = cur.execute('').fetchall()
	if name == []:
		return 'Ошибка'
	return name[0][0]

def upload_photo(photo):
	response = upload.photo_messages(photo)[0]
	owner_id = response['owner_id']
	photo_id = response['id']
	access_key = response['access_key']
	return owner_id, photo_id, access_key
	
def parse_id(cid):
	result = cur.execute('').fetchall()
	if result == []:
		return None
	return result[0][0]

def shorten_id(cid):
	return int(re.sub(r'^20+(?#[0-9]+)', '', str(cid)))

def get_id(scid):
	max_id = 10
	scid_len = len(str(scid))
	out_str = '2'
	for i in range(0,max_id-scid_len-1):
		out_str += '0'
	out_str += str(scid)
	return int(out_str)

def get_price_update(old_price=50):
	mul = random.randint(90, 110)/100
	return old_price-(old_price*mul)

def get_active_miners(offset=0, type='день'):
	countries_ids = cur.execute('').fetchall()
	exec_pattern = ''
	if type == 'день':
		exec_pattern = ""
	if type == 'неделя':
		exec_pattern = ""
	if type == 'месяц':
		exec_pattern = ""
	miners_list = []
	count = offset
	id = 0
	for country_id in countries_ids:
		miners_list.append(cur.execute('').fetchall()[0])
		count += 1
		id += 1
	return miners_list

block = text_to_bool(cur.execute('').fetchall()[0][0])

army_type_enum = {
	"пехота": "INFANTRY",
	"танк": "TANKS",
	"самолет": "PLANES",
	"ракета": "ROCKETS",
	"ядерка": "NUKES"
}

army_type_accusative = {
	"пехота": "пехоты",
	"танк": "танков",
	"самолет": "самолетов",
	"ракета": "ракет",
	"ядерка": "ядерок"
}

army_prices = {
}

def get_army_price(type, index) -> int:
	return eval(army_prices.get(type).format(index))

while True:
	try:
		for event in longpoll.listen():
			try:
				if event.obj['message']['action']['type'] == 'chat_invite_user':
					if event.obj['message']['action']['member_id'] == int(f'-{id}'):
						sendm(event.obj['message']['peer_id'],
							'Всем привет! Я - бот ПВГ.\n'+
							'Чтобы начать работу со мной, напишите команду "страна регистрация" и укажите ссылку на вашу группу страны.\n'+
							'Чтобы узнать команды, напишите "бот помощь".\n'+
							'Также вам необходимо выдать мне права администратора и доступ к переписке, чтобы я нормально функционировал.'
							)
					continue
			except:
				a = 0
			if event.type == VkBotEventType.MESSAGE_NEW:
				peer_id=event.obj['message']['peer_id']
				from_id=event.obj['message']['from_id']
				message_id=event.obj['message']['conversation_message_id']
				forward = "{" + f'"peer_id": {peer_id}, "conversation_message_ids": [{message_id}],"is_reply": true' + "}"
				if event.obj['message']['from_id'] < 0:
					continue
				lowcont = event.obj['message']['text'].lower()
				cont = event.obj['message']['text']
				if event.from_chat:
					if block and not is_admin_of_bot(from_id):
						continue
					if re.match(r'^/admin approve$', lowcont):
						if is_admin_of_bot(from_id):
							if not cur.execute('').fetchall():
								chat_title = vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['chat_settings']['title']
								now = get_now_string()
								cur.execute('')
								cur.execute('')
								db.commit()
								sendm(peer_id,
									f'Страна {peer_id} зарегистрирована'
								)
								continue
							sendm(peer_id,
								'Страна уже зарегистрирована'
							)
							continue
						sendm(peer_id,
							'Вы не администратор'
						)
						continue
					if re.match(r'^бот$', lowcont):
						sendr(peer_id, forward,
							"На месте"
						)
						continue
					if re.match(r'^бот помощь', lowcont):
						if re.match(r'^бот помощь$', lowcont):
							sendm(peer_id,
								"=Группы команд=\n"+
								"Бот помощь [группа]\n"+
								"- Страна\n"+
								"- Топы\n"+
								"- Аккаунт\n"+
								"- Армия\n"+
								"- Война\n"+
								"- Рынок\n"+
								"- Политика\n"+
								"- Биржа\n"+
								"- Общее"
							)
							continue
						if re.match(r'^бот помощь страна$', lowcont):
							sendm(peer_id,
								"=Команды страна="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nСтрана регистрация [ссылка на паблик] - регистрация страны"+
								"\nСтрана инфо - информация о вашей стране"+
								"\nСтрана армия - информация о вашей армии"+
								"\nСтраны список [страница] - список всех существующих стран"+
								"\nСтрана города - список городов конкретной страны"+
								"\nСтрана город имя <номер> <название> - переименовать город"+
								"\nСтрана шахта улучшить - улучшить шахту"+
								"\nСтрана город построить - построить город"+
								"\nСтрана завод построить - построить завод"+
								"\nСтрана название <название> - переименовать страну"+
								"\nСтрана ссылка <ссылка> - поменять ссылку на паблик страны"+
								"\nСтрана топ шахтеры [страница] - топ шахтеров"+
								"\nСтрана когда рег - Дата регистрации страны"+
								"\nВклад экономика <сырье> - Вложение в экономику"+
								"\nВклад война <сырье> - Вложение в войну"+
								"\nпвг +модер <пинг пользователя> - Сделать пользователя модератором беседы"+
								"\nпвг +модер <ответ на сообщение> - Сделать пользователя модератором беседы"+
								"\nпвг -модер <пинг пользователя> - Убрать пользователя из списка модераторов беседы"+
								"\nпвг -модер <ответ на сообщение> - Убрать пользователя из списка модераторов беседы"+
								"\nпвг модераторы - Вывести список модераторов этой беседы"
							)
							continue
						if re.match(r'^бот помощь топы$', lowcont):
							sendm(peer_id,
								"=Команды топы="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nТоп шахтеры [страница] - глобальный топ шахтеров"+
								"\nСтрана топ шахтеры [страница] - топ шахтеров"+
								"\nТоп экономика [страница] - Топ стран по индексу экономики"+
								"\nТоп война [страница] - Топ стран по военному индексу"
							)
							continue
						if re.match(r'^бот помощь аккаунт$', lowcont):
							sendm(peer_id,
								"=Команды аккаунт="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nАккаунт инфо - информация о шахтере в конкретной стране"+
								"\nАккаунт имя <имя> - поменять имя аккаунта"+
								"\nАккаунт создать - создать аккаунт в конкретной стране"+
								"\nРабота шахта/копать - добывать SF"+
								"\nРабота завод - производить сырье"
							)
							continue
						if re.match(r'^бот помощь армия$', lowcont):
							sendm(peer_id,
								"=Команды армия="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nСтрана армия - информация о вашей армии"+
								"\nАрмия создать <пехота|танк|самолет|ракета|ядерка> <количество> - пополнить армию указанным типом"+
								"\nАрмия передать <айди> <пехота|танк|самолет|ракета|ядерка> <количество> - передать еденицы армии конкретной стране"+
								"\nЦена <тип> <количество> - Цена за N типа армии"
							)
							continue
						if re.match(r'^бот помощь война$', lowcont):
							sendm(peer_id,
								"=Команды войны="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nОбъявить войну <айди> - объявить войну стране"+
								"\nПредложить мир - предложить мир стране, а также принять его"+
								"\nМир отказ - отказаться от предложения мира"+
								"\nВойна ход - выполнить ход войны"+
								"\nВойна инфо - информация о войне"
							)
							continue
						if re.match(r'^бот помощь политика$', lowcont):
							sendm(peer_id,
								"=Команды политика="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nПеревод сырье <айди> <сырье> - перевести сырье на счет другой страны"+
								"\nПеревод сафрил <айди> <SF> - перевести SF на счет другой страны"+
								"\nПеревод коин <айди> <PCN> - перевести PCN на счет другой страны"+
								"\nСанкции список от страны [страница] - Список стран, против которых ваша страна ввела санкции"+
								"\nСанкции список стране [страница] - Список стран, которые ввели против вашей страны санкции"+
								"\nСанкции ввести <айди> - Ввести санкции против конкретной страны"+
								"\nСанкции снять <айди> - Снять санкции против конкретной страны"+
								"\nОбъявить войну <айди> - объявить войну стране"+
								"\nПредложить мир - предложить мир стране, а также принять его"+
								"\nМир отказ - отказаться от предложения мира"+
								"\nАрмия передать <айди> <пехота|танк|самолет|ракета|ядерка> <количество> - передать еденицы армии конкретной стране"
							)
							continue
						if re.match(r'^бот помощь биржа$', lowcont):
							sendm(peer_id,
								"=Команды биржа="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nБиржа инфо [день|месяц|год]- Информация о курсе PCN"+
								"\nБиржа стата - Статистика о покупках и продажах на бирже, также локальная информация"+
								"\nБиржа цена <N> - Количество PCN, которое можно купить за N SF"+
								"\nБиржа цена коин <N> - Количество SF, которое можно получить за N PCN"+
								"\nБиржа купить <N> - Купить PCN за N SF"+
								"\nБиржа продать <N> - Продать N PCN"+
								"\nПеревод коин <айди> <PCN> - перевести PCN на счет другой страны"+
								"\nТранзакции - Транзакции"
							)
							continue
						if re.match(r'^бот помощь рынок$', lowcont):
							sendm(peer_id,
								"=Команды рынок="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nРынок сырья [страница] - список всех лотов на рынке"+
								"\nЛот создать <сырье> <цена> - выставить ед. сырья на продажу в SF"+
								"\nЛот снять <номер> - снять лот с продажи"+
								"\nЛот принять <номер> - купить лот"
							)
							continue
						if re.match(r'^бот помощь общее$', lowcont):
							sendm(peer_id,
								"=Общие команды="+
								"\n<обязательный аргумент> [необязательный аргумент]"+
								"\nБот - пинг бота"+
								"\nБот помощь - список всех команд"+
								"\nВсе цены - Список актуальных цен на улучшение всего"+
								"\nПеревод сырье <айди> <сырье> - перевести сырье на счет другой страны"+
								"\nПеревод сафрил <айди> <SF> - перевести SF на счет другой страны"+
								"\nСанкции список от страны [страница] - Список стран, против которых ваша страна ввела санкции"+
								"\nСанкции список стране [страница] - Список стран, которые ввели против вашей страны санкции"+
								"\nСанкции ввести <айди> - Ввести санкции против конкретной страны"+
								"\nСанкции снять <айди> - Снять санкции против конкретной страны"+
								"\nОбъявить войну <айди> - объявить войну стране"+
								"\nПредложить мир - предложить мир стране, а также принять его"+
								"\nМир отказ - отказаться от предложения мира"+
								"\nАрмия передать <айди> <пехота|танк|самолет|ракета|ядерка> <количество> - передать еденицы армии конкретной стране"+
								"\nКарта последняя"+
								"\nБот сво <Пересланное сообщение> - ищет сво в пересланном сообщении"+
								"\nЭкономика инфо"
							)
							continue
						sendm(peer_id,
							"Такой группы не существует"
						)
						continue
					#                                 0    1        2     3     4         5          6          7               8         9      10
					country_db = cur.execute('').fetchall()
					countries_amount = cur.execute('').fetchall()
					if country_db == [] and re.match(r'^страна регистрация ((https://vk\.com/((?!_)([A-Za-z0-9_]){1,}(?<!_))|(\[club\d+\|@(?!_)([A-Za-z0-9_]){1,}(?<!_)\])))$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						link = lowcont.split('страна регистрация ')[1]
						if not (re.match(r'^страна регистрация https://vk\.com/(?!_)([A-Za-z0-9_]){1,}(?<!_)$', lowcont) or \
								re.match(r'^страна регистрация \[club\d+\|@(?!_)([A-Za-z0-9_]){1,}(?<!_)\]$', lowcont)):
							sendm(peer_id,
								f'Ссылка "{link}" введена неверно.'
							)
							continue
						country_request = cur.execute('').fetchall()
						if country_request == []:
							cur.execute('')
							db.commit()
						country_request = cur.execute('').fetchall()
						if 0 == 1:
							sendm(peer_id,
								'Ваша страна уже зарегистрирована'
							)
							continue
						elif 0 == 1:
							now = get_now_date()
							refused_date = 0
							refused_date = datetime.fromisoformat(refused_date).date()
							wait = refused_date + timedelta(days=1)
							if(now < wait):
								sendm(peer_id,
									f'Вашей стране уже было отказано в регистрации.\nЧтобы отправить новую заявку, дождитесь следующей даты: {wait}'
								)
								continue
						elif 0 == 1:
							sendm(peer_id,
								f'Заявка на регистрацию уже была отправлена.'
							)
							continue
						bot_admins = vk.groups.getById(group_id = 'vcplanet', fields='contacts')[0]['contacts']
						admins_ids = []
						for admin in bot_admins:
							try:
								if admin['desc'] == '[БОТ] Администратор':
									admins_ids.append(admin['user_id'])
							except:
								continue
						if admins_ids == []:
							sendm(peer_id,
								'У бота не указаны администраторы.'
							)
							continue
						cur.execute('')
						db.commit()
						for admin in admins_ids:
							sendu(admin,
								f'Страна (id: {peer_id}) оставила заявку на регистрацию.\n'+
								f'Ее ссылка: {link}.\n'+
								'Чтобы подтвердить заявку, напишите "подтвердить <id>"\n'+
								'Если ссылка не была указана или вы хотите отказать в подтверждении, напишите "отказ [id]"'
							)
						sendm(peer_id,
							'Заявка успешно отправлена.'
						)
						continue

					if re.match(r'^/a msg info$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						sendm(peer_id,
							f'{event.obj["message"]}'
						)
						continue

					if re.match(r'^/a a msg info$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						sendu(272111116,
							f'{event.obj["message"]}'
						)
						continue

					if country_db == []:
						continue
					if re.match(r'^(работа|добыча)$', lowcont):
						if not miner_exists(peer_id, from_id):
							sendm(peer_id,
								'У вас нет аккаунта.\nСоздайте с помощью команды "аккаунт создать".'
							)
							continue
						active_miners_list = get_active_miners(offset=0, type='неделя')
						active_miners = [i for i in active_miners_list if i[0] == 0]
						if active_miners:
							active_miners = 0
						else:
							active_miners = 0
						user_data = cur.execute('').fetchall()
						now = get_now_time_nondate()
						last_mined = datetime.fromisoformat(user_data[0][2])
						last_worked = datetime.fromisoformat(user_data[0][3])
						bot_check = (now-last_mined).seconds - 14400
						if bot_check > 0 and bot_check <= 2:
							sendm(peer_id,
								f'У вашего бота села батарейка, и он ничего не добыл. Его кстати придаваило сафриловыми рудами.'
							)
							continue
						wait_mine = last_mined + timedelta(hours=MINE_WAIT_HOURS)
						wait_work = last_worked + timedelta(hours=WORK_WAIT_HOURS)
						do_mine = True
						do_work = True
						result_message = ''
						if now < wait_mine:
							do_mine = False
							result_message += f'\nВы уже копали недавно.\nСледующая возможность появится через {wait_mine-now}'
						if 0 == 0:
							do_work = False
							result_message += f'\nУ вашей страны нет заводов.\nПостроить с помощью команды "страна завод построить".'
						elif now < wait_work:
							do_work = False
							result_message += f'\nВы уже работали недавно.\nСледующая возможность появится через {wait_work-now}'
						if do_mine:
							last_mined = get_now_time_string()
							mine_safrylus = MINE_LVL_SAFRYLUS[0-1].split(',')
							mined = random.randint(int(0), int(0))
							cur.execute('')
							cur.execute('')
							coin_price = cur.execute('').fetchall()[0][0]
							coins_bonus = 0
							if active_miners == 0:
								coins_bonus = mined/coin_price
							elif active_miners == 1:
								coins_bonus = mined/coin_price
							elif active_miners == 2:
								coins_bonus = mined*0.8/coin_price
							elif active_miners == 3:
								coins_bonus = mined*0.6/coin_price
							elif active_miners == 4:
								coins_bonus = mined*0.4/coin_price
							elif active_miners == 5:
								coins_bonus = mined*0.2/coin_price
							cur.execute('')
							result_message += f'\nВы добыли {mined} ед. сафрила.'
							if coins_bonus:
								result_message += f'\nБонус малой страны: {round(coins_bonus, 4)} PCN.'
						if do_work:
							last_worked = get_now_time_string()
							work_resources = FACTORIES_AMOUNT_RESOURCES[0-1].split(',')
							worked = random.randint(int(0), int(0))
							cur.execute('')
							cur.execute('')
							result_message += f'\nВы произвели {worked} ед. сырья.'
						db.commit()
						sendr(peer_id, forward,result_message.strip())
						continue
					if re.match(r'^аккаунт создать$', lowcont):
						user_data = cur.execute('').fetchall()
						if user_data == []:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								f'Аккаунт "{get_name(from_id)}" создан.'
							)
							continue
						sendm(peer_id,
							f'Аккаунт "{user_data[0][1]}" уже существует.'
						)
						continue
					if re.match(r'^аккаунт инфо$', lowcont):
						user_data = cur.execute('').fetchall()
						if user_data == []:
							sendm(peer_id,
								'У вас нет аккаунта.\nСоздайте с помощью команды "аккаунт создать".'
							)
							continue
						country_name = 0
						name = 0
						safrylus = 0
						resources = 0
						sendm(peer_id,
							f'🙍‍♂Имя: {name}\n'+
							f'👷‍♂Добыто: '+f'{safrylus:,}'.replace(',',' ')+f' SF и '+f'{resources:,}'.replace(',',' ')+f' ед. сырья\n'+
							f'🏳Страна: {country_name}'
						)
						continue
					if re.match(r'^аккаунт имя', lowcont):
						if not miner_exists(peer_id, from_id):
							sendm(peer_id,
								'У вас нет аккаунта.\nСоздайте с помощью команды "аккаунт создать".'
							)
							continue
						if re.match(r'^аккаунт имя$', lowcont):
							sendm(peer_id,
								'Укажите имя.'
							)
							continue
						name = re.split('аккаунт имя ', cont, flags=re.IGNORECASE)[1]
						name = name.replace('\n', ' ')
						name = name.replace('\'', '')
						if len(name) > 30:
							name = name[:30]
						cur.execute('')
						db.commit()
						sendr(peer_id, forward,
							'Готово'
						)
						continue
					if re.match(r'^страна инфо$', lowcont):
						cities_data = cur.execute('').fetchall()
						mine_safrylus = MINE_LVL_SAFRYLUS[0-1].split(',')
						work_resources = [0, 0]
						if not 0 == 0:
							work_resources = FACTORIES_AMOUNT_RESOURCES[0-1].split(',')
						sendm(peer_id,
							f'🏳 Страна: {0} | ID: {shorten_id(0)}\n'+
							f'📝 Группа: {0}\n'+
							f'⛏ Уровень шахты: {0} ({math.ceil((int(mine_safrylus[0])+int(mine_safrylus[1]))/2)} добыча)\n'+
							f'🏢 Городов: {cities_data[0][0]}\n'+
							f'🏭 Заводов: {0} ({math.ceil((int(work_resources[0])+int(work_resources[1]))/2)} добыча)\n'+
							f'📈 Индекс экономики: {round(0, 2)}\n'+
							f'⚔ Индекс военной мощи: {round(0, 2)}\n'+
							f'🗺 Площадь: '+f'{0[10]:,}'.replace(',',' ')+f' км²\n'+
							f'💎 Сафрила на складе: '+f'{0:,}'.replace(',',' ')+f' SF\n'+
							f'📦 Сырья на складе: '+f'{0:,}'.replace(',',' ')+f'\n'+
							f'🪙 Coin\'ов на счету: {round(0, 4)} PCN'
						)
						continue
					if re.match(r'^страна армия$', lowcont):
						military_data = cur.execute('').fetchall()
						if military_data == []:
							cur.execute('')
							db.commit()
							military_data = cur.execute('').fetchall()
						sendm(peer_id,
							  f'🏳Вооружение государства {0}:\n\n'+
							  f'⚔Пехота - '+f'{0:,}'.replace(',',' ')+f'\n'+
							  f'⚙Танки - {0}\n'+
							  f'✈Самолёты - {0}\n'+
							  f'🚀Ракеты - {0}\n'+
							  f'☢Ядерные бомбы - {0}\n\n'+
							  f'⚔Индекс военной мощи: {round(0, 2)}'
						)
						continue
					if re.match(r'^армия создать ', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if not re.match(r'^армия создать (пехота|танк|самол(е|ё)т|ракета|ядерка)', lowcont):
							sendm(peer_id,
								"Укажите тип."
							)
							continue
						if not re.match(r'^армия создать (пехота|танк|самол(е|ё)т|ракета|ядерка) -?\d+$', lowcont):
							sendm(peer_id,
								"Укажите количество"
							)
							continue
						type_amount = re.sub('^армия создать ', '', lowcont)
						type = type_amount.split(' ')[0]
						amount = int(type_amount.split(' ')[1])
						if amount <= 0:
							sendm(peer_id,
								"Укажите корректное количество"
							)
							continue
						price_for_type = math.ceil(get_army_price(type, round(0, 2)) * amount)
						country_current_safrylus = 0
						country_current_resources = 0
						if type == 'пехота':
							if country_current_safrylus < price_for_type:
								sendm(peer_id,
									f'Вашей стране не хватает '+f'{price_for_type - country_current_safrylus:,}'.replace(',',' ')+f' SF для мобилизации '+f'{amount:,}'.replace(',',' ')+f' солдат.'
								)
								continue
							cur.executescript('')
							db.commit()
							sendm(peer_id,
								f'Ваша страна мобилизовала '+f'{amount:,}'.replace(',',' ')+f' солдат.'
							)
							continue
						if country_current_resources < price_for_type:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{price_for_type - country_current_resources:,}'.replace(',',' ')+f' ед. сырья для создания '+f'{amount:,}'.replace(',',' ')+f' ед. {army_type_accusative.get(type)}.'
							)
							continue
						cur.executescript('')
						db.commit()
						sendm(peer_id,
							f'Ваша страна произвела '+f'{amount:,}'.replace(',',' ')+f' ед. {army_type_accusative.get(type)}.'
						)
						continue
					if re.match(r'^страны список', lowcont):
						page = 0
						offset = 0
						if re.match(r'^страны список -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^страны список \d+$', lowcont):
							page = int(lowcont.split('страны список ')[1])-1
							offset = page * COUNTRIES_LIST_MAX
						countries_offset = cur.execute('')
						info = '=Страны ПВГ='
						count = offset+1
						for country in countries_offset:
							info += f'\n{count} - "{country[2]}" | ID: {shorten_id(country[0])}{[f" | Ссылка: {country[3]}", ""][country[3]==""]}'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(countries_amount[0][0]/COUNTRIES_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^страна название', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						name = ''
						if re.match(r'^страна название [A-Za-zА-Яа-я\- ]+$', lowcont, flags=re.IGNORECASE):
							name = re.split('страна название ', cont, flags=re.IGNORECASE)[1]
						else:
							sendm(peer_id,
								'Введите корректное название.'
							)
							continue
						name = name.replace('\n', ' ')
						if len(name) > 30:
							name = name[:30]
						cur.execute('')
						db.commit()
						sendm(peer_id,
							'Готово'
						)
						continue
					if re.match(r'^страна ссылка', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						link = ''
						if re.match(r'^страна ссылка ((https://vk\.com/((?!_)([A-Za-z0-9_]){1,}(?<!_))|(\[club\d+\|@(?!_)([A-Za-z0-9_]){1,}(?<!_)\])))$', lowcont):
							link = lowcont.split('страна ссылка ')[1]
						else:
							sendm(peer_id,
								'Введите корректную ссылку.'
							)
							continue
						cur.execute('')
						db.commit()
						sendm(peer_id,
							'Готово'
						)
						continue
					if re.match(r'^топ шахт(е|ё)ры', lowcont):
						page = 0
						offset = 0
						if re.match(r'^топ шахт(е|ё)ры -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^топ шахт(е|ё)ры \d+$', lowcont):
							page = int(re.split(r'топ шахт(е|ё)ры ', lowcont)[2])-1
							offset = page * MINERS_LIST_MAX
						miners_amount = cur.execute('').fetchall()[0][0]
						miners_list = cur.execute('').fetchall()
						info = '=Глобальный топ шахтеров='
						if miners_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for miner in miners_list:
							info += f'\n{count} - {miner[0]}: '+f'{miner[1]:,}'.replace(',',' ')+f' SF'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(miners_amount/MINERS_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^топ рабочие', lowcont):
						page = 0
						offset = 0
						if re.match(r'^топ рабочие -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^топ рабочие \d+$', lowcont):
							page = int(lowcont.split('топ рабочие ')[1])-1
							offset = page * WORKERS_LIST_MAX
						workers_amount = cur.execute('').fetchall()[0][0]
						workers_list = cur.execute('').fetchall()
						info = '=Глобальный топ рабочих='
						if workers_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for worker in workers_list:
							info += f'\n{count} - {worker[0]}: '+f'{worker[1]:,}'.replace(',',' ')+f' ед. сырья'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(workers_amount/WORKERS_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^страна топ шахт(е|ё)ры', lowcont):
						page = 0
						offset = 0
						if re.match(r'^страна топ шахт(е|ё)ры -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^страна топ шахт(е|ё)ры \d+$', lowcont):
							page = int(re.split(r'страна топ шахт(е|ё)ры ', lowcont)[2])-1
							offset = page * MINERS_LIST_MAX
						miners_amount = cur.execute('').fetchall()[0][0]
						miners_list = cur.execute('').fetchall()
						info = f'=Топ шахтеров в {0}='
						if miners_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for miner in miners_list:
							info += f'\n{count} - {0}: '+f'{0:,}'.replace(',',' ')+f' SF'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(miners_amount/MINERS_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^страна топ рабочие', lowcont):
						page = 0
						offset = 0
						if re.match(r'^страна топ рабочие -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^страна топ рабочие \d+$', lowcont):
							page = int(lowcont.split('страна топ рабочие ')[1])-1
							offset = page * WORKERS_LIST_MAX
						workers_amount = cur.execute('').fetchall()[0][0]
						workers_list = cur.execute('').fetchall()
						info = f'=Топ рабочих в {0}='
						if workers_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for worker in workers_list:
							info += f'\n{count} - {0}: '+f'{0:,}'.replace(',',' ')+f' ед. сырья'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(workers_amount/WORKERS_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^топ актив( (день|неделя|месяц))?( (\d+))?$', lowcont):
						page = 0
						pattern = r'^топ актив( (день|неделя|месяц))?( (\d+))?$'
						search = re.search(pattern, lowcont)
						type = search.group(2)
						page = search.group(4)
						if not type:
							type = 'день'
						if page:
							page = int(page)-1
						else:
							page = 0
						if page == -1:
							continue
						offset = int(page * MINERS_LIST_MAX) # type: int
						miners_list = get_active_miners(offset=offset, type=type)
						info = f'=Активные пользователи за {"день" if type == "день" else "неделю" if type == "неделя" else "месяц"}'
						if miners_list == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						miners_list = sorted(miners_list, key=lambda x: x[1], reverse=True)
						count = offset+1
						for miner in miners_list:
							if miner[0]:
								info += f'\n{count} - {get_country_name(0)}: {0} шахтеров'
								count += 1
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^страна города$', lowcont):
						cities_data = cur.execute('').fetchall()
						if cities_data == []:
							sendm(peer_id,
								'В данной стране нет городов.'
							)
							continue
						info = f'=Города в {get_country_name(peer_id)}='
						count = 1
						for city in cities_data:
							info += f'\n{count} - {city[1]}'
							count+=1
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^страна город имя', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^страна город имя$', lowcont):
							sendm(peer_id,
								'Введите номер и название города.'
							)
							continue
						if re.match(r'^страна город имя -\d+', lowcont):
							sendm(peer_id,
								'Номер не должен быть отрицательным.'
							)
							continue
						if re.match(r'^страна город имя \d+$', lowcont):
							sendm(peer_id,
								'Введите название города.'
							)
							continue
						if re.match(r'^страна город имя [A-Za-zА-Яа-я\- ]+$', lowcont):
							sendm(peer_id,
								'Введите номер города.'
							)
							continue
						if not re.match(r'^страна город имя \d+ [A-Za-zА-Яа-я\- ]+$', lowcont):
							sendm(peer_id,
								'Введите корректные номер и название города.'
							)
							continue
						cities_data = cur.execute('').fetchall()
						index_name = re.split('страна город имя ', cont, flags=re.IGNORECASE)[1]
						index = int(index_name.split(' ')[0])
						name = index_name.split(' ')[1]
						name = name.replace('\n', ' ')
						if len(name) > 30:
							name = name[:30]
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Название {index}-го города теперь {name}'
						)
						continue
					if re.match(r'^страна шахта улучшить$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						mine_current_lvl = 0
						country_current_safrylus = 0
						if mine_current_lvl == len(MINE_PRICES):
							sendm(peer_id,
								f'Ваша шахта уже максимального уровня: {mine_current_lvl}'
							)
							continue
						mine_upgrade_price = int(MINE_PRICES[mine_current_lvl])
						if country_current_safrylus >= mine_upgrade_price:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								f'Ваша шахта улучшена: {mine_current_lvl+1}.'
							)
							continue
						sendm(peer_id,
							f'Для улучшения шахты не хватает '+f'{mine_upgrade_price-country_current_safrylus:,}'.replace(',',' ')+f' SF.'
						)
						continue
					if re.match(r'^страна завод построить$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						cities_data = cur.execute('').fetchall()
						cities_amount = cur.execute('').fetchall()
						if cities_amount[0][0] == 0:
							sendm(peer_id,
								'У вашей страны нет городов.\nПостроить с помощью команды "страна город построить".'
							)
							continue
						if 0 == len(FACTORIES_AMOUNT_RESOURCES):
							sendm(peer_id,
								f'У вашей страны максимальное число заводов: {0}.'
							)
							continue
						if cities_amount[0][0] == 0:
							sendm(peer_id,
								f'У вашей страны не хватает городов для постройки завода: {cities_amount[0][0]} городов для {0+1}-го завода'
							)
							continue
						if 0 >= FACTORY_PRICE:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								'Готово.'
							)
							continue
						sendm(peer_id,
							f'Для строительства завода не хватает '+f'{FACTORY_PRICE-0:,}'.replace(',',' ')+f' SF.'
						)
						continue
					if re.match(r'^страна город построить$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						cities_data = cur.execute('').fetchall()
						cities_amount = cur.execute('').fetchall()
						if len(cities_data) == len(CITIES_PRICES):
							sendm(peer_id,
								f'У вашей страны максимальное число городов: {cities_amount[0][0]}.'
							)
							continue
						min_area_to_build = int(CITIES_LIMITS_AREAS[cities_amount[0][0]])
						if(0[10] < min_area_to_build):
							sendm(peer_id,
								  f'Площадь вашей страны слишком мала, чтобы построить новый город. Расширьтесь ещё на '+f'{min_area_to_build - 0[10]:,}'.replace(',',' ')+f' км².'
							)
							continue
						city_price = int(CITIES_PRICES[cities_amount[0][0]])
						if 0 >= city_price:
							cur.execute('')
							cur.execute('')
							db.commit()
							sendm(peer_id,
								'Город построен.'
							)
							continue
						sendm(peer_id,
							f'Для строительства города не хватает '+f'{city_price-0:,}'.replace(',',' ')+f' SF.'
						)
						continue
					if re.match(r'^страна когда рег$', lowcont):
						register_date = cur.execute('').fetchall()
						sendm(peer_id,
							f"Страна зарегистрирована {register_date[0][0]}."
						)
						continue
					if re.match(r'^лот создать', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^лот создать$', lowcont):
							sendm(peer_id,
								'Укажите ед. сырья и цену.'
							)
							continue
						if re.match(r'^лот создать \d+$', lowcont):
							sendm(peer_id,
								'Укажите цену.'
							)
							continue
						if not re.match(r'^лот создать \d+ \d+$', lowcont):
							sendm(peer_id,
								'Укажите ед. сырья и цену.'
							)
							continue
						res_price = lowcont.split('лот создать ')[1].split(' ')
						res = int(res_price[0])
						price = int(res_price[1])
						lots = cur.execute('').fetchall()
						lots_last_index = 0
						if not lots == []:
							lots_last_index = int(lots[-1][0].split('№')[1])
						if res < 100:
							sendm(peer_id,
								'Минимальное количество ед. сырья - 100.'
							)
							continue
						country_current_resources = 0
						if res > country_current_resources:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{res-country_current_resources:,}'.replace(',',' ')+f' ед. сырья.'
							)
							continue
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Лот №{lots_last_index+1} в '+f'{res:,}'.replace(',',' ')+f' ед. сырья за '+f'{price:,}'.replace(',',' ')+f' SF создан.'
						)
						continue
					if re.match(r'^лот снять', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^лот снять$', lowcont):
							sendm(peer_id,
								'Укажите номер лота.'
							)
							continue
						if not re.match(r'^лот снять \d+$', lowcont):
							sendm(peer_id,
								'Укажите корректный номер лота.'
							)
							continue
						index = int(lowcont.split('лот снять ')[1])
						lot_data = cur.execute('').fetchall()
						if lot_data == []:
							sendm(peer_id,
								f'Лот №{index} не существует.'
							)
							continue
						if not lot_data[0][1] == peer_id:
							sendm(peer_id,
								f'Лот №{index} не принадлежит вашей стране.'
							)
							continue
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Лот №{index} снят с рынка.'
						)
						continue
					if re.match(r'^лот принять', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^лот принять$', lowcont):
							sendm(peer_id,
								'Укажите номер лота.'
							)
							continue
						if not re.match(r'^лот принять \d+$', lowcont):
							sendm(peer_id,
								'Укажите корректный номер лота.'
							)
							continue
						index = int(lowcont.split('лот принять ')[1])
						lot_data = cur.execute('').fetchall()
						if lot_data == []:
							sendm(peer_id,
								f'Лот №{index} не существует.'
							)
							continue
						if 0 == peer_id:
							sendm(peer_id,
								f'Лот №{index} принадлежит вашей стране.'
							)
							continue
						country_current_safrylus = 0
						if country_current_safrylus < 0:
							sendm(peer_id,
								f'Для покупки не хватает '+f'{0-country_current_safrylus:,}'.replace(',',' ')+f' SF.'
							)
							continue
						cur.execute('')
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Лот №{index} приобритен: '+f'{0:,}'.replace(',',' ')+f' ед. сырья за '+f'{0:,}'.replace(',',' ')+f' SF.'
						)
						sendm(0,
							f'Ваш лот №{index} был приобритен страной "{get_country_name(peer_id)}": '+f'{0:,}'.replace(',',' ')+f' ед. сырья за '+f'{0:,}'.replace(',',' ')+f' SF.'
						)
						continue
					if re.match(r'^рынок сырья', lowcont):
						page = 0
						offset = 0
						if re.match(r'^рынок сырья -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^рынок сырья \d+$', lowcont):
							page = int(lowcont.split('рынок сырья ')[1])-1
							offset = page * AUCTION_LIST_MAX
						lots_amount = cur.execute('').fetchall()[0][0]
						lots = cur.execute('').fetchall()
						info = f'=Рынок='
						if lots_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for lot in lots:
							info += f'\n{lot[0]} от {get_country_name(0)}: '+f'{0:,}'.replace(',',' ')+f' ед. сырья за '+f'{0:,}'.replace(',',' ')+f'SF.'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(lots_amount/AUCTION_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^перевод сырь(е|ё)', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^перевод сырь(е|ё)$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и ед. сырья.'
							)
							continue
						if not re.match(r'^перевод сырь(е|ё) \d+ \d+$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и ед. сырья.'
							)
							continue
						id_res = re.split(r'перевод сырь(е|ё) ', lowcont)[2]
						id = int(id_res.split(' ')[0])
						res = int(id_res.split(' ')[1])
						if not re.match(r'^20+(?!0)[0-9]+$', str(id)):
							id = parse_id(id)
							if id == None:
								sendm(peer_id,
									'Страны с таким айди не существует.'
								)
								continue
						country_check = cur.execute('').fetchall()
						if country_check == [] or id == 2000000012:
							sendm(peer_id,
								'Страны с таким айди не существует.'
							)
							continue
						if 0 == id:
							sendm(peer_id,
								'Айди получателя не должен совпадать с вашим.'
							)
							continue
						if res < 100:
							sendm(peer_id,
								f'Число ед. сырья должно быть не менее 100.'
							)
							continue
						if 0 < res:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{res-0:,}'.replace(',',' ')+f' ед. сырья для перевода.'
							)
							continue
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы перевели стране "{get_country_name(id)}" '+f'{res:,}'.replace(',',' ')+f' ед. сырья.'
						)
						sendm(id,
							f'Страна "{0}" перевела вам '+f'{res:,}'.replace(',',' ')+f' ед. сырья'
						)
						continue
					if re.match(r'^перевод сафрил', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^перевод сафрил$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и SF.'
							)
							continue
						if not re.match(r'^перевод сафрил \d+ \d+$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и SF.'
							)
							continue
						id_res = re.split(r'перевод сафрил ', lowcont)[1]
						id = int(id_res.split(' ')[0])
						saf = int(id_res.split(' ')[1])
						if not re.match(r'^20+(?!0)[0-9]+$', str(id)):
							id = parse_id(id)
							if id == None:
								sendm(peer_id,
									'Страны с таким айди не существует.'
								)
								continue
						country_check = cur.execute('').fetchall()
						if country_check == [] or id == 2000000012:
							sendm(peer_id,
								'Страны с таким айди не существует.'
							)
							continue
						if 0 == id:
							sendm(peer_id,
								'Айди получателя не должен совпадать с вашим.'
							)
							continue
						if saf < 100:
							sendm(peer_id,
								f'Число SF должно быть не менее 100.'
							)
							continue
						if 0 < saf:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{saf-0:,}'.replace(',',' ')+f' SF для перевода.'
							)
							continue
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы перевели стране "{get_country_name(id)}" '+f'{saf:,}'.replace(',',' ')+f' SF.'
						)
						sendm(id,
							f'Страна "{0}" перевела вам '+f'{saf:,}'.replace(',',' ')+f' SF.'
						)
						continue
					if re.match(r'^перевод коин', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^перевод коин$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и PCN.'
							)
							continue
						if not re.match(r'^перевод коин \d+ \d+(.\d+)?$', lowcont):
							sendm(peer_id,
								'Укажите айди страны и PCN.'
							)
							continue
						id_res = re.split(r'перевод коин ', lowcont)[1]
						id = int(id_res.split(' ')[0])
						pcn = float(id_res.split(' ')[1])
						if not re.match(r'^20+(?!0)[0-9]+$', str(id)):
							id = parse_id(id)
							if id == None:
								sendm(peer_id,
									'Страны с таким айди не существует.'
								)
								continue
						country_check = cur.execute('').fetchall()
						if country_check == [] or id == 2000000012:
							sendm(peer_id,
								'Страны с таким айди не существует.'
							)
							continue
						if 0 == id:
							sendm(peer_id,
								'Айди получателя не должен совпадать с вашим.'
							)
							continue
						if pcn <= 0:
							sendm(peer_id,
								f'Введите корректное значениею'
							)
							continue
						if 0 < pcn:
							sendm(peer_id,
								f'Вашей стране не хватает {round(pcn-0,4)} PCN для перевода.'
							)
							continue
						cur.executescript(f'''UPDATE COUNTRIES SET COINS = COINS - {pcn} WHERE CID={peer_id};
UPDATE COUNTRIES SET COINS = COINS + {pcn} WHERE CID={id};''')
						db.commit()
						sendm(peer_id,
							f'Вы перевели стране "{get_country_name(id)}" {round(pcn, 4)} PCN.'
						)
						sendm(id,
							f'Страна "{0}" перевела вам {round(pcn, 4)} PCN.'
						)
						continue
					if re.match(r'^топ экономика', lowcont):
						page = 0
						offset = 0
						if re.match(r'^топ экономика -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^топ экономика \d+$', lowcont):
							page = int(lowcont.split('топ экономика ')[1])-1
							offset = page * AUCTION_LIST_MAX
						countries = cur.execute('').fetchall()
						countries_amount = cur.execute('').fetchall()
						info = '=Экономический индекс='
						count = offset
						for country in countries:
							info += f"\n{count+1} - {0} (id: {shorten_id(0)}): {round(0, 2)}."
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(countries_amount[0][0]/ECONOMICS_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^топ война', lowcont):
						page = 0
						offset = 0
						if re.match(r'^топ война -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^топ война \d+$', lowcont):
							page = int(lowcont.split('топ война ')[1])-1
							offset = page * WAR_LIST_MAX
						countries = cur.execute('').fetchall()
						countries_amount = cur.execute('').fetchall()
						info = '=Индекс военной мощи='
						count = offset
						for country in countries:
							info += f'\n{count+1} - {0} (id: {shorten_id(0)}): {round(0, 2)}.'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(countries_amount[0][0]/WAR_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^топ площадь', lowcont):
						page = 0
						offset = 0
						if re.match(r'^топ площадь -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^топ площадь \d+$', lowcont):
							page = int(lowcont.split('топ площадь ')[1])-1
							offset = page * WAR_LIST_MAX
						countries = cur.execute('').fetchall()
						countries_amount = cur.execute('').fetchall()
						info = '=Топ стран по площади='
						count = offset
						for country in countries:
							info += f'\n{count+1} - {0} (id: {shorten_id(0)}): '+f'{round(0, 2):,}'.replace(',',' ')+f' км².'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(countries_amount[0][0]/WAR_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^вклад экономика', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^вклад экономика$', lowcont):
							sendm(peer_id,
								'Введите количество ед. сырья.'
							)
							continue
						if not re.match(r'^вклад экономика \d+$', lowcont):
							sendm(peer_id,
								'Введите количество ед. сырья.'
							)
							continue
						res = int(lowcont.split('вклад экономика ')[1])
						if res < 100:
							sendm(peer_id,
								'Минимальное количество ед. сырья - 100.'
							)
							continue
						country_current_resources = cur.execute('').fetchall()[0][0]
						country_current_ecindex = cur.execute('').fetchall()[0][0]
						if country_current_ecindex >= 10.00:
							sendm(peer_id,
								'Экономический индекс не может быть выше 10.'
							)
							continue
						if res > country_current_resources:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{res-country_current_resources:,}'.replace(',',' ')+f' ед. сырья.'
							)
							continue
						if 0 > 10.00:
							resources_used = 0
							cur.execute('')
							db.commit()
							sendm(peer_id,
								f'Ваш экономический индекс вырос на {round(0, 2)}, '+f'{round(res-resources_used):,}'.replace(',',' ')+f' ед. сырья возвращено на ваш счет.'
							)
							continue
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Ваш экономический индекс вырос на {0}.'
						)
						continue
					if re.match(r'^вклад война', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^вклад война$', lowcont):
							sendm(peer_id,
								'Введите количество ед. сырья.'
							)
							continue
						if not re.match(r'^вклад война \d+$', lowcont):
							sendm(peer_id,
								'Введите количество ед. сырья.'
							)
							continue
						res = int(lowcont.split('вклад война ')[1])
						if res < 100:
							sendm(peer_id,
								'Минимальное количество ед. сырья - 100.'
							)
							continue
						country_current_resources = cur.execute('').fetchall()[0][0]
						country_current_ecindex = cur.execute('').fetchall()[0][0]
						country_current_warindex = cur.execute('').fetchall()[0][0]
						if country_current_warindex >= 10.00:
							sendm(peer_id,
								'Индекс военной мощи не может быть выше 10.'
							)
							continue
						if res > country_current_resources:
							sendm(peer_id,
								f'Вашей стране не хватает '+f'{res-country_current_resources:,}'.replace(',',' ')+f' ед. сырья.'
							)
							continue
						warindex_increase = 0
						if warindex_increase + country_current_warindex > 10:
							resources_used = 0
							warindex_increase = round(0, 2)
							cur.execute('')
							db.commit()
							sendm(peer_id,
								f'Ваш индекс военной мощи вырос на {warindex_increase}, '+f'{round(res-resources_used):,}'.replace(',',' ')+f' ед. сырья возвращено на ваш счет.'
							)
							continue
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Ваш индекс военной мощи вырос на {warindex_increase}.'
						)
						continue
					if re.match(r'^санкции список от страны', lowcont):
						page = 0
						offset = 0
						if re.match(r'^санкции список от страны -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^санкции список от страны \d+$', lowcont):
							page = int(lowcont.split('санкции список от страны ')[1])-1
							offset = page * SANCTIONS_TO_LIST_MAX
						your_sanctions = cur.execute('').fetchall()
						your_sanctions_amount = cur.execute('').fetchall()[0][0]
						info = '=Санкции от вашей страны='
						if your_sanctions == []:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for sanction in your_sanctions:
							info += f'\n{get_country_name(sanction[0])}'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(your_sanctions_amount/SANCTIONS_TO_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^санкции список стране', lowcont):
						page = 0
						offset = 0
						if re.match(r'^санкции список стране -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^санкции список стране \d+$', lowcont):
							page = int(lowcont.split('санкции список стране ')[1])-1
							offset = page * SANCTIONS_FROM_LIST_MAX
						to_you_sanctions = cur.execute('').fetchall()
						to_you_sanctions_amount = cur.execute('').fetchall()[0][0]
						info = '=Санкции вашей стране='
						if to_you_sanctions_amount == 0:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for sanction in to_you_sanctions:
							info += f'\n{get_country_name(sanction[0])}'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(to_you_sanctions_amount/SANCTIONS_FROM_LIST_MAX)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^санкции ввести', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^санкции ввести$', lowcont):
							sendm(peer_id,
								'Укажите айди страны.'
							)
							continue
						if not re.match(r'^санкции ввести (20{1,}((?!0))|)[0-9]+$', lowcont):
							sendm(peer_id,
								'Укажите айди страны.'
							)
							continue
						id_raw = lowcont.split('санкции ввести ')[1]
						id = None
						if re.match(r'^20{1,}((?!0))[0-9]+$', str(id_raw)):
							id = id_raw
						else:
							id = get_id(id_raw)
						sanction_check = cur.execute('').fetchall()
						if not sanction_check == []:
							sendm(peer_id,
								'Вы уже ввели санкции против этой страны.'
							)
							continue
						sanction_to_economics = cur.execute('').fetchall()
						if sanction_to_economics == [] or (id == 2000000001 or id == 2000000012):
							sendm(peer_id,
								'Данная страна не существует.'
							)
							continue
						index_to_decrease = 0 * 0.1
						if sanction_to_economics[0][0] - index_to_decrease < 0.01:
							cur.execute('')
						else:
							cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы ввели против страны {get_country_name(id)} санкции.'
						)
						sendm(id,
							f'Против вас ввела санкции страна {get_country_name(peer_id)}.'
						)
						continue
					if re.match(r'^санкции снять', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^санкции снять$', lowcont):
							sendm(peer_id,
								'Укажите айди страны.'
							)
							continue
						if not re.match(r'^санкции снять (20{1,}((?!0))|)[0-9]+$', lowcont):
							sendm(peer_id,
								'Укажите айди страны.'
							)
							continue
						id_raw = lowcont.split('санкции снять ')[1]
						id = None
						if re.match(r'^20{1,}((?!0))[0-9]+$', str(id_raw)):
							id = id_raw
						else:
							id = get_id(id_raw)
						sanction_check = cur.execute('').fetchall()
						if sanction_check == [] or (id == 2000000001 or id == 2000000012):
							sendm(peer_id,
								'Вы нет вводили санкции против этой страны.'
							)
							continue
						sanction_of_economics = cur.execute('').fetchall()
						if sanction_of_economics == []:
							sendm(peer_id,
								'Данная страна не существует. Санкции сняты.'
							)
							cur.execute('')
							db.commit()
							continue
						index_to_increase = 0 * 0.1
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы сняли санкции со страны {get_country_name(id)}.'
						)
						sendm(id,
							f'Страна {get_country_name(peer_id)} сняла с вашей страны санкции.'
						)
						continue
					if re.match(r'^рыбачить$', lowcont):
						sendm(peer_id,
							random.choice(EASTER).format(0)
						)
						continue
					if re.match(r'^все цены$', lowcont):
						info = f'Цены для {0}'
						mine_current_lvl = 0
						country_current_safrylus = 0
						if mine_current_lvl == len(MINE_PRICES):
							info += f'\nВаша шахта уже максимального уровня.'
						else:
							mine_upgrade_price = int(MINE_PRICES[mine_current_lvl])
							info += f'\nСтоимость улучшения до шахты {mine_current_lvl+1}-го уровня: '+f'{mine_upgrade_price:,}'.replace(',',' ')+f' SF.'
						cities_amount = cur.execute('').fetchall()
						if cities_amount[0][0] == len(CITIES_PRICES):
							info += f'У вашей страны максимальное число городов.'
						else:
							city_price = int(CITIES_PRICES[cities_amount[0][0]])
							info += f'\nСтоимость постройки {cities_amount[0][0]+1}-го города: '+f'{city_price:,}'.replace(',',' ')+f' SF.'
						if 0 == len(FACTORIES_AMOUNT_RESOURCES):
							info += f'У вашей страны максимальное число заводов.'
						else:
							info += f'\nСтоимость постройки завода: '+f'{FACTORY_PRICE:,}'.replace(',',' ')+f' SF.'
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^цена ', lowcont):
						if not re.match(r'^цена (пехота|танк|самол(е|ё)т|ракета|ядерка)', lowcont):
							sendm(peer_id,
								'Укажите тип пехоты.'
							)
							continue
						if not re.match(r'^цена (пехота|танк|самол(е|ё)т|ракета|ядерка) -?\d+$', lowcont):
							sendm(peer_id,
								'Укажите количество.'
							)
							continue
						type_amount = re.sub('^цена ', '', lowcont)
						type = type_amount.split(' ')[0]
						amount = int(type_amount.split(' ')[1]) 
						if amount <= 0:
							sendm(peer_id,
								'Укажите корректное количество.'
							)
							continue
						if type in army_prices.keys():
							sendr(peer_id, forward,
								f'{math.ceil(get_army_price(type, round(0, 2)) * amount):,}'.replace(',',' ')+f' {["ед. сырья", "SF"][type=="пехота"]}.'
							)
						else:
							sendr(peer_id, forward,
								'Такого типа не существует.'
							)
						continue
					if re.match(r'^война инфо$', lowcont):
						war_data = cur.execute('').fetchall()
						if war_data == []:
							sendm(peer_id,
								"В данный момент ваша страна ни с кем не воюет."                                
							)
							continue
						country1_name = get_country_name(0)
						country2_name = get_country_name(0)
						now = get_now_time_nondate()
						last_move = datetime.fromisoformat(0)
						wait = last_move + timedelta(hours=WAR_MOVE_COOLDOWN_HOUR)
						duration = wait-now
						if duration.total_seconds() < 0:
							duration = datetime.strftime(datetime.min, "%H:%M:%S")
						sendm(peer_id,
							f"=Война=\nМежду:\n{country1_name}\n{country2_name}\n\n"+
							f"Ход: {0}\nДо следующего хода: {duration}\n\n"+
							f'Потери {country1_name}:\nПехота - '+f'{0:,}'.replace(',',' ')+f'\nТанки - {0}\nСамолеты - {0}\n\n'+
							f'Потери {country2_name}:\nПехота - '+f'{0:,}'.replace(',',' ')+f'\nТанки - {0}\nСамолеты - {0}'
						)
						continue
					if re.match(r'^объявить войну', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if not war_check == []:
							sendm(peer_id,
								'Ваша страна уже воюет.'
							)
							continue
						if not re.match(r'^объявить войну \d+$', lowcont):
							sendm(peer_id,
								'Укажите айди страны.'
							)
							continue
						id_raw = lowcont.split('объявить войну ')[1]
						id = None
						if re.match(r'^20{1,}((?!0))[0-9]+$', str(id_raw)):
							id = id_raw
						else:
							id = get_id(id_raw)
						if cur.execute('').fetchall() == []:
							sendm(peer_id,
								'Данная страна не существует.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if not war_check == []:
							sendm(peer_id,
								'Данная страна уже воюет.'
							)
							continue
						if id == peer_id:
							sendm(peer_id,
								'Нельзя объявить войну самим себе.'
							)
							continue
						if id == 2000000001 or id == 2000000012:
							sendm(peer_id,
								'Данная страна не существует.'
							)
							continue
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f"Вы объявили стране {get_country_name(id)} войну!\n У вас есть {WAR_MOVE_COOLDOWN_HOUR} часов времени на подготовку."
						)
						sendm(id,
							f"Страна {0} объявила вам войну!\n У вас есть {WAR_MOVE_COOLDOWN_HOUR} часов времени на подготовку."
						)
						sendm(2000000001,
							f"Страна {0} объявила стране {get_country_name(id)} войну."
						)
						continue
					if re.match(r'^предложить мир$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'В данный момент ваша страна ни с кем не воюет.'
							)
							continue
						if 0 == peer_id:
							opp_id = 0
						else:
							opp_id = 0
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'Ошибка.'
							)
							continue
						war_data = cur.execute('').fetchall()
						if 0 == peer_id:
							sendr(peer_id, forward,
								'Вы уже предлагали мир, но не получили ответ.'
							)
							continue
						if not 0 == peer_id and (not 0 == 0 and not 0 == -1):
							cur.execute(f'DELETE FROM WARS WHERE (CIDOPPONENT1={peer_id} AND CIDOPPONENT2={opp_id}) OR (CIDOPPONENT2={peer_id} AND CIDOPPONENT1={opp_id})')
							end = cur.execute('').fetchall()
							db.commit()
							sendm(peer_id,
								f'Вы приняли предложение о мире от страны {get_country_name(opp_id)}. Война завершена.'
							)
							sendm(opp_id,
								f'Страна {0} приняла ваше предложение о мире. Война завершена.'
							)
							sendm(2000000001,
								 "=================\n"+
								f"Страны {get_country_name(0)} и {get_country_name(0)} подписали мирное соглашение.\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов\n\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							continue
						if 0 <= 0:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								f'Вы предложили стране {get_country_name(opp_id)} мир. Если хотите отменить, напишите "мир отказ".'
							)
							sendm(opp_id,
								f'Страна {0} предложила вам мир. Чтобы принять, напишите "Предложить мир".'
							)
							continue
						if 0 == 0:
							sendm(peer_id,
								"Предложения мира еще не было."
							)
							continue
						if 0 == -1:
							sendm(peer_id,
								"Вы не можете предложить мир в данном ходу, так как вам уже было отказано."
							)
							continue
					if re.match(r'^армия передать', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if re.match(r'^армия передать$', lowcont):
							sendm(peer_id,
								'Введите айди страны.'
							)
							continue
						if re.match(r'^армия передать \d+$', lowcont):
							sendm(peer_id,
								'Введите айди страны.'
							)
							continue
						if re.match(r'^армия передать \d+ (пехота|танк|самол(е|ё)т|ракета|ядерка)$', lowcont):
							sendm(peer_id,
								'Введите тип.'
							)
							continue
						if not re.match(r'^армия передать \d+ (пехота|танк|самол(е|ё)т|ракета|ядерка) \d+$', lowcont):
							sendm(peer_id,
								'Введите количество.'
							)
							continue
						raw = re.sub(r'^армия передать ', '', lowcont).split(' ')
						id = None
						if re.match(r'^20{1,}((?!0))[0-9]+$', str(raw[0])):
							id = raw[0]
						else:
							id = get_id(raw[0])
						if cur.execute('').fetchall() == []:
							sendm(peer_id,
								'Данная страна не существует.'
							)
							continue
						raw_type = raw[1]
						if id == 2000000001 or id == 2000000012:
							sendm(peer_id,
								'Данная страна не существует.'
							)
							continue
						type = army_type_enum.get(raw_type)
						amount = int(raw[2])
						army_type_amount = cur.execute('').fetchall()
						if army_type_amount[0][0] < amount:
							sendm(peer_id,
								'Вам не хватает '+f'{amount-army_type_amount[0][0]:,}'.replace(',',' ')+f' {army_type_accusative.get(raw_type)} для перевода стране {get_country_name(id)}.'
							)
							continue
						cur.executescript(f'''UPDATE MILITARY SET {type} = {type} - {amount} WHERE CID={peer_id};
UPDATE MILITARY SET {type} = {type} + {amount} WHERE CID={id};''')
						db.commit()
						sendm(peer_id,
							f'Вы передали стране {get_country_name(id)} '+f'{amount:,}'.replace(',',' ')+f' {army_type_accusative.get(raw_type)}.'
						)
						sendm(id,
							f'Страна {get_country_name(peer_id)} передала вам '+f'{amount:,}'.replace(',',' ')+f' {army_type_accusative.get(raw_type)}.'
						)
						continue
					if re.match(r'^мир отказ$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'В данный момент ваша страна ни с кем не воюет.'
							)
							continue
						if war_check[0][0] == peer_id:
							opp_id = war_check[0][1]
						else:
							opp_id = war_check[0][0]
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'Ошибка.'
							)
							continue
						war_data = cur.execute('').fetchall()
						if war_data[0][10] == peer_id:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								"Вы отменили свой запрос мира."
							)
							continue
						if war_data[0][10] == -1:
							sendm(peer_id,
								"В мире уже было отказано в этом ходу."
							)
							continue
						if war_data[0][10] == 0:
							sendm(peer_id,
								"Предложения мира еще не было."
							)
							continue
						if not war_data[0][10] == peer_id:
							cur.execute('')
							db.commit()
							sendm(peer_id,
								"Вы отказались от мира."
							)
							sendm(opp_id,
								f"Страна {0} отказалась от вашего предложения мира."
							)
							continue
					if re.match(r'^война ход$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'В данный момент ваша страна ни с кем не воюет.'
							)
							continue
						if war_check[0][0] == peer_id:
							opp_id = war_check[0][1]
						else:
							opp_id = war_check[0][0]
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'Ошибка.'
							)
							continue
						flag_end1 = False
						flag_end2 = False
						war_data = cur.execute('').fetchall()
						opponent1_army = cur.execute('').fetchall()
						opponent2_army = cur.execute('').fetchall()
						opponent1_war_power = cur.execute('').fetchall()[0][0]
						opponent2_war_power = cur.execute('').fetchall()[0][0]
						now = get_now_time_nondate()
						last_move = datetime.fromisoformat(0)
						wait = last_move + timedelta(hours=WAR_MOVE_COOLDOWN_HOUR)
						if now < wait:
							sendm(peer_id,
								f'Ход уже был проведен.\nСледующая возможность появится через {wait-now}.'
							)
							continue
						last_move = get_now_time_string()
						opponent1_inf = 0
						opponent2_inf = 0
						opponent1_tanks = 0
						opponent2_tanks = 0
						opponent1_planes = 0
						opponent2_planes = 0
						opp1lostinf = round((opponent2_inf/3 + opponent2_tanks*10 + opponent2_planes*10) * (opponent2_war_power/opponent1_war_power))
						if opp1lostinf > opponent1_inf:
							opp1lostinf = opponent1_inf
							opponent1_inf = 0
						else:
							opponent1_inf -= opp1lostinf
						opp2lostinf = round((opponent1_inf/3 + opponent1_tanks*10 + opponent1_planes*3) * (opponent1_war_power/opponent2_war_power))
						if opp2lostinf > opponent2_inf:
							opp2lostinf = opponent2_inf
							opponent2_inf = 0
						else:
							opponent2_inf -= opp2lostinf
						opp1losttanks = round((opponent2_inf/1000 + opponent2_tanks/3 + opponent2_planes/6) * (opponent2_war_power/opponent1_war_power))
						if opp1losttanks > opponent1_tanks:
							opp1losttanks = opponent1_tanks
							opponent1_tanks = 0
						else:
							opponent1_tanks -= opp1losttanks
						opp2losttanks = round((opponent1_inf/1000 + opponent1_tanks/3 + opponent1_planes*3) * (opponent1_war_power/opponent2_war_power))
						if opp2losttanks > opponent2_tanks:
							opp2losttanks = opponent2_tanks
							opponent2_tanks = 0
						else:
							opponent2_tanks -= opp2losttanks
						opp1lostplanes = round((opponent2_inf/1000 + opponent2_planes/3) * (opponent2_war_power/opponent1_war_power))
						if opp1lostplanes > opponent1_planes:
							opp1lostplanes = opponent1_planes
							opponent1_planes = 0
						else:
							opponent1_planes -= opp1lostplanes
						opp2lostplanes = round((opponent1_inf/1000 + opponent1_planes/3) * (opponent1_war_power/opponent2_war_power))
						if opp2lostplanes > opponent2_planes:
							opp2lostplanes = opponent2_planes
							opponent2_planes = 0
						else:
							opponent2_planes -= opp2lostplanes
						cur.execute('')
						cur.execute('')
						cur.execute('')
						db.commit()
						if opponent1_inf < 100 and opponent1_tanks <= 1 and opponent1_planes <= 1: flag_end2 = True
						if opponent2_inf < 100 and opponent2_tanks <= 1 and opponent2_planes <= 1: flag_end1 = True
						if opponent1_inf < 100 and opponent2_inf < 100 and opponent1_tanks <= 1 and opponent2_tanks <= 1 and opponent1_planes <= 1 and opponent2_planes <= 1:
							flag_end1 = False
							flag_end2 = False
						if flag_end1 and not flag_end2:
							end = cur.execute('').fetchall()
							cur.execute(f'DELETE FROM WARS WHERE CIDOPPONENT1={0} AND CIDOPPONENT2={0}')
							db.commit()
							sendm(0,
								f"Ваша страна одержала победу с {get_country_name(0)}!\n"+
								f"Полная сводка о потерях составила:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							sendm(0,
								f"Ваша страна потерпела поражение с {get_country_name(0)}.\n"+
								f"Полная сводка о потерях составила:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							sendm(2000000001,
								 "=================\n"+
								f"Страна {get_country_name(0)} одержала победу.\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов\n\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							continue
						if flag_end2 and not flag_end1:
							end = cur.execute('').fetchall()
							cur.execute(f'DELETE FROM WARS WHERE CIDOPPONENT1={0} AND CIDOPPONENT2={0}')
							db.commit()
							sendm(0,
								f"Ваша страна одержала победу!\n"+
								f"Полная сводка о потерях составила:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							sendm(0,
								f"Ваша страна потерпела поражение.\n"+
								f"Полная сводка о потерях составила:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							sendm(2000000001,
								 "=================\n"+
								f"Страна {get_country_name(0)} одержала победу.\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов\n\n"+
								f"Потери {get_country_name(0)} составили:\n"+
								f'{0:,}'.replace(',',' ')+f' пехоты\n'+
								f"{0} танков\n"+
								f"{0} самолетов"
							)
							continue
						sendm(0,
							f"Ваши потери после хода {0+1} составили:\n"+
							f'{opp1lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp1losttanks} танков\n"+
							f"{opp1lostplanes} самолетов\n\n"+
							f"Потери врага после хода {0+1} составили:\n"+
							f'{opp2lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp2losttanks} танков\n"+
							f"{opp2lostplanes} самолетов"
						)
						sendm(0,
							f"Ваши потери после хода {0+1} составили:\n"+
							f'{opp2lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp2losttanks} танков\n"+
							f"{opp2lostplanes} самолетов\n\n"+
							f"Потери врага после хода {0+1} составили:\n"+
							f'{opp1lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp1losttanks} танков\n"+
							f"{opp1lostplanes} самолетов"
						)
						sendm(2000000001,
							"=================\n"+
							f"Потери {get_country_name(0)} после хода {0+1} составили:\n"+
							f'{opp1lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp1losttanks} танков\n"+
							f"{opp1lostplanes} самолетов\n\n"+
							f"Потери {get_country_name(0)} после хода {0+1} составили:\n"+
							f'{opp2lostinf:,}'.replace(',',' ')+f' пехоты\n'+
							f"{opp2losttanks} танков\n"+
							f"{opp2lostplanes} самолетов"
						)
						continue
					if re.match(r'^война ракета$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'В данный момент ваша страна ни с кем не воюет.'
							)
							continue
						if 0 == peer_id:
							opp_id = 0
						else:
							opp_id = 0
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'Ошибка.'
							)
							continue
						peer_army = cur.execute('').fetchall()
						if 0 < 1:
							sendm(peer_id,
								f'У вас нет ракет.'
							)
							continue
						war_data = cur.execute('').fetchall()
						factories_amount = cur.execute('').fetchall()
						if factories_amount[0][0] < 1:
							sendm(peer_id,
								f'У противника {get_country_name(opp_id)} нет заводов.'
							)
							continue
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'У противника {get_country_name(opp_id)} уничтожен завод.'
						)
						sendm(opp_id,
							f'Противник {get_country_name(peer_id)} уничтожил ваш завод.'
						)
						continue
					if re.match(r'^война ядерка$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'В данный момент ваша страна ни с кем не воюет.'
							)
							continue
						if 0 == peer_id:
							opp_id = 0
						else:
							opp_id = 0
						war_check = cur.execute('').fetchall()
						if war_check == []:
							sendm(peer_id,
								'Ошибка.'
							)
							continue
						peer_army = cur.execute('').fetchall()
						if 0 < 1:
							sendm(peer_id,
								f'У вас нет ядерок.'
							)
							continue
						war_data = cur.execute('').fetchall()
						cities_data = cur.execute('').fetchall()
						if cities_data == []:
							sendm(peer_id,
								f'У противника {get_country_name(opp_id)} нет городов.'
							)
							continue
						factories_amount = cur.execute('').fetchall()
						factory_destroy = False
						if 0 == len(cities_data):
							factory_destroy = True
						cur.execute('')
						cur.execute('')
						if factory_destroy: cur.execute('')
						db.commit()
						sendm(peer_id,
							f'У противника {get_country_name(opp_id)} уничтожен город {0}{[""," вместе с заводом"][factory_destroy]}.'
						)
						sendm(opp_id,
							f'Противник {get_country_name(peer_id)} уничтожил ваш город {0}{[""," вместе с заводом"][factory_destroy]}.'
						)
						countries = cur.execute('').fetchall()
						for country in countries:
							if 0 == peer_id or 0 == opp_id: continue
							sendm(0,
								f'Внимание! В городе {0} страны {get_country_name(opp_id)} прогремел ядерный взрыв, '+
								f'уничтоживший {[""," как завод, так и "][factory_destroy]}целый город!'
							)
						continue
					if re.match(r'^биржа инфо( день| месяц| год|)$', lowcont):
						exchange_data = cur.execute('').fetchall()
						if exchange_data == []:
							cur.execute('')
							db.commit()
						exchange_data = cur.execute('').fetchall()
						now = get_now_time_nondate()
						last_updated = datetime.fromisoformat(0)
						wait = last_updated + timedelta(hours=EXCHANGE_UPDATE_COOLDOWN_HOUR)
						price_update = 0
						if now >= wait:
							price_update = get_price_update(old_price=0)
							changed_price = 0
							if 0 < 0.005:
								changed_price = round(0 - price_update, 5)
							elif 0 < 0.05:
								changed_price = round(0 - price_update, 4)
							elif 0 < 0.5:
								changed_price = round(0 - price_update, 3)
							else:
								changed_price = round(0 - price_update, 2)
							updated_time = datetime.isoformat(get_now_time_nondate())
							cur.execute('')
							cur.execute('')
							db.commit()
						exchange_data = cur.execute('').fetchall()
						type = re.sub('^биржа инфо ', '', lowcont)
						selectvals = ''
						selectdates = ''
						if type=='день':
							selectvals = ''
							selectdates = ''
						if type=='месяц':
							selectvals = ''
							selectdates = ''
						if type=='год':
							selectvals = ''
							selectdates = ''
						valsf = cur.execute('').fetchall()
						datesf = cur.execute('').fetchall()
						vals = [float(x[0]) for x in valsf]
						dates = [datetime.strftime(datetime.fromisoformat(x[0]), '%d/%m %H:%M:%S') for x in datesf]
						datevals = list(range(1, len(dates)+1))

						plt.figure(figsize=(16, 6))
						plt.plot(datevals, vals, marker='o', linestyle='-')

						#for i, (xi, yi) in enumerate(zip(datevals, vals)):
						#    plt.annotate(f'({yi})', (xi, yi), textcoords='offset points', xytext=(0, 10), ha='center')
						
						plt.ylabel('SAFRYLUS')
						#plt.xticks(ticks=datevals, labels=dates, rotation=45, fontsize=8)
						plt.grid(True)
						
						plt.savefig('', bbox_inches='tight')
						tries = 0
						while(True):
							if tries == 5:
								break
							try:
								if os.path.isfile(r''):
									photo = upload_photo(r'')
									attachment = f"photo{photo[0]}_{photo[1]}_{photo[2]}"
									sendma(peer_id,
										f'Курс на {datetime.strftime(datetime.fromisoformat(0), "%d/%m/%Y %H:%M:%S")}\n1 PCN за {0} SF ({abs(0)} {[["🔻", "🔺"][0 > 0], "🟰"][0==0.0]})',
										attachment
									)
									break
							except:
								tries += 1
						plt.close('all')
						continue
					if re.match(r'^биржа цена коин', lowcont):
						if not re.match(r'^биржа цена коин \d+(\.\d+)?$', lowcont):
							sendr(peer_id, forward,
								'Укажите количество'
							)
							continue
						amount = round(float(re.sub(r'^биржа цена коин ', '', lowcont)), 4)
						if amount <= 0:
							sendr(peer_id, forward,
								'Количество должно быть больше 0'
							)
							continue
						coin_price = cur.execute('').fetchall()
						safrylus_to_get_raw = 0*amount
						safrylus_to_get = math.floor(safrylus_to_get_raw)
						fee = safrylus_to_get_raw - safrylus_to_get
						sendm(peer_id,
							f'За {amount} PCN: {safrylus_to_get} SF, комиссия: {round((fee/safrylus_to_get_raw)*100, 2)}%'
						)
						continue
					if re.match(r'^биржа цена', lowcont):
						if not re.match(r'^биржа цена \d+$', lowcont):
							sendr(peer_id, forward,
								'Укажите количество'
							)
							continue
						amount = int(re.sub(r'^биржа цена ', '', lowcont))
						if amount < 1:
							sendr(peer_id, forward,
								'Количество должно быть больше 1'
							)
							continue
						coin_price = cur.execute('').fetchall()
						sendm(peer_id,
							f'За '+f'{amount:,}'.replace(',',' ')+f' SF: {round(amount/coin_price[0][0], 2)} PCN.'
						)
						continue
					if re.match(r'^биржа купить', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if not re.match(r'^биржа купить \d+$', lowcont):
							sendr(peer_id, forward,
								'Укажите количество SF'
							)
							continue
						amount = int(re.sub(r'^биржа купить ', '', lowcont))
						if amount < 1:
							sendr(peer_id, forward,
								'Укажите корректное количество SF'
							)
							continue
						if 0 < amount:
							sendr(peer_id, forward,
								f'Вам не хватает '+f'{amount-0:,}'.replace(',',' ')+f' SF для покупки PCN'
							)
							continue
						exchange_country_stats = cur.execute('').fetchall()
						if exchange_country_stats == []:
							cur.execute('')
							db.commit()
						coin_price = cur.execute('').fetchall()
						amount_to_buy = round(amount/coin_price[0][0], 2)
						cur.execute('')
						if not peer_id == 2000000001:
							cur.execute('')
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы приобрели {amount_to_buy} PCN'
						)
						continue
					if re.match(r'^биржа продать', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if not re.match(r'^биржа продать \d+(.\d+)?$', lowcont):
							sendr(peer_id, forward,
								'Укажите количество PCN'
							)
							continue
						amount = round(float(re.sub(r'^биржа продать ', '', lowcont)), 4)
						if amount <= 0:
							sendr(peer_id, forward,
								'Укажите корректное количество PCN'
							)
							continue
						if 0 < amount:
							sendr(peer_id, forward,
								f'Вам не хватает '+f'{amount-0:,}'.replace(',',' ')+f' PCN для продажи'
							)
							continue
						exchange_country_stats = cur.execute('').fetchall()
						if exchange_country_stats == []:
							cur.execute('')
							db.commit()
						coin_price = cur.execute('').fetchall()
						safrylus_to_get_raw = amount*coin_price[0][0]
						safrylus_to_get = math.floor(safrylus_to_get_raw)
						fee = safrylus_to_get_raw - safrylus_to_get
						cur.execute('')
						if not peer_id == 2000000001:
							cur.execute('')
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Вы продали {amount} PCN за '+f'{safrylus_to_get:,}'.replace(',',' ')+f' SF, комиссия составила: {round((fee/safrylus_to_get_raw)*100, 2)}%.'
						)
						continue
					if re.match(r'^биржа стата$', lowcont):
						exchange_stats = cur.execute('').fetchall()
						exchange_country_stats = cur.execute('').fetchall()
						coins_in_total = cur.execute('').fetchall()
						if exchange_country_stats == []:
							cur.execute('')
							db.commit()
							exchange_country_stats = cur.execute('').fetchall()
						profit_amount = 0-0
						sendm(peer_id,
							f'Статистика биржи:\n'+
							f'Коинов куплено всего: '+f'{round(0, 2):,}'.replace(',',' ')+f' PCN\n'+
							f'Коинов продано всего: '+f'{round(0, 2):,}'.replace(',',' ')+f' PCN\n'+
							f'Коинов в обороте всего: '+f'{round(0, 2):,}'.replace(',',' ')+f' PCN\n'+
							f'Сафрила получено всего: '+f'{0:,}'.replace(',',' ')+f' SF\n'+
							f'Сафрила потрачено всего: '+f'{0:,}'.replace(',',' ')+f' SF\n'+
							f'Ваш доход: '+f'{0:,}'.replace(',',' ')+f' SF\n'+
							f'{["Ваша прибыль", "Ваш убыток"][profit_amount<0]}: '+f'{abs(profit_amount):,}'.replace(',',' ')+f' SF'
						)
						continue
					if re.match(r'^экономика инфо', lowcont):
						safrylus_total = cur.execute('').fetchall()[0][0]
						resources_total = cur.execute('').fetchall()[0][0]
						coins_total = round(cur.execute('').fetchall()[0][0], 4)
						average_index = cur.execute('').fetchall()[0][0]
						difference_index = 0-average_index
						mean_of = (0+average_index)/2
						sendm(peer_id, 
							f'Сафрил: '+f'{safrylus_total:,}'.replace(',', ' ')+' SF'+
							f'\nСырье: '+f'{resources_total:,}'.replace(',', ' ')+' ед.'+
							f'\nКоины: '+f'{coins_total:,}'.replace(',', ' ')+' PCN'+
							f'\nСредний индекс экономики: {round(average_index, 2)}'+
							f'\nВаша экономика на {round((abs(difference_index)/mean_of)*100, 2)}% {["лучше", "хуже"][difference_index<0]}'
						)
					if re.match(r'^транзакции', lowcont):
						page = 0
						offset = 0
						if re.match(r'^транзакции -\d+$', lowcont):
							sendm(peer_id,
								'Число не должно быть отрицательным.'
							)
							continue
						if re.match(r'^транзакции \d+$', lowcont):
							page = int(lowcont.split('транзакции ')[1])-1
							offset = page * 10
						#DATE TEXT, FROMID TEXT, TOID INT, AMOUNT INT, FEE INT
						transactions_offset = cur.execute('').fetchall()
						info = '=Транзакции=\nДАТА ОТ К СУММА КОМ-ИЯ'
						if transactions_offset == []:
							info += '\nПусто'
							sendm(peer_id,
								info
							)
							continue
						count = offset+1
						for transaction in transactions_offset:
							fromid = int(transaction[1])
							toid = transaction[2]
							if fromid == 2000000001:
								fromid = 'PWGInfSt'
							if toid == 2000000001:
								toid = 'PWGInfSt'
							info += f'\n{datetime.strftime(datetime.fromisoformat(transaction[0]), "%d/%m/%Y %H:%M:%S")} {fromid} {toid} {transaction[3]} {round(transaction[4], 2)} PCN'
							count += 1
						info += f'\n=Страница {page+1}/{math.ceil(len(transactions_offset)/10)}='
						sendm(peer_id,
							info
						)
						continue
					if re.match(r'^бот сво$', lowcont):
						if 'reply_message' in event.obj['message']:
							if len(event.obj['message']['reply_message']['text']) != 0:
								textsvo = SVOFinder.parse(event.obj['message']['reply_message']['text'])
								if textsvo is not None:
									sendr(peer_id,
										forward,
										textsvo
									)
								else:
									sendr(peer_id,
										forward,
										'Сообщение слишком длинное!'
									)
								continue
							sendr(peer_id,
								  forward,
								  'Сообщение пустое!'
							)
							continue
						if len(event.obj['message']['fwd_messages']) != 0:
							if len(event.obj['message']['fwd_messages'][0]['text']) != 0:
								textsvo = SVOFinder.parse(event.obj['message']['fwd_messages'][0]['text'])
								if textsvo is not None:
									sendr(peer_id,
										forward,
										textsvo
									)
								else:
									sendr(peer_id,
										forward,
										'Сообщение слишком длинное!'
									)
								continue
							sendr(peer_id,
								forward,
								'Сообщение пустое!'
							)
						sendr(peer_id,
							  forward,
							  'Перешлите сообщение для обработки'
						)
						continue
					if re.match(r'^пвг \+модер', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if 'reply_message' in event.obj["message"]:
							moder_id = event.obj['message']['reply_message']['from_id']
							moder_check = cur.execute('').fetchall()
							if not moder_check == []:
								sendr(peer_id, forward,
									'Данный пользователь уже является модератором.'
								)
								continue
							cur.execute('')
						else:
							moder_match = re.match(r'^пвг \+модер \[id(?P<id>[0-9]+)\|(@|\*)?[\w\W]+\]$', event.obj["message"]["text"])
							if not moder_match:
								sendr(peer_id, forward,
									'Что-то пошло не так.\nОбратитесь к админу /admins'
								)
								continue
							groups = moder_match.groupdict()
							moder_id = groups.get('id')
							moder_check = cur.execute('').fetchall()
							if not moder_check == []:
								sendr(peer_id, forward,
									'Данный пользователь уже является модератором.'
								)
								continue
							cur.execute('')
						db.commit()
						sendm(peer_id,
							f'[id{moder_id}|Пользователь] теперь является модератором данной беседы.'
						)
						continue
					if re.match(r'^пвг -модер', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if 'reply_message' in event.obj["message"]:
							moder_id = event.obj['message']['reply_message']['from_id']
							moder_check = cur.execute('').fetchall()
							if moder_check == []:
								sendr(peer_id, forward,
									'Данный пользователь не является модератором.'
								)
								continue
							cur.execute('')
						else:
							moder_match = re.match(r'^пвг -модер \[id(?P<id>[0-9]+)\|(@|\*)?[\w\W]+\]$', event.obj["message"]["text"])
							if not moder_match:
								sendr(peer_id, forward,
									'Что-то пошло не так.\nОбратитесь к админу /admins'
								)
								continue
							groups = moder_match.groupdict()
							moder_id = groups.get('id')
							moder_check = cur.execute('').fetchall()
							if moder_check == []:
								sendr(peer_id, forward,
									'Данный пользователь не является модератором.'
								)
								continue
							cur.execute('')
						db.commit()
						sendm(peer_id,
							f'[id{moder_id}|Пользователь] больше не является модератором данной беседы.'
						)
						continue
					if re.match(r'^пвг модераторы$', lowcont):
						moders = cur.execute('').fetchall()
						if not moders:
							sendm(peer_id,
								'Список модераторов пуст.'
							)
							continue
						result_message = 'Модераторы беседы'
						for moder in moders:
							result_message += f'\n[id{moder[0]}|{get_name(moder[0])}]'
						sendm(peer_id,
							result_message
						)
						continue
					if re.match(r'^о боте$', lowcont):
						botabout = cur.execute('').fetchall()
						sendm(peer_id,
							f"ПВГ Бот. Версия v{botabout[0][0]}.{botabout[0][1]}.{botabout[0][2]}.{botabout[0][3]}"
						)
						continue
					if re.match(r'^карта последняя$', lowcont):
						maps_desc = cur.execute('').fetchall()
						sendma(peer_id,
							'',
							maps_desc[0][0]
						)
						continue
					if re.match(r'^/admins$', lowcont):
						admins = vk.groups.getById(group_id = 'vcplanet', fields='contacts')
						info = 'Администраторы бота'
						for admin in admins[0]['contacts']:
							info += f"\n[id{admin['user_id']}|{get_name(admin['user_id'])}] ({admin['desc']})"
						sendm(peer_id,
							info
						)
						continue

					# АДМИН КОМАНДЫ

					if re.match(r'^/a getid$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						sendm(peer_id,
							re.sub(r'^\[id(?P<id>[0-9]+)\|(@|\*)?[\w\W]+\]', r'\g<id>', event.obj['message']['reply_message']['text'])
						)
						continue
					if re.match(r'^пвг -смс$', lowcont):
						if not is_admin(peer_id, from_id):
							sendm(peer_id,
								'Вы не администратор беседы.'
							)
							continue
						if not 'reply_message' in event.obj['message']:
							sendm(peer_id,
								'Нечего удалять.'
							)
							continue
						id_delete = event.obj['message']['reply_message']['conversation_message_id']
						vk.messages.delete(
							cmids=id_delete,
							delete_for_all=1,
							peer_id=peer_id
						)
						continue
					if re.match(r'^/a gen saf ', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						if not re.match(r'^/a gen saf -?\d+$', lowcont):
							continue
						amount = int(re.sub(r'^/a gen saf ', '', lowcont))
						if amount <= 0:
							continue
						cur.execute('')
						db.commit()
						sendr(peer_id, forward,
							"Готово"
						)
						continue
					if re.match(r'^/a gen res ', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						if not re.match(r'^/a gen res -?\d+$', lowcont):
							continue
						amount = int(re.sub(r'^/a gen res ', '', lowcont))
						if amount <= 0:
							continue
						cur.execute('')
						db.commit()
						sendr(peer_id, forward,
							"Готово"
						)
						continue
					if re.match(r'^/a exec([\w\W]+)$', cont):
						if not is_admin_of_bot(from_id):
							continue
						pattern = r'^/a exec\((?P<n>[\w\W]+)\)$'
						code = re.sub(pattern, r'\g<n>', cont)
						try:
							result = cur.execute('').fetchall()
						except:
							sendr(peer_id, forward,
								"Error"
							)
							continue
						db.commit()
						if result == []:
							continue
						sendr(peer_id, forward,
							result
						)
						continue
					if re.match(r'^/a i patch$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						cur.execute('')
						db.commit()
						continue
					if re.match(r'^/a i minor$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						cur.execute('')
						db.commit()
						continue
					if re.match(r'^/a set area (\d+) (\d+)$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						pattern = r'^/a set area (?P<id>\d+) (?P<area>\d+)$'
						id = re.sub(pattern, r'\g<id>', lowcont)
						area = re.sub(pattern, r'\g<area>', lowcont)
						full_id = get_id(id)
						old_data = cur.execute('').fetchall()
						cur.execute('')
						db.commit()
						sendr(peer_id, forward,
							  f'{old_data[0][0]}: {old_data[0][1]} -> {area}'
						)
						continue
					if re.match(r'^/cmd list$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						sendu(from_id,'')
						continue
				elif event.from_user:
					if re.match(r'^подтвердить \d+$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						cid = lowcont.split(' ')[1]
						request_check = cur.execute('').fetchall()
						if request_check == []:
							sendm(peer_id,
								f'Запроса от страны с указанным id: {cid} не существует.'
							)
							continue
						if request_check[0][1] == 1:
							sendm(peer_id,
								f'Страна (id: {cid}) уже зарегистрирована.'
							)
							continue
						now = get_now_string()
						chat_title = vk.messages.getConversationsById(peer_ids=cid)['items'][0]['chat_settings']['title']
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Стране (id: {cid}) была подтверждена регистрация.'
						)
						sendm(cid,
							'Ваша страна была успешно зарегистрирована\n'+
							'Вам тепепрь доступны все возможности бота.\n\n'+
							'На данный момент название вашей страны - ваша беседа, чтобы его поменять, используйте команду "страна название <название>".\n'+
							'Также, привяжите ссылку вашей страны командой "страна ссылка <ссылка>", если вы не сделали оного при регистрации.'
						)
						continue
					if re.match(r'^отказ \d+$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						cid = lowcont.split(' ')[1]
						request_check = cur.execute('').fetchall()
						if request_check == []:
							sendm(peer_id,
								f'Запроса от страны с указанным id: {cid} не существует.'
							)
							continue
						now = get_now_string()
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Стране (id: {cid}) было отказано в регистрации.'
						)
						sendm(cid,
							f'Вашей стране было отказано в регистрации.'
						)
						continue
					if re.match(r'^/a load map$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						try:
							sizes = []
							if not event.obj['message']['attachments'] == []:
								if event.obj['message']['attachments'][0]['type'] == 'photo':
									for size in event.obj['message']['attachments'][0]['photo']['sizes']:
										sizes.append(size['type'])
							size_to = sorted(sizes)[-1]
							url = ''
							for size in event.obj['message']['attachments'][0]['photo']['sizes']:
								if size['type'] == size_to:
									url = size['url']
									break
							image = requests.get(url).content
							with open(r'', 'wb') as handler:
								handler.write(image)
							photo = upload_photo(r'')
							attachment = f"photo{photo[0]}_{photo[1]}_{photo[2]}"
							now = datetime.now(pytz.timezone('Europe/Moscow'))
							name = datetime.strftime(now, "map_%d-%m-%Y_%H-%M-%S")
							maps_amount = cur.execute('').fetchall()
							cur.execute('')
							db.commit()
							sendma(peer_id,
								'Карта загружена.',
								attachment
							)
						except Exception as e:
							sendm(peer_id,
								f'{e}\nОшибка загрузки.'
							)
							continue
						continue
					if re.match(r'^/a send map recent$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						maps = cur.execute('').fetchall()
						maps_amount = cur.execute('').fetchall()
						if maps == []:
							sendm(peer_id,
								'Карт нет.'
							)
							continue
						attachment = maps[-1][0]
						countries = cur.execute('').fetchall()
						for country in countries:
							sendma(country[0],
								'Карта обновлена.',
								attachment
							)
						sendm(peer_id,
							'Карта разослана по странам.'
						)
						continue
					if re.match(r'^/a s i', lowcont):
						if not re.match(r'/a s i (\d+)$', lowcont):
							continue
						id = int(re.sub(r'/a s i (?P<id>\d+)$', r'\g<id>', lowcont))
						try:
							sizes = []
							if not event.obj['message']['attachments'] == []:
								if not event.obj['message']['attachments'][0]['type'] == 'photo':
									continue
							photo = event.obj['message']['attachments'][0]['photo']
							attachment = f"photo{photo['owner_id']}_{photo['id']}_{photo['access_key']}"
							sendma(parse_id(id), '', attachment)
							continue
						except:
							continue
					if re.match(r'^/a list maps$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						maps = cur.execute('').fetchall()
						info = 'Loaded maps:'
						for map in maps:
							info += f'\n{map[0]} - {map[2]}'
						sendm(peer_id,
							[info, "Empty"][info==""]
						)
						continue
					if re.match(r'^/a map preview', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						if re.match(r'^/a map preview$', lowcont):
							sendm(peer_id,
								'Укажите айди карты.'
							)
							continue
						id = lowcont.split('/admin preview map ')[1]
						map = cur.execute('').fetchall()
						if map == []:
							sendm(peer_id,
								'Карты с указанным айди не существует.'
							)
							continue
						sendma(peer_id,
							map[0][1],
							map[0][0]
						)
						continue
					if re.match(r'^/a block$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						block = not block
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Бот был {["разблокирован", "заблокирован"][block]}.'
						)
						countries = cur.execute('').fetchall()
						for country in countries:
							sendm(country[0],
								f'{["Технические работы завершены, можно продолжить использование.", "Ведутся технические работы, любые команды будут игнорироваться."][block]}',
							)
						continue
					if re.match(r'^/a an', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						if not re.match(r'^/a an "(?P<a>[\s\S]+)"$', lowcont):
							sendm(peer_id,
								'Введите сообщение'
							)
							continue
						message = re.sub(r'^/a an "(?P<message>[\s\S]+)"$', r'\g<message>', cont)
						countries = cur.execute('').fetchall()
						for country in countries:
							sendm(country[0],
								f'{message}',
							)
						continue
					if re.match(r'^/a cids$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						sendm(peer_id,
							"\n".join(str(x[0]) for x in cur.execute('').fetchall())
						)
						continue
					if re.match(r'^/a parse id \d+$', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						cid = lowcont.split('/a parse id ')[1]
						sendm(peer_id,
							parse_id(cid)
						)
						continue
					if re.match(r'^/a delete country \d+', lowcont):
						if not is_admin_of_bot(from_id):
							sendm(peer_id,
								'Вы не администратор.'
							)
							continue
						id_raw = lowcont.split('/a delete country ')[1]
						id = None
						if re.match(r'^20{1,}((?!0))[0-9]+$', str(id_raw)):
							id = id_raw
						else:
							id = get_id(id_raw)
						cur.execute('')
						cur.execute('')
						cur.execute('')
						cur.execute('')
						cur.execute('')
						db.commit()
						sendm(peer_id,
							f'Страна (id: {id}) удалена.'
						)
					if re.match(r'^/cmd list$', lowcont):
						if not is_admin_of_bot(from_id):
							continue
						sendu(from_id,'')
						continue
					if re.match(r'/a s p', lowcont):
						if not re.match(r'^/a s p (?P<m>\d+) "(?P<a>[\s\S]+)"$', lowcont):
							continue
						message = re.sub(r'^/a s p (?P<id>\d+) "(?P<message>[\s\S]+)"$', r'\g<message>', cont)
						id = int(re.sub(r'^/a s p (?P<id>\d+) "(?P<message>[\s\S]+)"$', r'\g<id>', cont))
						sendm(parse_id(id), message)
						continue
			if event.type == VkBotEventType.WALL_POST_NEW:
				countries = cur.execute('').fetchall()
				attachment = f'wall{event.obj["owner_id"]}_{event.obj["id"]}'
				for country in countries:
					sendma(country[0],
						'Новый пост в группе!',
						attachment
					)
				continue
	except KeyboardInterrupt as e:
		print("Bot has been shut down")
		sys.exit()
	except Exception as e:
		traceback.print_exc()
		print(f'<{get_now_time_string()}> Bot received error - restarting...')