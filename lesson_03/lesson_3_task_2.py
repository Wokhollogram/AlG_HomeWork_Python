from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 15 Pro", "+79161234567"),
    Smartphone("Samsung", "Galaxy S24 Ultra", "+79262345678"),
    Smartphone("Xiaomi", "Redmi Note 13", "+79373456789"),
    Smartphone("Huawei", "P60 Pro", "+79484567890"),
    Smartphone("Google", "Pixel 8 Pro", "+79595678901"),
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")