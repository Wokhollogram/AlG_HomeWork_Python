from Address import Address
from Mailing import Mailing

to_addr = Address("123456", "Москва", "ул. Тверская", "10", "25")
from_addr = Address("654321", "Санкт-Петербург", "Невский пр.", "5", "12")

mailing = Mailing(
    to_address=to_addr,
    from_address=from_addr,
    cost=350,
    track="RU123456789"
)

print(
    f"Отправление {mailing.track} "
    f"из {mailing.from_address.index}, {mailing.from_address.city}, "
    f"{mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartment} "
    f"в {mailing.to_address.index}, {mailing.to_address.city}, "
    f"{mailing.to_address.street}, {mailing.to_address.house} - {mailing.to_address.apartment}. "
    f"Стоимость {mailing.cost} рублей."
)