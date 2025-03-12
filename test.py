# group.set_g_pub('place_dict',{random.randint(100000, 999999):'電力',random.randint(100000, 999999):'維生',random.randint(100000, 999999):'任務'},'group',pri_get('g_group'))
import random

place_dict={random.randint(100000, 999999):'電力',random.randint(100000, 999999):'維生',random.randint(100000, 999999):'任務'}
print(place_dict)
target_value='電力'

key = next((k for k, v in place_dict.items() if v == target_value), None)

print(key)  # ['BBB']