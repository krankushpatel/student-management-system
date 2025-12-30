x = [1]
x.append("AB")
x.extend(["CD"])
x.extend("EF")

print(x)


y = []
y.append(["A", "B"])
y.extend(["C", "D"])
y.extend("EF")

print(y)

z = (10,)  # this is single tuple 
a = (9)  # this is treated as integer not tuple  because tuple is deceided by comma not parenthesis 


d = {"a": 1, "b": 2, "c": 3}
x = d.pop("b")
print(x)   # 2    (returned value)
print(d)   # {"a": 1, "c": 3}


e = {"name": "Ankush", "age": 21}
name_value = e.get("name")   # output is Ankush
print(f"name = {name_value}")   # Output: name = Ankush