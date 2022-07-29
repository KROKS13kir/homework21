from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, name, quantity):
        pass

    @abstractmethod
    def remove(self, name, quantity):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):

    def __init__(self, items: dict = {}, capacity: int = 100) -> None:
        super().__init__(items, capacity)

    def add(self, name, quantity):
        if name in self._items.keys():
            self._items[name] += quantity
            self._capacity -= quantity
        else:
            self._items[name] = quantity
            self._capacity -= quantity

    def remove(self, name, quantity):
        self._items[name] -= quantity
        self._capacity += quantity

    @property
    def get_free_space(self):
        return self._capacity

    @get_free_space.setter
    def get_free_space(self, new_cap_value):
        self._capacity = new_cap_value

    @property
    def get_items(self):
        return self._items

    @get_items.setter
    def get_items(self, new_items_value):
        self._items = new_items_value
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())

    def _check_free_space(self, quantity):
        if 100 >= self._capacity + quantity & self._capacity + quantity >= 0:
            return True
        return False

    def _max_position(self) -> bool:
        return True


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20

    def _check_free_space(self, count: int) -> bool:
        if 20 >= self._capacity + count >= 0:
            return True
        return False

    def _max_position(self) -> bool:
        if len(self._items) <= 5:
            return True
        return False


class Request:
    def __init__(self, info):
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split(" ")

    def __repr__(self):
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to}"


def main():
    while True:
        user_input = input("Введите запрос: ")

        if user_input == "stop" or user_input == 'стоп':
            break

        request = Request(user_input)
        store._items = store_items

        from_ = store if request.from_ == 'склад' else shop
        to = shop if request.to == 'магазин' else store

        if request.product in from_.get_items:
            print(f'Нужный товар есть в пункте \"{request.from_}\"')
        else:
            print(f'В пункте \"{request.from_}\" нет такого товара')
            continue

        if from_.get_items[request.product] >= request.amount:
            print(f'Нужное количество есть в пункте \"{request.from_}\"')
        else:
            print(f'Не хватает на {request.from_}, попробуйте заказать меньше')
            continue

        if to.get_free_space >= request.amount:
            print(f'В пункте \"{request.to}\" достаточно места')
        else:
            print(f'В {request.to} недостаточно места, попробуйте что-то другое')
            continue

        if request.to == 'магазин' and to.get_unique_items_count == 5 and request.product not in to.get_items:
            print("В магазине достаточно уникальных значений")
            continue

        store.remove(request.product, request.amount)
        print(f'Курьер забрал {request.amount} {request.product} из пункта \"{request.from_}\"')
        print(f'Курьер везёт {request.amount} {request.product} из пункта \"{request.from_}\" в пункт \"{request.to}\"')
        shop.add(request.product, request.amount)
        print(f'Курьер доставил {request.amount} {request.product} в пункт \"{request.to}\"')

        print("-" * 30)
        print('На складе:')
        for name, quantity in store.get_items.items():
            print(f'{name}: {quantity}')
        print(f"Свободного места {store.get_free_space}")

        print("-" * 30)
        print('В магазине:')
        for name, quantity in shop.get_items.items():
            print(f'{name}: {quantity}')
        print(f"Свободного места {shop.get_free_space}")
        print("-" * 30)


if __name__ == "__main__":

    store_items = {
        'чипсы': 10,
        "сок": 20,
        "кофе": 7,
    }
    capacit = 100
    for i in store_items.values():
        capacit -= i
    store = Store(capacity=capacit)
    shop = Shop()
    main()
