

# Статусы заявок
STATUS_NEW = "новая"
STATUS_CONFIRMED = "подтвержденная"
STATUS_CANCELLED = "отмененная"
STATUS_COMPLETED = "выполненная"

# Продукты
PRODUCTS = [
    "Молоко",
    "Сметана",
    "Творог",
    "Кефир",
    "Масло",
]

# Заявки (пример данных)
ORDERS = [
    {
        "id": 1,
        "client_name": "Иван Иванов",
        "products": ["кефир", "масло"],
        "phone": "+7 123 456-78-90",
        "date": "2025-07-30",
        "status": STATUS_NEW,
    },
    {
        "id": 2,
        "client_name": "Мария Петрова",
        "products": ["молоко","сметана"],
        "phone": "+7 987 654-32-10",
        "date": "2025-07-29",
        "status": STATUS_CONFIRMED,
    },
    {
        "id": 3,
        "client_name": "Алла Захарова",
        "products": ["творог","сметана"],
        "phone": "+7 456 789-01-23",
        "date": "2025-07-25",
        "status": STATUS_CANCELLED,
    },
    {
        "id": 4,
        "client_name": "Пётр Абросимов",
        "products": ["масло","кефир"],
        "phone": "+7 321 654-98-76",
        "date": "2025-07-29",
        "status": STATUS_COMPLETED,
    },
    {
        "id": 5,
        "client_name": "Николай Изжогов",
        "products": ["масло","молоко"],
        "phone": "+7 654 321-09-87",
        "date": "2025-07-27",
        "status": STATUS_NEW,
    },
]
