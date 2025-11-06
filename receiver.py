#%%
# Como tener esta file asociada a mas de un codigo
from controller import Arduino
from cmd_commands import clear_buf, nsteps, mode

#%%
ard = Arduino(port="COM13")
#%%

nsteps(ard, 3)
mode(ard, 2)
clear_buf(ard,verbose=True) 


#%%
while True:
    data = ard.get_data()
    if data is None:
        pass
    else:
        print(data)
#%%
ard.close()