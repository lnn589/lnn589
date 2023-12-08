import os
import sys
import glob
import datetime
import shutil
from config import all_file_path, out_path
from QC_ei import deal_ei

def download_batch(time_n, day, num):
    time_s = time_n - datetime.timedelta(days=day)
    for i in range(num):
        time_n_i = time_s + datetime.timedelta(hours=5*(i+1) + i)
        # time_n_C_i = time_n_i.strftime('%Y%m%d%H') + '0000'
        input_save = os.path.join(out_path, 'output', time_n_i.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        print(input_save)
        NAS_download = all_file_path + 'download/output/' +  time_n_i.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")
        if not os.path.exists(NAS_download):
            os.makedirs(NAS_download)
        for f in glob.glob(input_save + "*.TXT"):
            f_n = os.path.split(f)[1]
            shutil.move(f, NAS_download+f_n)

def select_time(pros, time_n, t):
    if pros == 'appoint':
        time_n = datetime.datetime.strptime(time_n, "%Y%m%d%H%M%S")
        time_nc = time_n + datetime.timedelta(hours=1)
        download_batch(time_nc, 1, 4)
    elif pros == 'offsetDay':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(days=abs(int(time_n)))
        time_n = datetime.datetime.strftime(time_n, "%Y%m%d")
        time_n = datetime.datetime.strptime(time_n, "%Y%m%d")
        # time_nc = time_n + datetime.timedelta(hours=24)
        print(time_n)
        download_batch(time_n, 4, 20)
    elif pros == 'offsetHour':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(hours=abs(int(time_n)))
        time_nc = time_n + datetime.timedelta(hours=1)
        download_batch(time_nc, 1, 4)

    input_folder = '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/input/'+ time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")
    NAS_input = all_file_path + 'QC/input/' + time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")
    if not os.path.exists(NAS_input):
        os.makedirs(NAS_input)
    QC_inputfile_names = []
    for f in glob.glob(input_folder + "*.TXT"):
        f_n = os.path.split(f)[1]
        QC_inputfile_names.append(f_n)
        shutil.move(f, NAS_input+f_n)
    output_folder = '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/output/'+ time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")
    NAS_output = all_file_path + 'QC/output/' + time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")
    if not os.path.exists(NAS_output):
        os.makedirs(NAS_output)
    QC_outputfile_names = []
    for f_o in glob.glob(output_folder + "*.TXT"):
        f_n = os.path.split(f_o)[1]
        QC_outputfile_names.append(f_n)
        shutil.move(f_o, NAS_output + f_n)
    if len(QC_inputfile_names) > len(QC_outputfile_names):
        for f_n in QC_inputfile_names:
            if f_n not in QC_outputfile_names:
                shutil.move(NAS_input+f_n, input_folder+f_n)
        deal_ei(NAS_output, time_nc.strftime("%Y%m%d%H"), len(QC_inputfile_names), len(QC_outputfile_names))
        
    
if __name__ == '__main__':
    select_time(sys.argv[1], sys.argv[2], sys.argv[3])