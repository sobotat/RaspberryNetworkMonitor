import os, shutil

file = open('output.log', 'rt')
data = file.readlines()
file.close()

try:
    shutil.rmtree('out')
except:
    pass
try:
    os.mkdir('out')
except:
    pass

space = False

data.insert(0, '')

outBuffer = []
outDate = ''

def writeBuffer():
    global outBuffer, outDate
    filePath = f'out/network-{outDate}.csv'
    fileExists = os.path.exists(f'out/network-{outDate}.csv')

    if not fileExists:
        file = open(filePath, 'wt')
        file.write('Time;Upload;Download\n')
    else:
        file = open(filePath, 'at')

    file.writelines(outBuffer)
    print(f'Written [{len(outBuffer)}] lines - {outDate}')
    outBuffer = []
    outDate = ''
    file.close()  

for line in data:
    if 'Us' not in line or 'Ds' not in line:        
        if not space and outDate != '':        
            writeBuffer()
        space = True
        continue

    space = False

    date = line.split(' ')[0]
    time = line.split(' ')[1]
    dateTime = f'{date} {time}'

    lineData = line.split('>')[1]
    splited = lineData.split(' ')
    upload = float(splited[1].split('[')[1])
    download = float(splited[3].split('[')[1])
        
    if outDate == '':
        outDate = date
    speedsStr = f'{upload};{download}'.replace('.', ',')
    outBuffer.append(f'{time};{speedsStr}\n')

writeBuffer()
print('Done')