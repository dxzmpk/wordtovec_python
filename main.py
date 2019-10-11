import word2vec

"""
1. 同义词合并，例如michael jacson和 michael-jackson 
"""
word2vec.word2phrase('./txt_file/text8', './txt_file/text8-phrases', verbose=True)

"""
2. 训练skip-gram model， 得到word2vec词向量表示
"""

word2vec.word2vec('./txt_file/text8-phrases', './word2vectors/text8.bin', size=100, verbose=True)

"""
3. 词向量的应用：单词聚类，产生 text8-clusters.txt 包含所有单词的聚类结果, 结果数目小于等于单词表数目
"""
word2vec.word2clusters('./txt_file/text8', './word2vectors/text8-clusters.txt', 100, verbose=True)

"""
4. model模型的使用
"""

model = word2vec.load('./word2vectors/text8.bin')
print(model.vocab.size)
print(model.vectors[0])
print(model['dog'][:10])
print(model.distance("dog", "cat", "fish"))

indexes, metrics = model.similar("dog")
print(model.vocab[indexes])
print(model.generate_response(indexes, metrics).tolist())
indexes, metrics = model.analogy(pos=['king', 'woman'], neg=['man'])
print(model.generate_response(indexes, metrics).tolist())

"""
5. cluster模型的使用
"""
clusters = word2vec.load_clusters('./word2vectors/text8-clusters.txt')
print(clusters.get_words_on_cluster(90)[:10])

"""
6. cluster和model的结合使用
"""

model.clusters = clusters
indexes, metrics = model.analogy(pos=["paris", "germany"], neg=["france"])
print(model.generate_response(indexes, metrics).tolist())