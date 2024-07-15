import pandas as pd
import json

print('读取数据中......')
df = pd.read_excel('./data.xlsx')
print('读取数据完成')




if __name__ == '__main__':
    entity_dict = {}

    col_name = ['name', 'hobby',  'hometown', 'live', 'person']

    A = df['name']
    B = df['hobby']
    # C = df['homemate']
    D = df['hometown']
    E = df['live']
    F = df['person']

    entity_list = [A, B, D, E, F]

    one = []

    for i in range(len(col_name)):
        for e in entity_list[i]:
            if e not in one:
                one.append(e)
            entity_dict.update({e: col_name[i]})

    print(one)

    with open('./entity.txt', 'w', encoding='utf-8') as file:
        json.dump(entity_dict, file, ensure_ascii=False)

    with open('segment_word.txt', 'w', encoding='utf-8') as f:
        for o in one:
            f.write(str(o) + '\n')
            f.write('\n')
    f.close()
