import os
import shutil
import subprocess
import sys
from tqdm import tqdm
import time

def file_copy(source,target):
    try:
        shutil.copy(source, target)
    except IOError as e:
        print("\n不能复制此文件. %s" % e)
    except:
        print("\n未知错误:", sys.exc_info())

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("\n文件夹创建成功\n")
    else:
        print("\n此文件夹已经存在\n")

"""传入TXT的路径进行打开操作"""
def open_txt_file(TXT_PATH,FLAC_PATH_DIR,FLAC_PATH_SAVE_DIR):
    print("正在对["+TXT_PATH+"]文件进行操作")
    TXT_FILE  = open(TXT_PATH,encoding='utf-8')
    i = 1 #记录行数
    while True:
        print("正在对["+TXT_PATH+"]的第"+str(i)+"行进行处理")
        TXT_LINE = TXT_FILE.readline()
        if TXT_LINE:  ##获取到的行数
            WAV_NAME_EXPAND  = TXT_LINE.split('|')[0] ##获取WAV文件的名称包含扩展名 vo_adv_0000011_1.wav
            WAV_NAME = WAV_NAME_EXPAND.split('.')[0]  ##获取文件名
            FLAC_PATH = FLAC_PATH_DIR + "\\" + WAV_NAME +".flac"
            FLAC_PATH_T = FLAC_PATH_DIR+"\\"+"t"+"\\"+WAV_NAME +".flac"
            if os.path.exists(FLAC_PATH): ##如果flac文件存在
                file_copy(source=FLAC_PATH,target=FLAC_PATH_SAVE_DIR) #复制命令
            elif os.path.exists(FLAC_PATH_T):
                file_copy(source=FLAC_PATH_T, target=FLAC_PATH_SAVE_DIR)  # 复制命令
        else:
            break
        i = i +1
    TXT_FILE.close()

def select_flac_from_txt(TXT_PATH_DIR,FLAC_PATH_DIR,FLAC_PATH_SAVE_DIR):
    """首先遍历所有的TXT文件"""
    TXT_FILES = os.listdir(TXT_PATH_DIR)
    FILE_NUM = len(TXT_FILES)
    for TXT_FILE in tqdm(TXT_FILES,desc="当前进度为："):
        TXT_FILE_PATH = TXT_PATH_DIR+ "\\" + TXT_FILE  #拼接的文件路径
        """传入路径,打开TXT文件"""
        TXT_PATH_SAVE_DIR_NAME = FLAC_PATH_SAVE_DIR+"\\"+TXT_FILE.split(".")[0]
        mkdir(TXT_PATH_SAVE_DIR_NAME)
        open_txt_file(TXT_PATH=TXT_FILE_PATH,FLAC_PATH_DIR=FLAC_PATH_DIR,FLAC_PATH_SAVE_DIR=TXT_PATH_SAVE_DIR_NAME)



def reform_fre(input_path, output_path,SPEAKER_ID):

    i = 1

    for file in os.listdir(input_path):

        file1 = input_path + '\\' + file

        # file2 = output_path + '\\' + ''+str("%04d" % (int(os.path.splitext(file)[0])+1)) + '.wav'

        file2 = output_path + '\\' + str(SPEAKER_ID)+"_" + str("%04d" % i) + '.wav'

       # cmd = "ffmpeg -y -i " + file1 + " -ac 1 -ar 22050 -f wav " + file2 + " -y"

        cmd = "ffmpeg -y -i " + file1 + " -ac 1 -ar 22050 -f wav " + file2
        # 对mp3视频进行采样率 格式 声道
        subprocess.call(cmd, shell=True)
        # cmd = "sox " + file2 + " -b 16 " + file2
        # subprocess.call(cmd, shell=True)
        if i == 500 :
            break
        else:
            i = i + 1

def SAVE_SPEAKER_ID(FILE_PATH_DIR,MSG):
    FILE_NAME = "id对应的说话人.txt"
    FILE_PATH = FILE_PATH_DIR+"\\"+FILE_NAME
    # if not os.path.exists(FILE_PATH):
    #     os.mkdir(FILE_PATH)
    FILE = open(FILE_PATH,"a",encoding='utf-8')
    FILE.write(MSG)
    FILE.close()

def REFORM_FLAC_TO_WAV(FILE_DIR_PATH,WAV_PATH):

    FILE_DIR_NAMES = os.listdir(FILE_DIR_PATH)
    SPEAKER_ID = 0 #说话人从0开始
    for FILE_DIR in tqdm(FILE_DIR_NAMES,desc="构造多人数据集进度为:"):
        FILE_DIR2 = FILE_DIR_PATH +"\\"+FILE_DIR #'E:\\newflac\\七七香'
        reform_fre(input_path=FILE_DIR2,output_path=WAV_PATH,SPEAKER_ID=SPEAKER_ID)
        SAVE_SPEAKER_ID(FILE_PATH_DIR=WAV_PATH,MSG=str(SPEAKER_ID)+"-----"+FILE_DIR+"\n")
        SPEAKER_ID = SPEAKER_ID + 1


def read_save_transcript(FILE_PATH,speaker_id):
    path = r'/root/autodl-tmp/myprojectwhisper/whisper-vits-japanese/sliced_audio/'
    newfile_dir = r'D:\project\select_flac_from_txt\newfile'
    newfile_path = newfile_dir +'\\'+'train_filelist.txt'
    file = open(FILE_PATH,'w',encoding='utf-8')
    newfile = open(newfile_path,'w',encoding='utf-8')
    i = 1 #记录行数
    while True:
        print("进行转存操作...")
        txt_line = file.readline()
        if txt_line and i<=500:
            transcript = txt_line.split('|')[2]
            txt = path +"|"+speaker_id +"|"+transcript
            newfile.write(txt+'\n')
        else:
            break
        i = i + 1
def gen_txt(FILES_DIR):
    FILES = os.listdir(FILES_DIR)
    speaker_id = 0
    for FILE in FILES:
        FILE_PATH = FILES_DIR +'\\'+FILE
        read_save_transcript(FILE_PATH =FILE_PATH,speaker_id=speaker_id)
        speaker_id = speaker_id + 1

if __name__ == '__main__':

    print("开始运行程序...")
    start = time.perf_counter()
    TXT_PATH_DIR = r"D:\project\select_flac_from_txt\name"
    FLAC_PATH_DIR = r"E:\PCR\sound2manifest\v"
    FLAC_PATH_SAVE_DIR = r"E:\newflac"
    WAV_PATH = r"E:\wav800"
    """"根据TXT选择FLAC"""
    select_flac_from_txt(TXT_PATH_DIR=TXT_PATH_DIR,FLAC_PATH_DIR=FLAC_PATH_DIR,FLAC_PATH_SAVE_DIR=FLAC_PATH_SAVE_DIR)
    REFORM_FLAC_TO_WAV(FILE_DIR_PATH=FLAC_PATH_SAVE_DIR,WAV_PATH=WAV_PATH)
    #gen_txt(FILES_DIR=TXT_PATH_DIR) 废弃
    end = time.perf_counter()
    runTime = end - start
    print("运行时间：", runTime, "秒")
