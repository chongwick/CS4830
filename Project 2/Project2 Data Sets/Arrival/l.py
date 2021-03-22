data = ''

with open('arrival_data.txt') as f:
    data = f.read()
f.close()

data_set = data.split('\n\n')
for i in data_set:
    tmp = i.split('\n')
    for j in range(len(tmp)):
        if j != len(tmp) - 1:
            print(round(float(tmp[j+1]),9)-round(float(tmp[j]),9))
