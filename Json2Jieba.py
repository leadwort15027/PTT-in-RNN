########################################################
# python Json2Jieba.py INPUT_FILE_NAMW OUTPUT_FIE_NAME #
########################################################
import json
import sys
import logging
import jieba
from gensim.models import word2vec

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(level=logging.INFO,format="[%(levelname)s] %(message)s")
jieba.set_dictionary("jieba/dict.txt")

#Load json file
with open(sys.argv[1]) as data_file:
	data = json.load(data_file)
articles =  data.get("articles")

#Parse and format json file
total_line = 0
with open("temp/content","w") as file:
	for i in range(len(articles)):
		logging.info("Writing Article : %d / %d" %(i+1,len(articles)))

		#get article i's title, content and each messages
		file.write(articles[i].get("article_title")+"\n")
		file.write(articles[i].get("content")+"\n")
		for j in range(len(articles[i].get("messages"))):
			file.write(articles[i].get("messages")[j].get("push_content")+"\n")
		
		total_line += len(articles[i].get("messages"))+2
		#total message + content + title per article

#Cut word
line_num = 0
with open("temp/word","w") as output_file:
	with open("temp/content","r") as content:
		for line in content:
			line_num+=1
			logging.info("Cutting Line : %d / %d" %(line_num, total_line))
			words = jieba.cut(line, cut_all=False)
			for word in words:
				output_file.write(word+" ")

#word to vector
sentences = word2vec.Text8Corpus("temp/word")
model = word2vec.Word2Vec(sentences, size=250)
model.save_word2vec_format(sys.argv[2])

logging.info("Finished")
