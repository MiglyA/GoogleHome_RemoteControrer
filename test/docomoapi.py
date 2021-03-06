import datetime
import argparse
import subprocess
import requests

# config
# ===========================================
# Docomo 音声合成 API
API_KEY = '6855693376564975533566726e496d352f4e767267566954594339757a4e37702e6665464546744b616e33'
url = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY=" + API_KEY

# aitalk パラメーター設定
# ===========================================

"""
参考）音声合成 | docomo Developer support
https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=text_to_speech&p_name=api_1#tag01

    'speaker' : "nozomi"、"seiji"、"akari"、"anzu"、"hiroshi"、"kaho"、"koutarou"、"maki"、"nanako"、"osamu"、"sumire"
    'pitch' : ベースライン・ピッチ。 基準値:1.0、範囲:0.50～2.00
    'range' : ピッチ・レンジ。基準値:1.0、範囲:0.00～2.00
    'rate' : 読み上げる速度。基準値:1.0、範囲:0.50～4.00
    'volume' : 音量。基準値:1.0、範囲:0.00～2.00
"""

prm = {
	'speaker': 'maki',
	'pitch': '1',
	'range': '1',
	'rate': '1',
	'volume': '2'
}

# パラメーター受取
# ===========================================
# %% arguments
parser = argparse.ArgumentParser()
parser.add_argument('--text', type=str, required=True)
text = input(">>")

# SSML生成
# ===========================================
xml = u'<?xml version="1.0" encoding="utf-8" ?>'
voice = '<voice name="' + prm["speaker"] + '">'
prosody = '<prosody rate="' + prm['rate'] + '" pitch="' + prm['pitch'] + '" range="' + prm['range'] + '">'
xml += '<speak version="1.1">' + voice + prosody + text + '</prosody></voice></speak>'

# utf-8にエンコード
xml = xml.encode("UTF-8")

# Docomo APIアクセス
# ===========================================
print("Start API")
print(xml)

response = requests.post(
	url,
	data=xml,
	headers={
		'Content-Type': 'application/ssml+xml',
		'Accept': 'audio/L16',
		'Content-Length': len(xml)
	}
)

# print(response)
# print(response.encoding)
# print(response.status_code)
# print(response.content)

if response.status_code != 200:
	print("Error API : " + response.status_code)
	exit()

else:
	print("Success API")

# 現在日時を取得
now = datetime.datetime.now()
tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')

# 保存するファイル名
rawFile = tstr + ".raw"
wavFile = tstr + ".wav"

# バイナリデータを保存
fp = open(rawFile, 'wb')
fp.write(response.content)
fp.close()

print("Save Binary Data : " + rawFile)

# バイナリデータ → wav に変換
# ===========================================

# macのsoxを使って raw→wavに変換
cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 " + rawFile + " " + wavFile
# コマンドの実行
subprocess.check_output(cmd, shell=True)

print("Done : " + wavFile)
