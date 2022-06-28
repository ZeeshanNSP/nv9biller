from nv9biller import Biller

biller = Biller("COM1")
t = biller.stacker()
print(biller.counters)
print(biller.counters_reset())
print(biller.counters)