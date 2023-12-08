import os
import time
import datetime
import sys
def downlaod(input_1, input_2):
    print('数据下载开始运行')
    time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    t = datetime.datetime.now().strftime('%Y%m%d%H') + '0000'
    str1 = '[{}]:流程：数据下载\n'.format(time_)
    str1 += '[{}]:开始运行\n'.format(time_)
    t1 = time.time()
    try:
        os.system('sh /space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/auto/download.sh {} {}'.format(input_1, input_2))
    except Exception as e:
        str1 += '出现的问题是：' + str(e) + '\n'
    do = time.time()
    str1 += '[{}]:程序运行结束，耗时为{}\n'.format(time_, do - t1)

    with open(r'/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/runLogs/test.txt','a') as f:
        f.write(str1)
    return t
    

def rain_qc(input_1, input_2, t):
    print('降水质控开始运行')
    time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    str1 = '[{}]:流程：降水质控\n'.format(time_)
    str1 += '[{}]:开始运行\n'.format(time_)
    t1 = time.time()
    try:
        os.system('echo -e "exit" | sh /space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/auto/qc.sh {} {} {}'.format(input_1, input_2, t))
    except Exception as e:
        str1 += '出现的问题是：' + str(e) + '\n'
    do = time.time()
    str1 += '[{}]:程序运行结束，耗时为{}\n'.format(time_, do - t1)

    with open(r'/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/runLogs/test.txt','a') as f:
        f.write(str1)

def update(input_1, input_2, t):
    print('数据库质控码更新')
    time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    str1 = '[{}]:流程：数据库质控码更新\n'.format(time_)
    str1 += '[{}]:开始运行\n'.format(time_)
    t1 = time.time()
    try:
        os.system('echo -e "exit" | sh /space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/auto/update.sh {} {} {}'.format(input_1, input_2, t))
    except Exception as e:
        str1 += '出现的问题是：' + str(e) + '\n'
    do = time.time()
    str1 += '[{}]:程序运行结束，耗时为{}\n'.format(time_, do - t1)

    with open(r'/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/runLogs/test.txt','a') as f:
        f.write(str1)

def draw(input_1, input_2, t):
    print('绘图流程开始运行')
    time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    str1 = '[{}]:流程：绘图流程开始运行\n'.format(time_)
    str1 += '[{}]:开始运行\n'.format(time_)
    t1 = time.time()
    try:
        os.system('echo -e "exit" | sh /space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/auto/draw.sh {} {} {}'.format(input_1, input_2, t))
    except Exception as e:
        str1 += '出现的问题是：' + str(e) + '\n'
    do = time.time()
    str1 += '[{}]:程序运行结束，耗时为{}\n'.format(time_, do - t1)
    with open(r'/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/runLogs/test.txt','a') as f:
        f.write(str1)


if __name__ == '__main__':
    input_1 = sys.argv[1]
    input_2 = sys.argv[2]
    t1 = time.time()
    t = downlaod(input_1, input_2)
    rain_qc(input_1, input_2, t)
    time.sleep(15)
    update(input_1, input_2, t)
    draw(input_1, input_2, t)
    do = time.time()
    str1 = '整个流程运行结束，总耗时为{}\n'.format( do - t1)
    with open(r'/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/runLogs/test.txt','a') as f:
        f.write(str1)

