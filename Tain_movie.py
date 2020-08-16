# ALL in One

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox, glob
import cv2
import numpy as np

# フォルダ選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.getcwd()
tkinter.messagebox.showinfo('○×プログラム','対象ディレクトリを選択してください！')

# ここの1行を変更
dir = tkinter.filedialog.askdirectory(initialdir = iDir)


# 処理ディレクトリパスの出力
tkinter.messagebox.showinfo('○×プログラム',dir)

# 読み込みファイル名一括変更：先頭の５文字（フォルダのパスに注意）や終わりの４文字
# PathFolderに作業ディレクトリのパスを入力

PathFolder = dir

os.chdir(PathFolder)
path = '*.jpg'
flist = glob.glob(path)

# 先頭5文字を抽出（CTなど）
for file in flist:
  os.rename(file, file[:5] + '.jpg')

files = glob.glob('*.jpg')
MAISU = len(files)

# もとになるファイルを作る。２次元画像を重ねて３次元にする。


# イメージファイルのパス。1枚目と2枚目を重ねておく！
img0 = cv2.imread('00001.jpg', cv2.IMREAD_GRAYSCALE)
img1 = cv2.imread('00002.jpg', cv2.IMREAD_GRAYSCALE)
sum0 = np.stack([img0, img1])
sumt = sum0

# 後ろ（前）に二次元画像を重ねていく。

for i in range(2, MAISU):
    img = cv2.imread('{0:05d}.jpg'.format(i), cv2.IMREAD_GRAYSCALE)
    sumt = np.concatenate([sumt, [img]], axis=0)

pixels = sumt
    
# ボリュームデータから、冠状断動画を作る

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

# ！グレースケールの時は、５つめの変数をFalseにする！
video = cv2.VideoWriter('coronal.mp4', fourcc, 20.0, (pixels.shape[2], pixels.shape[0]), False)
MAISU_video = pixels.shape[1]
for i in range(0, MAISU_video):
    img = pixels[:, i, :]
    img = np.asarray(img)
    img = cv2.resize(img, dsize=(pixels.shape[2], pixels.shape[0]))
    video.write(img)

video.release()


# ボリュームデータから、水平断動画を作る

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

# ！グレースケールの時は、５つめの変数をFalseにする！
video = cv2.VideoWriter('axial.mp4', fourcc, 20.0, (pixels.shape[2], pixels.shape[1]), False)
MAISU_video = pixels.shape[0]
for i in range(0, MAISU_video):
    img = pixels[i, :, :]
    img = np.asarray(img)
    img = cv2.resize(img, dsize=(pixels.shape[2], pixels.shape[1]))
    video.write(img)

video.release()


# In[ ]:




