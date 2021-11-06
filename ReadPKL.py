'''Load dictionary from .pkl file without losing original variable type '''
import pickle
def ReadPKL(fileName, mode):
    if 'pkl' not in fileName:
        fileName = fileName + '.pkl'
    File = open(fileName, mode)
    DicList = []
    while True:
        try:
            DicList.append(pickle.load(File))
        except EOFError:
            break
    return DicList

# os.chdir('RawTimetableData')
# List = ReadPKL('TimetableDic.pkl', 'rb')
