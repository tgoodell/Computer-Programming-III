import difflib

with open("fresher.txt") as f1:
    f1_text = f1.read()
with open("fresh.txt") as f2:
    f2_text = f2.read()

# Find and print the diff:
for line in difflib.unified_diff(f1_text, f2_text):
    print(line)

# FLAG{EZMoney}