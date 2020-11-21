from janome.tokenizer import Tokenizer
import markovify

def split(text):
    # 改行、スペース、問題を起こす文字の置換
    table = str.maketrans({
        '\n': '',
        '\r': '',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"':'”',
        "'":"’",
    }) 
    text = text.translate(table)
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    # 1形態素ずつ見ていって、間に半角スペース、文末の場合は改行を挿入
    splitted_text = ""
    for i in range(len(result)):
        splitted_text += result[i]
        if result[i] != '。' and result[i] != '！' and result[i] != '？':
            splitted_text += ' '
        if result[i] == '。' or result[i] == '！' or result[i] == '？':
            splitted_text += '\n'
    return splitted_text

def textGen(file):
    f = open(file, 'r', encoding="utf-8")
    text = f.read()
    sentence = None
    while sentence == None: # 素材によっては空の文章が生成されることがあるので、その対策
        # テキストを処理できる形に分割
        splitted_text = split(text)
        # モデルの生成
        text_model = markovify.NewlineText(splitted_text, state_size=3)

        # モデルを基にして文章を生成
        sentence = text_model.make_sentence(tries=100)   

    # 学習データの保存
    # with open('/content/drive/My Drive/souseki/natsume/learned_data.json', 'w') as f:
    #     f.write(text_model.to_json())

    # データを使いまわす場合
    with open('/content/drive/My Drive/souseki/natsume/learned_data.json') as f:
        text_model = markovify.NewlineText.from_json(f.read())

    # 結合された一連の文字列として返す
    return ''.join(sentence.split())


if __name__ == '__main__':
    for i in range(4):
        result_text = textGen('/content/drive/My Drive/souseki/natsume/kokoro2.txt')
        print(result_text)
        with open('/content/drive/My Drive/souseki/natsume/output.txt', 'a') as f:
            f.write(result_text + "\n")