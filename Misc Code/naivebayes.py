
from collections import Counter
import numpy as np

classes = {0: 'Yes', 1: 'No'}
data = [('Sunny', 'Yes'), ('Overcast', 'Yes'), ('Rainy', 'Yes'), ('Sunny', 'Yes'), ('Sunny', 'No'),('Overcast', 'Yes'), ('Rainy', 'No'), ('Rainy', 'No'), ('Sunny', 'Yes'), ('Rainy', 'Yes'),('Sunny', 'No'), ('Overcast', 'Yes'), ('Overcast', 'Yes'), ('Rainy', 'No')]

# get all values from list where the second value is 'Yes'
yes = [x[0] for x in data if x[1] == 'Yes']
no = [x[0] for x in data if x[1] == 'No']


# get counts of all values
yes_counts = Counter(yes)
no_counts = Counter(no)

# p(yes|sunny) = p(sunny|yes) * p(yes) / p(sunny)
p_yes = len(yes) / len(data)
p_no = len(no) / len(data)

# p(sunny|yes)
p_sunny_yes = yes_counts['Sunny'] / len(yes)
# p(sunny|no)
p_sunny_no = no_counts['Sunny'] / len(no)
p_sunny = (yes_counts['Sunny'] + no_counts['Sunny']) / len(data)
# p(sunny)
# p(yes|sunny)
p_yes_sunny = p_sunny_yes * p_yes / p_sunny
# p(no|sunny)
p_no_sunny = p_sunny_no * p_no / p_sunny

print(f'Are the players predicted to go out: {classes.get(np.argmax([p_yes_sunny, p_no_sunny]))}')

print('p(yes|sunny) =', p_yes_sunny)
print('p(no|sunny) =', p_no_sunny)

