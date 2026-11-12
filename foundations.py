"""
Period 0 warm-up: the new Python you need for the canteen app.

You already know variables, if, loops, lists and 2D lists. This file adds
four new ideas: functions, tuples, dictionaries, and lists of dictionaries.

Run it:   python foundations.py      (on a Mac: python3 foundations.py)

Each TODO is a small task. Do one, run the file, check the output, then move on.
"""

# --------------------------------------------------------------------------
# 1. Functions
# A function is a named block of code. It takes inputs (parameters) and
# gives back an answer with return. You run it by "calling" it by name.
# --------------------------------------------------------------------------
def add_gst(price):
    return round(price * 1.09, 2)


print("1a.", add_gst(10))          # 10.9

# TODO 1b: write a function called discount that takes a price and returns
# the price with 20% off. Then remove the # from the print below.
# print("1b.", discount(5))        # should print 4.0


# --------------------------------------------------------------------------
# 2. Tuples
# A tuple is like a list in round brackets, but it cannot be changed.
# --------------------------------------------------------------------------
point = (3, 5)
print("2a.", point[0], point[1])   # 3 5

one = ("aisha",)                   # a tuple with ONE item needs a comma
print("2b.", type(one), len(one))  # <class 'tuple'> 1

# TODO 2c: print type(("aisha")) with NO comma. What changes, and why?


# --------------------------------------------------------------------------
# 3. Dictionaries
# A dictionary stores values under names (keys) instead of position numbers.
# --------------------------------------------------------------------------
item = {"name": "Nasi lemak", "price": 3.50}
print("3a.", item["name"], item["price"])   # Nasi lemak 3.5

# TODO 3b: add a key "id" with the value 1 to item, then print item.


# --------------------------------------------------------------------------
# 4. From a 2D list to a list of dictionaries
# Both hold the same menu. The dictionary version uses names, not numbers.
# A database table is a list of rows like this, and each row is like a
# dictionary: row["name"], row["price"].
# --------------------------------------------------------------------------
menu_2d = [["Nasi lemak", 3.50], ["Laksa", 4.00], ["Beef pie", 3.20]]
print("4a.", menu_2d[1][0], menu_2d[1][1])        # Laksa 4.0

menu = [
    {"name": "Nasi lemak", "price": 3.50},
    {"name": "Laksa", "price": 4.00},
    {"name": "Beef pie", "price": 3.20},
]
print("4b.", menu[1]["name"], menu[1]["price"])   # Laksa 4.0


# --------------------------------------------------------------------------
# 5. Loop over the rows
# --------------------------------------------------------------------------
for row in menu:
    print("5a.", row["name"], row["price"])

# TODO 5b: work out the total price of the whole menu (use a loop, or sum),
# and print it. It should be 10.7.


# --------------------------------------------------------------------------
# 6. Building text with +
# You will build a database question (a query) out of pieces of text.
# --------------------------------------------------------------------------
name = "aisha"
message = "Hello, " + name + "!"
print("6a.", message)                             # Hello, aisha!

# TODO 6b: use + and the variable name to build and print exactly this text:
#     WHERE username = 'aisha'
# Hint: the single quotes go inside the double-quoted pieces.
