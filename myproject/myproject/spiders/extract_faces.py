import sys
import os

import cv2


try:
    # 顔検出用の特徴量ファイルのパス
    cascade_path = sys.argv[1] 
except IndexError:
    # コマンドライン引数が足りない場合は、使い方を表示して終了する。
    print('Usage: python extract_faces.py CASCADE_PATH IMAGE_PATH...', file=sys.stderr)
    exit(1)

print(sys.argv[1])
# 顔検出用の出力先ディレクトリが存在しない場合は作成しておく。
output_dir = 'faces'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

assert os.path.exists(cascade_path)

# 特徴量ファイルのパスを指定して、分類器オブジェクトを作成する。
classifier = cv2.CascadeClassifier(cascade_path)

# 第２引数以降のファイルパスについて反復処理をする。
for image_path in sys.argv[2]:
    print('processing', image_path, file=sys.stderr)

    # コマンドライン引数で与えたパスの画像ファイルを読み込む。
    image = cv2.imread(image_path)

    # 顔検出を高速化するため、画像をグレースケールに変換する。
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # 顔を検出する
    faces = classifier.detectMultiScale(gray_image)

    # 画像ファイル名の拡張子を除いた部分を取得する。
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # 取得できた顔のリストについて反復処理を行う。
    # i は、0 からの連番を表す。
    for i,(x,y,w,h) in enumerate(faces):
        # 顔の部分だけを切り取った画像を取得する。
        face_image = image[y:y + h , x:x + w]

        # 出力先のファイルパスを組み立てる
        output_path = os.path.join(output_dir,'{0}_{1}.jpg',format(images_name, i ))
        
        # 顔の画像を保存する。
        cv2.iwrite(output_dir,face_image)
