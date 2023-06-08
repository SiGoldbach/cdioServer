import time
import numpy as np

import LiveVideoFeed

p1 = LiveVideoFeed.get_image(1)
time.sleep(1)
p2 = LiveVideoFeed.get_image(2)

print(type(p1))
print(type(p2))
equals = np.array_equal(p1, p2)
print(equals)
