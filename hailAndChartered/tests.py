# from django.test import TestCase
# Create your tests here.

import datetime

ts = '06:00'
t = datetime.datetime.strptime(ts, '%H:%M')
# print(t)

# n = datetime.datetime.now()

# print(n)

# nh = [str((t + datetime.timedelta(hours=h)).time())[1] for h in range(12)]

# print(f'{nh}點')

data=[f'action=ch2Date&chId=a&chdt=0928 {6+h:02d}' for h in range(12)]

print(data)