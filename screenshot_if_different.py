#! python3
#-------------------------------------------------------------------------------
# Name:        camera_capture
# Purpose:     特定範囲のスクリーンショットを撮影し、その中の特定範囲を監視し変化量が既定値以上であれば保存する。マウスカーソルは撮影できない。
#
# Author:      kadota masayuki
#
# Created:     2022/03/16,17
# Copyright:   (c) kadota masayuki 2022
# Licence:     BSD Licence
#-------------------------------------------------------------------------------


import pyscreeze
import os
import time
import sys
import PIL

#起動時引数
#撮影範囲
image_left = -1
image_top = -1
image_right = -1
image_bottom = -1
#監視範囲
monitor_left = -1
monitor_top = -1
monitor_right = -1
monitor_bottom = -1
monitor_pcr_th = 1.0  #0から1までの小数。範囲を逸脱しても可。監視範囲内の「変化の無いピクセル数/総ピクセル数」が、この値未満であれば、撮影範囲に変化ありとして保存する
monitor_color_th = 0  #0から255までの整数。範囲を逸脱しても可。監視範囲内のグレースケール表現されたピクセル値の差の絶対値がこの値以下であれば、ピクセルは同一とみなす
#撮影インターバル
interval_msec = -1



#保存するディレクトリ名
datetime_str = time.strftime("%Y%m%d-%H%M%S")
img_dir_name="./screenshotpy" + datetime_str



#スクリーンショットを監視しまくって保存しまくる
def exec_screenshot():
    #画像保存用ディレクトリを作成
    os.makedirs(img_dir_name, exist_ok=True)
    
    #監視用履歴画像
    monitor_hist2 = PIL.Image.new("RGB", (1, 1), "white")
    
    #画像のカウント
    img_idx = 1

    #監視幅
    monitor_width = monitor_right - monitor_left
    #監視高さ
    monitor_height = monitor_bottom - monitor_top
    #ピクセルマッチ率
    monitor_pix_match_pct = 0.0
    #ピクセルマッチ数
    monitor_pix_match_cnt = 0
    #総ピクセル数
    monitor_pix_total_cnt = monitor_width * monitor_height
    #繰り返しスクリーンショットを撮り、ファイルに保存
    while(True):
        #スクリーンショット(PIL形式で取得)
        img = pyscreeze.screenshot(region = (image_left, image_top, image_right, image_bottom))
        #監視
        is_image_changed = True
        if (monitor_left >= 0):
            ##opencvで扱える型に変更
            #img = np.asarray(img)
            #監視範囲の切り出し
            monitor_hist1 = img.crop((monitor_left - image_left, monitor_top - image_top, monitor_right - image_left, monitor_bottom - image_top))
            #監視範囲をグレー化
            if ((monitor_hist2.width != monitor_hist1.width) or (monitor_hist2.height != monitor_hist1.height)):
                #履歴無いので履歴にグレー画像をセットして、変化ありフラグを立てておく
                monitor_hist2 = monitor_hist1.convert('L')
                is_image_changed = True
            else:
                #履歴と比較するためにグレー化
                monitor_hist1 = monitor_hist1.convert('L')
                #監視範囲の変化確認
                monitor_pix_match_cnt = 0
                #配列化して1ピクセルずつ比較
                monitor_hist_array1 = monitor_hist1.getdata()
                monitor_hist_array2 = monitor_hist2.getdata()
                for x in range(0, monitor_width, 1):
                    for y in range(0, monitor_height, 1):
                        if (abs(monitor_hist_array1[y * (monitor_width) + x] - monitor_hist_array2[y * (monitor_width) + x]) <= monitor_color_th):
                            monitor_pix_match_cnt = monitor_pix_match_cnt + 1
                #同一ピクセル数の割合
                monitor_pix_match_pct = monitor_pix_match_cnt / monitor_pix_total_cnt
                if (monitor_pix_match_pct < monitor_pcr_th):
                    #変化ありフラグ
                    is_image_changed = True
                else:
                    is_image_changed = False
                #履歴置き換え
                monitor_hist2 = monitor_hist1
        if (is_image_changed):
            #png形式で、指定ディレクトリに、ゼロ埋めのファイル名で保存
            img_output_file_name = '{}/{:010d}.png'.format(img_dir_name, img_idx)
            print(img_output_file_name)
            img.save(img_output_file_name)
            #監視範囲を保存(普段は不要なのでコメントアウト)
            #monitor_hist2.save('{}/monitor_{:010d}.png'.format(img_dir_name, img_idx)
            #番号を1増やす
            img_idx = img_idx + 1
            #更新したことをお伝え
            print(time.strftime("image updated %Y%m%d-%H%M%S"))
        #判定結果をお伝え
        print("{} : match {}/{}={:.3f} (threshold={:.3f}) : press Ctrl+C to finish".format(img_idx, monitor_pix_match_cnt, monitor_pix_total_cnt, monitor_pix_match_pct, monitor_pcr_th))
        #指定時間待機
        time.sleep(interval_msec)



if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 2):
        msg = """スクリーンショット取得&監視&保存
インターバルをミリ秒単位で指定して起動してください(必須)。
また、切り取り座標と監視座標を指定できます。
  例 : command 500 -r,50,0,1024,768 -m,100,200,300,400,0.85,4
     0.5秒ごとに、左上(X50,Y0)、右下(X1024,Y768)を撮影
     取得した画像の左上(X150,Y200)、右下(X350,Y400)を監視
     監視範囲のうち、変化が無いピクセル数が85%未満なら
     撮影した画像を保存する
     ※変化が無いピクセル数の割合を1.0と指定すると、1ピクセルでも変化あれば保存
     ただし、同一座標のピクセル値の差の絶対値が4以下なら変化なしと判断する
     ※255以上を設定すると、変化ありにならない
     ※0未満を設定すると、変化なしにならない
  例 : command 1000
     1秒ごとに全画面を撮影し、保存する
  例 : command 500 -m,200,300,400,500,0.4,128
     0.5秒ごとに全画面を撮影し、左上(X200,Y300)、右下(X400,Y500)を監視
     監視範囲のうち、変化が無いピクセル数が40%未満なら
     撮影した画像を保存する
     ただし、同一座標のピクセルの値の差が128以下なら変化無しと判断する
  例 : command 300 -r,0,0,1024,768
     0.3秒ごとに左上(X0,Y0)、右下(X1024,Y768)を撮影し、保存する
"""
        print(msg)
        exit(1)
    if (len(args) >= 2):  # 撮影インターバル[ms]
        interval_msec = int(args[1])
    for i in range(2, len(args)):
        arr = args[i].split(",")
        if (arr[0] == "-r"):  # 撮影範囲
            image_left = int(arr[1])
            image_top = int(arr[2])
            image_right = int(arr[3])
            image_bottom = int(arr[4])
        elif (arr[0] == "-m"):  # 監視範囲
            monitor_left = int(arr[1])
            monitor_top = int(arr[2])
            monitor_right = int(arr[3])
            monitor_bottom = int(arr[4])
            monitor_pcr_th = float(arr[5])
            monitor_color_th = int(arr[6])
    #起動時引数で撮影サイズを指定しなかったとき、デスクトップ画面の大きさを取得
    if (image_left < 0):
        img = pyscreeze.screenshot()
        image_left = 0
        image_top = 0
        image_bottom = img.height
        image_right = img.width
    #監視範囲が指定されていた場合は、撮影範囲内であることを確認
    if (monitor_left >= 0):
        if (monitor_left < image_left):
            monitor_left = image_left
        if (monitor_top < image_top):
            monitor_top = image_top
        if (monitor_right > image_right):
            monitor_right = image_right
        if (monitor_bottom > image_bottom):
            monitor_bottom = image_bottom
    #指定内容を出力
    print("screenshot interval {} sec, (left,top)(right,bottom)=({},{}),({},{})".format(interval_msec, image_left, image_top, image_right, image_bottom))
    print("monitor    threshold {:.3f}, {} (left,top)(right,bottom)=({},{}),({},{})".format(monitor_pcr_th, monitor_color_th, monitor_left, monitor_top, monitor_right, monitor_bottom))

    exec_screenshot()

    print("Finish")
