class Tokenizer(object):
    def __init__(self, words, max_len):
        self.words = words
        self.max_len = max_len

    def fmm_split(self, text):
        '''
        正向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        words = []
        index = 0
        while index < len(text):
            for size in range(min(self.max_len, len(text)-index), 0, -1):
                piece = text[index:index+size]
                if piece in self.words or size == 1:
                    words.append(piece)
                    index += size
                    break
        return words

    def rmm_split(self, text):
        '''
        逆向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        words = []
        index = len(text)
        while index > 0:
            for size in range(min(self.max_len, index), 0, -1):
                piece = text[index-size:index]
                if piece in self.words or size == 1:
                    words.insert(0, piece)
                    index -= size
                    break
        return words

    def bimm_split(self, text):
        '''
        双向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        fmm_words = self.fmm_split(text)
        rmm_words = self.rmm_split(text)
        if len(fmm_words) != len(rmm_words):
            return fmm_words if len(fmm_words) < len(rmm_words) else rmm_words
        fmm_word_set = set(fmm_words)
        rmm_word_set = set(rmm_words)
        return fmm_words if len(fmm_word_set) < len(rmm_word_set) else rmm_words


def load_dict(path):
    tmp = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().split(' ')[0]
            tmp.add(word)
    return tmp


if __name__ == '__main__':
    words = load_dict('dict.txt')
    max_len = max(map(len, [word for word in words]))

    # test
    tokenizer = Tokenizer(words, max_len)
    texts = [
        '研究生命的起源',
        '无线电法国别研究',
        '人要是行，干一行行一行，一行行行行行，行行行干哪行都行。'
]
for text in texts:
    # 前向最大匹配
    print('前向最大匹配:', '/'.join(tokenizer.fmm_split(text)))
    # 后向最大匹配
    print('后向最大匹配:', '/'.join(tokenizer.rmm_split(text)))
    # 双向最大匹配
    print('双向最大匹配:', '/'.join(tokenizer.bimm_split(text)))
    print('')