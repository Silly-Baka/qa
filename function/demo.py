import chardet
import pandas as pd
import random
import ipaddress

# 生成随机 IP 地址
def generate_random_ip():
    return str(ipaddress.IPv4Address(random.randint(0, (1 << 32) - 1)))

# 生成随机交易金额
def generate_random_amount():
    return round(random.uniform(1.0, 1000.0), 2)

if __name__ == '__main__':
    # with open('C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\交易流水表.csv', 'rb') as f:
    #     result = chardet.detect(f.read())  # 读取一定量的数据进行编码检测
    #     print(result)
    # # 读取现有的 CSV 文件
    input_file = "C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\交易流水表.csv"
    df = pd.read_csv(input_file, encoding='GB2312')

    # 生成随机数据并添加到 DataFrame 中
    # 定义存储IP地址的数组
    ip_list = []
    # 读取文件
    file_path = "所有ip.txt"  # 替换为你的文件路径
    flen = 0
    with open(file_path, 'r') as file:
        # 遍历文件的每一行
        for line in file:
            # 去除行末的换行符并添加到列表
            ip_list.append(line.strip())
            flen+=1

    len = len(df)
    input_ip = []
    for i in range(len):
        input_ip.append(ip_list[i % flen])

    df['交易金额'] = [generate_random_amount() for _ in range(len)]
    df['IP地址'] = input_ip

    # 写回到 CSV 文件
    df.to_csv(input_file, index=False, encoding='GB2312')

    print(f"随机数据已添加并写回到 {input_file}")


