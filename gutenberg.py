import difflib

with open("64412-0-diff.txt") as f1:
    f1_text = f1.read()
with open("64412-0.txt") as f2:
    f2_text = f2.read()

# Find and print the diff:
for line in difflib.unified_diff(f1_text, f2_text):
    print(line)

# FLAG{EZMoney}