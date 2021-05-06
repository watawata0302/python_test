from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import PySimpleGUI as GUI
import webbrowser

# 画面レイアウトを指定
layout = [
  [GUI.Text('JPEGファイル選択'), GUI.InputText(), GUI.FileBrowse()],
  [GUI.Submit(button_text = '検索')]]

# ウィンドウを表示する関数
def show_window():
    win = GUI.Window('JPEGファイルの撮影場所表示プログラム', layout)
      
    # イベントループ
    while True:
        event, values = win.read()
        
        # ウィンドウの×ボタン押下
        if event is None: break
        # 検索ボタン押下  
        if event == '検索':
            exif_info = get_exif(values[0])
            gps_info = get_gps(exif_info)

            # ブラウザ指定(実行ファイルまでの絶対パス指定)
            browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
            url = "https://www.google.com/maps/search/?api=1&query=" + gps_info
            browser.open(url)
    win.close()

# 画像ファイルのEXIF情報を取得する関数
def get_exif(file):
    output = {}
    Im = Image.open(file)
    #EXIF情報を取得
    # 存在しなければそのまま終了
    try:
        exif = Im._getexif()
    except AttributeError:
        return print('このファイルにはEXIF情報がありません。')
    
    # EXIF情報を表示
    for tag_id, value in exif.items():
        TAG_info = TAGS.get(tag_id, tag_id)
        output[TAG_info] = value

    return output

# 緯度/経度ダグを度分秒(DMS)形式に変換する関数
def format_DMS(ref, value):
    D = int(value[0])
    M = int(value[1])
    S = value[2] 
    # F-stringで変換
    return f"{D}°{M}'" + f'{S}"{ref}' 

# EXIF情報からGPS情報(緯度/経度)を取得する関数
def get_gps(exif_info):
    gps = {}
    # EXIF情報 に GPSInfo タグが含まれているときに処理
    if 'GPSInfo' in exif_info:
    # EXIF情報から GPS情報を取り出す
        gps_tags = exif_info['GPSInfo']
    # GPS情報を辞書に格納する
        for t in gps_tags:
            gps[GPSTAGS.get(t,t)] = gps_tags[t]

        # 緯度/経度のタグがあることを確認した上で処理する
        is_lati = gps['GPSLatitude'] 
        is_lati_ref = gps['GPSLatitudeRef']
        is_longi = gps['GPSLongitude']
        is_longi_ref = gps['GPSLongitudeRef']
        
        if is_lati and is_lati_ref and is_longi and is_longi_ref:
            # 緯度/経度ダグを度分秒(DMS)形式に変換する
            lati = format_DMS(is_lati_ref, is_lati)
            longi = format_DMS(is_longi_ref, is_longi)
            return f'{lati} {longi}'
        else:
            return print('このファイルには緯度/経度の情報がありません。')
    else:
        return print('このファイルにはGPS情報がありません。')


# モジュールとしてこのプログラムを使用することになったときのための記述
# このファイルを直接実行したときは変数__name__の値が__main__となりif文が実行される
# importされた際は変数__name__の値がモジュール名(ファイル名)になり実行されないようにするための記述

if __name__ == '__main__':
    show_window()
    
    