import re
import time
import os
from tqdm import tqdm
import shutil
import sys

def SAVE_SPEAKER_ID(FILE_PATH_DIR,MSG):
    FILE_NAME = "id对应的说话人.txt"
    FILE_PATH = FILE_PATH_DIR+"\\"+FILE_NAME
    # if not os.path.exists(FILE_PATH):
    #     os.mkdir(FILE_PATH)
    FILE = open(FILE_PATH,"a",encoding='utf-8')
    FILE.write(MSG)
    FILE.close()


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


def flac_to_wav(input_path, output_path,SPEAKER_ID,i): ##返回生成的名称

    file1 = input_path
    file2 = output_path +"\\"+str(SPEAKER_ID)+"_"+ str("%04d"%i)+'.wav'
    # cmd = "ffmpeg -y -i " + file1 + " -ac 1 -ar 22050 -f wav " + file2
    # # # 对mp3视频进行采样率 格式 声道
    # subprocess.call(cmd, shell=True)
    name = file2.rsplit('\\',1)[1]
    return name

def open_txt_file(TXT_PATH, flac_file_name,speaker_id,output_path):

    print("正在对[" + TXT_PATH + "]文件进行操作")
    TXT_FILE = open(TXT_PATH, encoding='utf-8')

    train_filelist_path =output_path+"\\"+'train_filelist.txt'
    val_filelist_path = output_path+"\\"+'val_filelist.txt'

    train_filelist = open(train_filelist_path,'a',encoding='utf-8')#训练集  500
    val_filelist = open(val_filelist_path,'a',encoding='utf-8')#验证集 50

    i = 1  # 记录行数
    while True:
        print("正在对[" + TXT_PATH + "]的第" + str(i) + "行进行处理")
        TXT_LINE = TXT_FILE.readline()
        if TXT_LINE and i <= 500:  ##获取到的行数
            transcript = TXT_LINE.split('|')[2] ##文字
            WAV_NAME_EXPAND = TXT_LINE.split('|')[0]  ##获取WAV文件的名称包含扩展名 vo_adv_0000011_1.wav
            WAV_NAME = WAV_NAME_EXPAND.split('.')[0]  ##获取文件名
            flac_name = WAV_NAME+'.flac' ## vo_adv_0000011_1.flac
            flac_file_path = flac_file_name + "\\"+flac_name  #E:\newflac\七七香\vo_adv_0000427_1.flac
            wav_name = flac_to_wav(input_path=flac_file_path,output_path=output_path,SPEAKER_ID=speaker_id,i=i)
            path = r'/root/vits/wavs/'
            txt = path + wav_name + "|" + str(speaker_id) + "|" + transcript  # /root/autodl-tmp/myprojectwhisper/whisper-vits-japanese/sliced_audio/0_0001.wav|0|ふーーーー！　楽勝楽勝☆夜は焼肉っしょー♪あははははは！
            if i%10 !=1:
                train_filelist.write(txt) #存入训练集
            else:
                val_filelist.write(txt) #存入验证集
        else:
            break
        i = i + 1
    train_filelist.close()
    val_filelist.close()
    TXT_FILE.close()

def multi_wav_txt_gen(TXT_PATH_DIR, FLAC_PATH_SAVE_DIR,output_path):
    TXT_FILES = os.listdir(TXT_PATH_DIR)
    speaker_id = 0
    for TXT_FILE in tqdm(TXT_FILES, desc="当前进度为："):
        TXT_FILE_PATH = TXT_PATH_DIR + "\\" + TXT_FILE  # 拼接的文件路径 D:\project\select_flac_from_txt\name\七七香.txt
        temp_str = TXT_FILE_PATH.split('.')[0]  ##  D:\project\select_flac_from_txt\name\七七香
        temp_str = temp_str.rsplit('\\',1)[1] ## 七七香
        file_name = FLAC_PATH_SAVE_DIR +"\\"+temp_str ##  E:\newflac\七七香
        """传入路径,打开TXT文件"""
        ##
        open_txt_file(TXT_PATH=TXT_FILE_PATH,flac_file_name=file_name,speaker_id=speaker_id,output_path=output_path)
        SAVE_SPEAKER_ID(FILE_PATH_DIR=output_path,MSG=str(speaker_id)+"----------"+temp_str+"\n")
        speaker_id = speaker_id + 1 #随机选择speaker_id


def pre_process(input_path,output_path):

    with open(input_path,'r',encoding='utf-8') as f:
        content  = f.read()

    #【0123–456789】\{ play\}『』★（NIGHTMARE）♩♪♫♬

    str1 = r'♪'
    str2 =r'{player}'
    str3 = r'（NIGHTMARE）'
    str4 = r'★'
    str5 = r'『'
    str8 = r'』'
    str6 = r'【'
    str7 = r'】'
    str9 = r'☆'
    a1 = re.sub(str1,'',content)#
    a2 = re.sub(str2,'',a1)
    a3 = re.sub(str3, '', a2)
    a4 = re.sub(str4, '', a3)
    a5 = re.sub(str5, '', a4)
    a6 = re.sub(str6, '', a5)
    a7 = re.sub(str7, '', a6)
    a8 = re.sub(str8, '', a7)
    a9 = re.sub(str9,'',a8)



    fh = open(output_path, 'w', encoding='utf-8')
    fh.write(a9)
    fh.close()


if __name__ == '__main__':

    print("开始运行程序...")
    start = time.perf_counter()
    TXT_PATH_DIR = r"D:\project\select_flac_from_txt\name"
    FLAC_PATH_SAVE_DIR = r"E:\newflac"
    WAV_PATH = r"E:\500"

    """"根据TXT选择FLAC"""
    multi_wav_txt_gen(TXT_PATH_DIR=TXT_PATH_DIR, FLAC_PATH_SAVE_DIR=FLAC_PATH_SAVE_DIR,output_path=WAV_PATH)
    pre_process(input_path=r'E:\500\train_filelist.txt',output_path=r'E:\1.txt')
    pre_process(input_path=r'E:\500\val_filelist.txt', output_path=r'E:\2.txt')
    end = time.perf_counter()
    runTime = end - start
    print("运行时间：", runTime, "秒")
