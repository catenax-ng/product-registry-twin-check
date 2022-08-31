

import datetime

t1 = datetime.datetime.now()
t2 = t1 + datetime.timedelta(seconds=-100)

print()



print(f"t1: {t1}")

print(f"t2: {t2}")

print(f"{t1<t2}")