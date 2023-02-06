import json
from yookassa import Configuration, Payment
from os import environ
from dotenvy import load_env, read_file
import asyncio

load_env(read_file('.env'))
Configuration.account_id = environ.get('SHOP_ID')
Configuration.secret_key = environ.get('SHOP_API_TOKEN')

def payment(value,description):
	payment = Payment.create({
    "amount": {
        "value": value,
        "currency": "RUB"
    },
    "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "урл редиректа"
    },
    "capture": True,
    "description": description
	})
	return json.loads(payment.json())


async def check_payment(payment_id):
	payment = json.loads((Payment.find_one(payment_id)).json())
	while payment['status'] == 'pending':
		payment = json.loads((Payment.find_one(payment_id)).json())
		await asyncio.sleep(3)

	if payment['status']=='succeeded':
		print("SUCCSESS RETURN")
		print(payment)
		return True
	else:
		print("BAD RETURN")
		print(payment)
		return False


#print(payment('59','Оплата услуги'))