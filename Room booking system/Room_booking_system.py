class ReservationException(Exception):
    pass


class Room:
    """
    Class: as arguments gets the type and amount of free rooms, returns available free rooms type and count.
    class field 1. room_type: rooms' type (penthouse, double, single, etc  - string)
    class field 2. count: amount of rooms (int)
    methods:
    1. __repr__()
    2. get_type():  returns the type of the room
    3. get_count(): returns the amount of free rooms
    4. reserve(): takes room's count - returns message about amount of successfully or not reserved rooms.
    5. checkout(): takes room's count - returns messagea about amount of successfully or not checked out rooms.
    """

    def __init__(self, room_type, count):
        self.__room_type = room_type
        self.__count = count
        self.__total_rooms_count = count

    def __repr__(self):
        return f'In the hotel there is {self.__count} {self.__room_type}'

    def get_type(self):
        return self.__room_type

    def get_count(self):
        return self.__count

    def reserve(self, cnt):
        try:
            if cnt > self.__count:
                raise ReservationException
        except ReservationException:
            print(f'Room.reserve(): Incorrect number of free rooms. We have only {self.__count} available rooms.')
        else:
            self.__count -= cnt
            print(f'{cnt} rooms has been successfully reserved.')

    def checkout(self, cnt):
        reserved_rooms_count = self.__total_rooms_count - self.__count
        try:
            if reserved_rooms_count < cnt:
                raise ReservationException
        except ReservationException:
            print(f'Room.checkout(): Incorrect number of rooms for checking out. You have reserved only {reserved_rooms_count} rooms.')
        else:
            self.__count += cnt
            print(f'{cnt} rooms has been successfully checked out.')


class Hotel:
    """
    Class: as arguments takes hotel's name and list of Room type objects.
    class fields:
    1. name - str, hotel's name
    2.rating - int, hotel's rating
    3.rater count - int, counts how many different customers have rated
    4. rooms - lst, takes list of Room type objects
    methods:
    1. set_rating(): takes rating, checks and add to total rating, increases total number of raters
    2. get_rating(): counts and returns the total rating of the hotel
    3. set_rooms(): to the list appends new  Room type objects
    4. get_rooms(): returns list of Room type objects
    5. get_room_by_type(): takes room_type as argument, checks if it exists in the list of rooms, returns the relevant Room object by type
    6. operation(): takes room_type, count of room, operation type(reserve or checkout), returns reserved/checked out rooms \
                   or information about incorrect type of provided room
    7. reserve(): takes room's type and count, calls operation() method
    8. checkout(): takes room's type and count, calls operation() method
    9. get_hotel_name(): returns hotel's name

    """

    def __init__(self, name, rooms_list):
        self.__name = name
        self.__rating = 0
        self.__rater_count = 0
        self.__rooms = rooms_list

    def get_hotel_name(self):
        return self.__name

    def set_rating(self, rating):
        if rating < 1 or rating > 6:
            rating = 5
        self.__rating += rating
        self.__rater_count += 1
        print(f'Thank you for rating, you rated {rating} for the {self.get_hotel_name()} hotel.')

    def get_rating(self):
        if self.__rater_count == 0:
            return 0
        self.__rating /= self.__rater_count
        return self.__rating

    def set_rooms(self, room):
        self.__rooms.append(room)

    def get_room_by_type(self, room_type):
        for r in self.__rooms:
            if r.get_type() == room_type:
                return r
        return None

    def get_rooms(self):
        return self.__rooms

    def operation(self, room_type, cnt, operation_type):
        room = self.get_room_by_type(room_type)

        try:
            if room is None:
                raise ReservationException
        except ReservationException:
            print(f"Hotel.{operation_type} : Incorrect room type. Provided {room_type} room type is not valid.")
        else:
            if operation_type == 'reserve()':
                room.reserve(cnt)
            elif operation_type == 'checkout()':
                room.checkout(cnt)

    def reserve(self, room_type, cnt):
        self.operation(room_type, cnt, 'reserve()')

    def checkout(self, room_type, cnt):
        self.operation(room_type, cnt, 'checkout()')


class Customer:
    """
    Class: as argument takes list of hotels
    class field:
    1. hotel_list - list, list of hotels
    2. room_type - str, the room type reserved by each customer
    3. room_count_by_type - int, count of room reserved by each customer
    4. hotel_name - str, name of hotel where was reserved room by each customer
    5. hotel_rating - int, rating of hotel
    methods:
    1. get_hotel_by_name(): checks if the hotel exists in the list of hotels or not and return Hotel type object
    2. reservation(): as argument takes hotel's name, room's type and count, through calling hotel reservation \
                      returns message about successfully or not room's reserving.
    3. checking_out(): works same as reservation()
    4. rate(): through Hotel.set_rating() rates Hotel, where was reserved the room.
    5. get_name_of_reserved_hotel(): gets the name of reserved hotel
    6. get_reserved_room_type(): gets type of reserved room
    7. get_reserved_room_count_by_type(): gets count of reserved room
    8. get_hotels_rating(): gets rating of hotel
    """

    def __init__(self, hotel_list):
        self.__hotel_list = hotel_list
        self.__room_type = None
        self.__room_count_by_type = 0
        self.__hotel_name = None
        self.__hotel_rating = 0

    def get_hotel_by_name(self, name):
        for n in self.__hotel_list:
            if name == n.get_hotel_name():
                return n
        return None

    def get_hotels_rating(self, hotel_name):
        for hotel in self.__hotel_list:
            if hotel_name == hotel.get_hotel_name():
                return hotel.get_rating()

    def reservation(self, hotel_name, room_type, room_count):
        hotel = self.get_hotel_by_name(hotel_name)

        try:
            if hotel is None:
                raise ReservationException
        except ReservationException:
            print(f"Customer reservation(): There isn't hotel by {hotel_name}.")
        else:
            self.__hotel_name = hotel_name
            self.__room_type = room_type
            self.__room_count_by_type = room_count
            return hotel.reserve(room_type, room_count)

    def checking_out(self, hotel_name, room_type, room_count):
        hotel = self.get_hotel_by_name(hotel_name)
        return hotel.checkout(room_type, room_count)

    def rate(self, hotel_name, rate):
        hotel = self.get_hotel_by_name(hotel_name)
        return hotel.set_rating(rate)

    def get_name_of_reserved_hotel(self):
        return self.__hotel_name

    def get_reserved_room_type(self):
        return self.__room_type

    def get_reserved_room_count_by_type(self):
        return self.__room_count_by_type


class IdGenerator:
    """
    Class: as argument gets object's type(class field)
    method - generate_id(): generates id for specific objects(customer, room, hotel) and returns each one
    """

    def __init__(self, object_type):
        self.__type = object_type

    def generate_id(self):
        import random
        import string
        size = 4
        letters = ''.join(random.sample(string.ascii_letters, size))
        numbers = random.randint(10, 1000)

        # str(object_type), example:  str(Room) -> <class '__main__.Room'>, object's first letter = 17th index
        object_type_first_letter = str(type(self.__type)).lower()[17]
        id = object_type_first_letter + str(numbers) + letters

        return id


class Booking:
    """
    Class: argument takes list of customer(class field- type:list)
    other fields: customer_data - dict(), saves information about each customer's id, reserved hotel, room's type and count
    methods:
    1. check_customer(): as argument takes customer, returns- checks if each customer exists in the customer list
    2. set_customer_data(): as argument takes customer, \
                            returns information about each customer's id, reserved hotel, room's type and count
    3. get_customer_data_to_csv(): collecting reservation data by customers to csv file

    """

    def __init__(self, customers_list):
        self.__customers_list = customers_list
        self.__customer_data = dict()

    def check_customer(self, customer):
        try:
            if customer not in self.__customer_data:
                raise ValueError
        except ValueError:
            print(f'Booking.check_customer(): there is not the {customer} customer object.')
        else:
            return customer

    def set_customer_data(self, customer):
        id = IdGenerator(customer).generate_id()
        hotel_name = customer.get_name_of_reserved_hotel()
        room_type = customer.get_reserved_room_type()
        room_count = customer.get_reserved_room_count_by_type()
        hotel_rating = customer.get_hotels_rating(hotel_name)

        self.__customer_data.update(
            {customer:
                {'ID': id,
                 'hotel_name': hotel_name,
                 'room_type': room_type,
                 'room_count': room_count,
                 'hotel_rating': hotel_rating}
             }
        )
        return self.__customer_data

    def get_customer_data_to_csv(self):

        with open('room_booking_system.csv', 'w') as res:
            import csv
            import numpy as np
            fieldnames = ['customer_id', 'reserved_hotel', 'hotel_rating', 'reserved_room_type', 'reserved_room_count']
            writer = csv.DictWriter(res, fieldnames=fieldnames)
            writer.writeheader()

            for customer in self.__customers_list:
                custom_data = self.set_customer_data(customer)

                id = custom_data[customer]['ID']
                hotel = custom_data[customer]['hotel_name']
                room_type = custom_data[customer]['room_type']
                room_count = custom_data[customer]['room_count']
                hotel_rating = custom_data[customer]['hotel_rating']

                if hotel is None:
                    hotel = np.nan
                    hotel_rating = np.nan
                    room_type = np.nan
                    room_count = np.nan

                writer.writerow(
                    {'customer_id': id,
                     'reserved_hotel': hotel,
                     'hotel_rating': hotel_rating,
                     'reserved_room_type': room_type,
                     'reserved_room_count': room_count
                     }
                )


def main():
    """
    Function: creates Room, Hotel, Customer, Booking types objects, \
              makes list from those objects calls methods from respective classes.
    """

    room1 = Room('president', 4)
    room2 = Room('double', 10)
    room3 = Room('single', 12)
    room4 = Room('double lux', 6)
    room5 = Room('single lux', 9)
    rooms_list1 = [room1, room2,  room4, room5]
    rooms_list2 = [room1, room2, room3]
    rooms_list3 = [room2, room3, room4, room5]

    hotel1 = Hotel('Messier87', rooms_list1)
    hotel2 = Hotel('Andromeda', rooms_list2)
    hotel3 = Hotel('Halsey', rooms_list3)
    hotels_list1 = [hotel1, hotel3]
    hotels_list2 = [hotel3, hotel2]
    hotels_list3 = [hotel1, hotel3]

    customer1 = Customer(hotels_list1)
    customer2 = Customer(hotels_list2)
    customer3 = Customer(hotels_list3)
    customers_list = [customer1, customer2, customer3]

    customer1.reservation('Messier87', 'president', 2)
    customer1.checking_out('Messier87', 'president', 2)
    customer1.rate('Messier87', 4.6)
    print(f'Your reserved hotel\'s rating is:  {hotel1.get_rating()}')

    customer2.reservation('Andromeda', 'single', 4)
    customer2.checking_out('Andromeda', 'single', 4)
    customer2.rate('Andromeda', 4.8)
    print(f'Your reserved hotel\'s rating is:  {hotel2.get_rating()}')

    booking = Booking(customers_list)
    booking.get_customer_data_to_csv()


if __name__ == "__main__":
    main()
