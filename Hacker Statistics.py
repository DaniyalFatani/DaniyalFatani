#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
#set the seed so that results are reproducible
np.random.seed(123)
all_walks=[]
for i in range(1000) : #playing game for 1000 times
    random_walk=[0]
    for x in range(100): #one dice throw
        step = random_walk[-1]
        dice = np.random.randint(1,7)
        if dice <= 2:
            step = max(0,step-1) #its done as we cant go below 0
        elif dice <= 5:
            step = step+1
        else:
            step = step + np.random.randint(1,7)
        if np.random.rand() <0.001:
            step = 0
        random_walk.append(step)
    all_walks.append(random_walk)            


np_aw=np.array(all_walks)
np_aw_t=np.transpose(np_aw)
print(np.random.randint(1,7))
print(all_walks)

ends = np_aw_t[-1,:]
import matplotlib.pyplot as plt

plt.hist(ends)
plt.show()
print(np.mean(ends>=60))


# In[ ]:




