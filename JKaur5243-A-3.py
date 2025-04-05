# Constants
HST_RATE = 0.13
STUDENT_DISCOUNT_RATE = 0.10
DELIVERY_CHARGE = 5.00
FREE_DELIVERY_THRESHOLD = 30.00
TIP_OPTIONS = [10, 15, 20]  # Tip options in percentage
MENU = {
    1: {"name": "Cheesy Pizza", "price": 12.99},
    2: {"name": "Spicy Wings", "price": 13.99},
    3: {"name": "Veggie Burger", "price": 11.99},
    4: {"name": "Caesar Salad", "price": 9.99},
    5: {"name": "Pasta Primavera", "price": 14.99},
    6: {"name": "Fish Tacos", "price": 15.99}
}

def get_input(prompt, valid_type=str, valid_options=None):
    """General function for input validation."""
    while True:
        try:
            value = valid_type(input(prompt))
            if valid_options and value not in valid_options:
                print(f"Invalid choice. Options: {valid_options}")
                
            elif valid_type == float and value <= 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {valid_type.__name__}.")

def collect_customer_info():
    """Collects and returns customer information."""
    return {field: get_input(f"Enter {field.replace('_', ' ')}: ") for field in ['first_name', 'last_name', 'address', 'city', 'phone_number']}

def print_receipt(order, customer_info, total_cost, student_discount, hst, delivery_charge, tip):
    """Prints receipt to screen and file."""
    total_due = total_cost + hst + delivery_charge + tip
    receipt = f"\nThank you for ordering, {customer_info['first_name']}!\n\nOrder Details:\n"
    
    for details in order.values():
        receipt += f"{details['name']:15} x{details['quantity']} @ ${details['price']:.2f} = ${details['price'] * details['quantity']:.2f}\n"
    
    if student_discount: 
        receipt += f"Student Discount: -${student_discount:.2f}\n"
    if delivery_charge: 
        receipt += f"Delivery Charge: ${delivery_charge:.2f}\n"
    
    receipt += f"Subtotal: ${total_cost:.2f}\nTax: ${hst:.2f}\nTip: ${tip:.2f}\nTotal: ${total_due:.2f}\n"
    
    print(receipt)  # Print to screen
    with open("receipt.txt", "w") as file:  # Save to file
        file.write(receipt)

def main():
    print("Welcome to Arnold's Amazing Eats!")
    customer_info = collect_customer_info()
    
    order = {}
    total_cost = 0
    is_student = get_input("Are you a student? (y/n): ", str, ['y', 'n']) == 'y'

    # Meal selection loop
    while True:
        print("\nMenu options:")
        for key, meal in MENU.items():
            print(f"{key}) {meal['name']} - ${meal['price']:.2f}")
        
        meal_choice = get_input("Choose your meal (1-6): ", int, MENU.keys())
        meal = MENU[meal_choice]
        quantity = get_input(f"How many {meal['name']} would you like? ", float)

        # Add to order
        order.setdefault(meal['name'], {"name": meal['name'], "price": meal['price'], "quantity": 0})
        order[meal['name']]['quantity'] += quantity
        total_cost += meal['price'] * quantity
        
        if get_input("Add another item? (y/n): ", str, ['y', 'n']) == 'n':
            break
    
    # Calculate discounts and charges
    student_discount = total_cost * STUDENT_DISCOUNT_RATE if is_student else 0
    total_cost -= student_discount
    hst = total_cost * HST_RATE
    delivery_charge = DELIVERY_CHARGE if total_cost < FREE_DELIVERY_THRESHOLD else 0
    tip = (get_input("Enter tip percentage (10, 15, 20): ", int, TIP_OPTIONS) / 100) * total_cost if delivery_charge else 0

    # Print the receipt
    print_receipt(order, customer_info, total_cost, student_discount, hst, delivery_charge, tip)

if __name__ == "__main__":
    main()
    