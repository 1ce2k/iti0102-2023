"""Spa."""
import random

# Exercise 1: Generate Spa Menu Prices
def generate_menu_prices(services: list) -> list:
    """
    Generate random prices for spa services.

    Prices have to be between 30 and 150.
    :param services: list of spa service names
    :return: list of service prices
    """
    return [round(random.uniform(30, 150), 2) for service in services]


# Exercise 2: Create Spa Appointment Slots
def create_appointment_slots(hours: list, duration: int, date: str) -> list:
    """
    Generate available appointment slots for a specific date.

    :param hours: list of spa working hours
    :param duration: duration of each appointment
    :param date: appointment date
    :return: list of available slots
    """
    pass


# Exercise 3: Discounted Spa Packages
def generate_package_names(adjectives: list) -> list:
    """
    Generate spa package names using given adjectives.

    :param adjectives: list of adjectives to use in package names
    :return: list of spa package names
    """
    pass


# Exercise 4: Customer Feedback
def filter_positive_feedback(feedback_data: list) -> list:
    """
    Filter positive feedback comments (rated 3 or better).

    :param feedback_data: list of feedback comments with grades (e.g., ["Excellent", 5], ["Bad", 1])
    :return: list of positive feedback comments
    """
    pass


# Exercise 5: Spa Employee Schedules
def generate_employee_schedules(employees: list, working_hours: list) -> list:
    """
    Generate schedules for spa employees.

    Each employee should have 5 working hours in his schedule.
    :param employees: list of employee names
    :param working_hours: list of working hours for each day
    :return: list of employee schedules
    """
    pass


# Exercise 6: Spa Product Inventory
def generate_product_inventory(products: list, initial_quantity: int) -> list:
    """
    Generate spa product names and quantities in stock.

    You have to update initial quantity of the product by using calculate_product_quantity method.

    :param products: list of product names
    :param initial_quantity: initial quantity in stock
    :return: list of product names and quantities
    """
    pass


def calculate_product_quantity(initial_quantity: int, product: str) -> int:
    """
    Calculate the updated quantity of a product.

    Do not change this method!

    :param initial_quantity: initial quantity of the product
    :return: updated quantity
    """
    updated_quantity = len(product) * initial_quantity
    return updated_quantity


# Exercise 7: Spa Product Pairing
def generate_product_scents(product_types: list, scents: list) -> list:
    """
    Generate pairings of spa product types and scents.

    :param product_types: list of spa product types (e.g., "Lotion", "Shampoo")
    :param scents: list of scents (e.g., "Lavender", "Eucalyptus")
    :return: list of paired product and scent combinations
    """
    pass


# Exercise 8: Identify VIP Customers
def identify_vip_customers(customer_names: list) -> list:
    """
    Identify VIP customers and replace their names with "vip".

    Customer is "vip" if his name starts with uppercase.

    :param customer_names: list of customer names
    :return: list of customer names with VIPs marked as "vip"
    """
    pass


# Exercise 9: Spa Service Availability Checker
def check_service_availability(service_schedules: dict, date: str) -> list:
    """
    Check the availability of spa services for a given date.

    :param service_schedules: list of service schedules with dates
    :param date: date for which availability is checked
    :return: list of available spa services
    """
    pass


if __name__ == '__main__':
    print("Exercise 1: Generate Spa Menu Prices")
    services = ["Massage", "Facial", "Manicure", "Pedicure", "Sauna"]
    prices = generate_menu_prices(services)
    print(prices)  # prices can differ, but it should look like this
    # [['Massage', 95.66], ['Facial', 62.72], ['Manicure', 97.96], ['Pedicure', 135.33], ['Sauna', 69.99]]

    print("\nExercise 2: Create Spa Appointment Slots")
    hours = [10, 11, 12, 14, 15, 16]
    duration = 2
    date = "2023-09-20"
    slots = create_appointment_slots(hours, duration, date)
    print(slots)  # ['2023-09-20 10:00 - 12:00', '2023-09-20 11:00 - 13:00', '2023-09-20 12:00 - 14:00',
    # '2023-09-20 14:00 - 16:00', '2023-09-20 15:00 - 17:00', '2023-09-20 16:00 - 18:00']

    print("\nExercise 3: Discounted Spa Packages")
    adjectives = ["Relaxing", "Pampering", "Ultimate", "Luxury", "Tranquil"]
    packages = generate_package_names(adjectives)
    print(packages)  # ['Relaxing Spa Package', 'Pampering Spa Package', 'Ultimate Spa Package',
    # 'Luxury Spa Package', 'Tranquil Spa Package']

    print("\nExercise 4: Customer Feedback")
    feedback_data = [["Good", 4], ["Poor", 2], ["Excellent", 5], ["Bad", 1], ["Average", 3]]
    positive_feedback = filter_positive_feedback(feedback_data)
    print(positive_feedback)  # ['Good', 'Excellent', 'Average']

    print("\nExercise 5: Spa Employee Schedules")
    employees = ["Therapist A", "Therapist B", "Receptionist"]
    working_hours = ["10:00 AM - 2:00 PM", "2:00 PM - 6:00 PM", "10:00 AM - 6:00 PM"]
    schedules = generate_employee_schedules(employees, working_hours)
    print(schedules)
    # [['Therapist A', '10:00 AM - 6:00 PM', '2:00 PM - 6:00 PM', '2:00 PM - 6:00 PM', '10:00 AM - 6:00 PM',
    # '10:00 AM - 6:00 PM'], ['Therapist B', '2:00 PM - 6:00 PM', '2:00 PM - 6:00 PM', '10:00 AM - 2:00 PM',
    # '2:00 PM - 6:00 PM', '10:00 AM - 2:00 PM'], ['Receptionist', '10:00 AM - 2:00 PM', '2:00 PM - 6:00 PM',
    # '2:00 PM - 6:00 PM', '10:00 AM - 6:00 PM', '10:00 AM - 6:00 PM']]

    print("\nExercise 6: Spa Product Inventory")
    products = ["Lotion", "Shampoo", "Candles", "Robes"]
    initial_quantity = 1
    product_inventory = generate_product_inventory(products, initial_quantity)
    print(product_inventory)  # [['Lotion', 6], ['Shampoo', 7], ['Candles', 7], ['Robes', 5]]

    print("\nExercise 7: Spa Product Pairing")
    product_types = ["Lotion", "Shampoo", "Candles"]
    scents = ["Lavender", "Eucalyptus", "Citrus"]

    product_scents_pairings = generate_product_scents(product_types, scents)
    print(product_scents_pairings)
    # [['Lotion', 'Lavender'], ['Lotion', 'Eucalyptus'], ['Lotion', 'Citrus'], ['Shampoo', 'Lavender'],
    # ['Shampoo', 'Eucalyptus'], ['Shampoo', 'Citrus'], ['Candles', 'Lavender'], ['Candles', 'Eucalyptus'],
    # ['Candles', 'Citrus']]

    print("\nExercise 8: Identify VIP Customers")
    customer_names = ["Alice", "bob", "Charlie", "David", "eve"]
    vip_customer_names = identify_vip_customers(customer_names)
    print(vip_customer_names)  # ['vip', 'bob', 'vip', 'vip', 'eve']

    print("\nExercise 9: Spa Service Availability Checker")
    service_schedules = {
        "Massage": ["2023-09-15", "2023-09-16"],
        "Facial": ["2023-09-15"],
        "Manicure": ["2023-09-14", "2023-10-15"],
        "Pedicure": [],
        "Sauna": ["2023-09-11", "2023-09-15"]
    }
    date = "2023-09-15"

    available_services = check_service_availability(service_schedules, date)
    print(f"Available services at {date}: {available_services}")
    # Available services at 2023-09-15: ['Massage', 'Facial', 'Sauna']
