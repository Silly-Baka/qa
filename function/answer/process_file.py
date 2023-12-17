import pandas as pd
import json

print('读取数据中......')
df = pd.read_excel('./政策查询.xls')
print('读取数据完成')




if __name__ == '__main__':
    entity_dict = {}

    col_name = ['ZCMC', 'FWJG', 'GWZL', 'ZCJB', 'ZCFL', 'ZTC', 'GJC', 'ZCZX_LXR', 'ZCZX_LXDH', 'ZCGS', 'ZCZW', 'SBTJ',
                'SBFS', 'SBDZ', 'SBLC']

    A = df['ZCMC']
    B = df['FWJG']
    C = df['GWZL']
    D = df['ZCJB']
    E = df['ZCFL']
    F = df['ZTC']
    G = df['GJC']
    H = df['ZCZX_LXR']
    I = df['ZCZX_LXDH']
    J = df['ZCGS']
    K = df['ZCZW']
    L = df['SBTJ']
    M = df['SBFS']
    N = df['SBDZ']
    O = df['SBLC']

    entity_list = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O]

    one = []

    for i in range(len(col_name)):
        for e in entity_list[i]:
            if e not in one:
                one.append(e)
            entity_dict.update({e: col_name[i]})

    print(one)

    with open('./entity.txt', 'w', encoding='utf-8') as file:
        json.dump(entity_dict, file, ensure_ascii=False)

    with open('./1.txt', 'w', encoding='utf-8') as f:
        for o in one:
            f.write(str(o) + '\n')
            f.write('\n')
    f.close()
