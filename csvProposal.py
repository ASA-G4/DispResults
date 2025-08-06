import pandas as pd
import random 
from datetime import timedelta,datetime
timeStampRef='Time'
travelTimeRef='Real-time vehicle counting'
ts=datetime(2025,7,22,0,0,0)
data_list=[ {timeStampRef:ts+timedelta(minutes=minute),travelTimeRef:random.randint(1,10)} for minute in range(720*8) ]
individualTT=pd.DataFrame(data_list)
individualTT[travelTimeRef]=individualTT[travelTimeRef].cumsum()
individualTT.to_csv('Bota.csv',index=False)


'''[{'group': np.int64(20), 'readers': array([36]), 'data': [...]},
 {'group': np.int64(21), 'readers': array([37]), 'data': [...]},
 {'group': np.int64(22), 'readers': array([38]), 'data': [...]},
 {'group': np.int64(23), 'readers': array([39]), 'data': [...]},
 {'group': np.int64(24), 'readers': array([40]), 'data': [...]},
 {'group': np.int64(25), 'readers': array([41, 42, 43]), 'data': [...]}, 
 {'group': np.int64(26), 'readers': array([44]), 'data': [...]}]'''
