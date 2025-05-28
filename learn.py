# #region types
# list = ["Red", "Green", "Blue"]
# print(type(list))

# tuple = ("Red", "Green", "Blue")
# print(type(tuple))

# set = {"Red", "Green", "Blue"}
# print(type(set))

# dict = {"Red": 1, "Green": 2, "Blue": 3}
# print(type(dict))

# frozenset = frozenset({"Red", "Green", "Blue"})
# print(type(frozenset))

# # # endregion

# # #region numbers
# x, y, z = 1, 1.5, 1 + 2j
# print(type(x))
# print(type(y))
# print(type(z))
# print(type(x + y))
# print("x + y + z", x + y + z)

# print(type(int(y)))
# print(type(float(x)))
# print(type(float(z.real)))
# print(float(z.real))
# print(type(z.imag))
# print(complex(x))


# print(isinstance(x, int))
# print(isinstance(y, float))
# print(isinstance(z, complex))
# print(isinstance(x, (float)))
# # endregion numbers

# #region strings
s = "Hello, World!"
print("upper",s.upper())
print("lower",s.lower())
print("title",s.title())
print("String split by comma", s.split(","))
print("String slice", s[2:5])
print("String length", len(s))
print("String negative index slice", s[-5:-2])
print("String replace", s.replace("World", "Everyone"))
print("String concatenate", f"{s} How are you?")
print("String find", s.find("World"))

print("String count", s.count("o"))
print("String starts with", s.startswith("Hello"))
print("String ends with", s.endswith("!"))

# endregion strings
def print_items():
    pass