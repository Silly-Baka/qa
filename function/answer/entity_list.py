import json

import pandas as pd

def add_dict(d1,d2,d3,d4):
    result = d1.copy()
    result.update(d2)
    result.update(d3)
    result.update(d4)
    return result


def file_process():      # pe文件名，pb文件名，公司名
    # 处理pe文件，把pe和时间数据写入新文件
    df_fund =pd.read_csv('all_data/fund.csv', sep=',')
    data_fund_name = df_fund['name']
    data_fund_type = df_fund[':LABEL']
    dict1 = dict(zip(data_fund_name, data_fund_type))

    df_company = pd.read_csv('all_data/company.csv', sep=',')
    data_company_name = df_company['name']
    data_company_type = df_company[':LABEL']
    dict2 = dict(zip(data_company_name, data_company_type))

    df_index = pd.read_csv('all_data/index.csv', sep=',')
    data_index_name = df_index['name']
    data_index_type = df_index[':LABEL']
    dict3 = dict(zip(data_index_name, data_index_type))

    df_manage = pd.read_csv('all_data/manage.csv', sep=',')
    data_manage_name = df_manage['name']
    data_manage_type = df_manage[':LABEL']
    dict4 = dict(zip(data_manage_name, data_manage_type))
    dict_all = add_dict(dict1,dict2,dict3,dict4)
    js = json.dumps(dict_all, ensure_ascii=False)

    f = open('all_data/entity.txt', "a")
    f.write(js)
    f.close()


    # df_pe[['时间', 'PE-TTM市值加权']].to_csv('data/new/{}.csv'.format(file_comp), sep=',', header=True,index=False)
    #
    # # 处理pb文件，读入新文件，再把pb数据写入
    # df = pd.read_csv('data/new/{}.csv'.format(file_comp), header=0, sep=',')
    # df_pb = pd.read_csv('data/process/{}'.format(file_pb), header=0, sep=',')
    # data1 = df_pb['PB市值加权']
    # df['pb'] = data1
    # df.rename(columns={'PE-TTM市值加权': 'pe'}, inplace=True)
    # df.sort_values(by='时间', axis=0, ascending=True, inplace=True, na_position='last')
    # df.drop([len(df) - 1], inplace=True)
    # df.to_csv(r"data/new/{}.csv".format(file_comp), index=False)


if __name__ == "__main__":
    file_process()