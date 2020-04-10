import jieba
import langconv
import langid


class sentence(object):
    def __init__(self):
        self.s = ""
        self.code_mix = 0
        self.note = "" #indicate the sentence is chinese or english or other
        self.token = []
        self.chinese = []
        self.english = []
        self.other = []
        self.symbol = []
        self.translated = []
        
    def split(self,input_s):
        self.s = input_s
        self.token = jieba.tokenize(self.s)
        num_en = 0
        num_zh = 0
        for t in self.token:
            if not t[0].isspace():
                if t[0] in ',，"\'‘’“”#@%<>《》{}【】[]。，！!?？' :
                    self.symbol.append(t)
                else:
                    lang = langid.classify(t[0])[0]
                    if lang == "en":
                        self.english.append(t)
                        num_en += 1
                    elif lang == "zh":
                        self.chinese.append(t)
                        num_zh += 1
                    else:
                        self.other.append(t)
        if num_en == 1 and num_zh == 1:
            code_mix = 1
        if num_en == 0 and num_zh == 0:
            self.note = "other"
        elif num_en > num_zh:
            self.note = "en"
            self.translate_en_zh()
        else:
            self.note = "zh"
            self.translate_zh_en()
            
    def Traditional2Simplified(self,input_s):
        return langconv.Converter('zh-hans').convert(input_s)              
    
    def translate_en_zh(self):
        translated.append("翻译过的中文")
    def translate_zh_en(self):
        translated.append("translated english")
        
#s = sentence()
#s.split("哈哈哈 Good Morning")
#print(s.english)