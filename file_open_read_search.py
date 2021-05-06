from chardet.universaldetector import UniversalDetector
import PySimpleGUI as GUI

# 画面レイアウトを指定
layout = [
  [GUI.Text('検索ファイル'), GUI.InputText(), GUI.FileBrowse()],
  [GUI.Text('検索文字列   '), GUI.InputText()],
  [GUI.Submit(button_text = '検索')]]
            
            
# ウィンドウを表示する関数
def show_window():
    win = GUI.Window('ファイル内文字列検索', layout)
      
    # イベントループ
    while True:
        event, values = win.read()
        
        # ウィンドウの×ボタン押下
        if event is None: break
        # 検索ボタン押下  
        if event == '検索':
            file_code = check_encoding(values[0])
            file_read_search(values[0], values[1], file_code) 

    win.close()

# ファイルの文字コード判定
def check_encoding(file_path):
    try:
        detector = UniversalDetector()
        with open(file_path, mode='rb') as f:
            for binary in f:
                detector.feed(binary)
                #ある程度、ファイルを読んだら読込終了
                if detector.done:
                    break
            detector.close()
            
    # ファイルが存在しなかった場合
    except FileNotFoundError as e: 
       print('ファイルが見つかりません', e)
    # Exceptionは、それ以外の例外が発生した場合
    except Exception as e: 
       print('予期せぬエラーです', e)
    
    return detector.result['encoding'] 


# 文字列を検索　文字列を含む行を表示する
def file_read_search(file_name, word, code):
    list1 = []
    try:
        # withならcloseが不要
        with open(file_name, 'r', encoding = code) as file:
            for line in file: # 一行ずつ読み取って処理する
                if word in line: # 読み込んだ行にwordが含まれていたら配列に追加
                    list1.append(line)
        
        if not list1:
            GUI.popup('ファイル内に検索した文字列はありません。', title = '検索結果', keep_on_top = True)
        else:
            list = '\n'.join(list1)
            GUI.popup( list, title = '検索結果', keep_on_top=True)
                
    # ファイルが存在しなかった場合
    except FileNotFoundError as e: 
       print('ファイルが見つかりません', e)

    # Exceptionは、それ以外の例外が発生した場合
    except Exception as e: 
       print('予期せぬエラーです', e)

# モジュールとしてこのプログラムを使用することになったときのための記述
# このファイルを直接実行したときは変数__name__の値が__main__となりif文が実行される
# importされた際は変数__name__の値がモジュール名(ファイル名)になり実行されないようにするための記述

if __name__ == '__main__':
    show_window()