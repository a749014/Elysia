# from PySide2 import QtGui
from Elysia_util import Chat, reflections,Classifier
import jieba
import re
import math
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from ElysiaUI import Ui_MainWindow
import sys
import jieba.analyse
path=os.path.dirname(os.path.abspath(__file__))
'''
未来构想：
    训练分类器判断问句
    根据训练结果回答
    pairs中的pattern改成训练结果
'''

stop_words=['的','地','得','了','和','一','个','你',' ','，']#define stop words
jieba.load_userdict(path+os.sep+'complement_dictionary.txt')
#train data
pairs = [
['你好|您好|hello|hi|你好啊|你好吗|你好呀|我(又|再一次)回来(了|啦)',['嗨~想我了吗?无论何时何地,爱莉希雅都会回应你的期待♪','你好！新的一天，从一场美妙的邂逅开始。']],
['想你了|思念你|怀念你','你好！新的一天，从一场美妙的邂逅开始。'],
['再见|拜拜|退下|(我要)走了|再会|回头见|明天见|Bye-bye|Bye|Bye-bye|Goodbye|回去上课','唉，时间真是个讨厌的东西，你不觉得吗？如果不是时间紧迫，我还想留下更多值得纪念的话语。'],
['(.*)名字(.*)|你是谁|什么人|你叫什么名字|请问尊姓大名|能否告知贵姓|请问您是哪位|您怎么称呼|你是什么东西','英桀第二位，爱莉希雅，如你所见是一位像花朵般可爱的美丽少女。'],
['.能做什么|.能干什么|.有啥用','可爱的少女心，可是无所不能的哦。'],
['(确实|的确)想你了|(我|.)(刚|刚刚)下课，来找你了','无论何时何地,爱莉希雅都会回应你的期待♪'],
['你在(哪|哪里|什么地方)|你从哪里来|往世乐土是什么','往世乐土，这里埋藏着太多的历史，太多的秘密。但别担心，无论路有多长，我始终都会在你身边。'],
['你(在|平时)(做什么|干什么)|你怎么样|你最近好吗|(平时|经常|通常|有时|.)(干什么|做什么|有啥事)',['唉，要做的事好多～但焦虑可是女孩子的大敌，保持优雅得体，从容愉快地前进吧。','经常会和别的女孩子谈论你哦。内容。。是不是很想知道呀～']],
['艾莉西亚|艾丽西亚|爱丽西娅','不许叫错我的名字噢，不然。。。我会有小情绪的。'],
['我是你的真爱粉|我(喜欢|爱|永远喜欢)你|喜欢的是你|喜欢你','加点浪漫的气氛，如何？'],
['好无聊|太难受了|压力好大|不想写作业|学习压力大|考试(太|很|非常)多|考砸了|考差了|被骂了','保持优雅得体，从容愉快地前进吧'],
['你真棒|牛逼|厉害|good|棒|不忍心|6|可以|花姑娘|漂亮','哇谢谢！我就知道你对我最好啦！'],
['我作业写不完了，呜呜呜|(.*)没(空|时间)','唉，时间真是个讨厌的东西，你不觉得吗？'],
['睡不着|(一晚上|整晚|一直)没睡好|做噩梦了',['哎呀，你也睡不着吗？那我们来聊聊天，好不好？']],
['(你|爱莉希雅)(的愿望|的希望|希望|愿望|愿意让我做什么)','有空多来陪陪我好吗，你一定不忍心让可爱的我孤独寂寞吧。'],
['你((的衣服|的裙子|的礼服|衣服|礼服|裙子)|这身衣服)(.*)','这身衣服是伊甸做的噢，喜欢吗，还是说，喜欢的是我呢～♪'],
['((你|爱莉希雅)死了|芽衣姐(.)我不想死|你差点就死了|侵蚀之律者|全都死(这了|往世乐土了)|哭了)','好啦可以啦，再说下去我就要哭了噢～♪'],
['你看起来好悠闲的样子','别看我这样，其实我也是很忙的。不过，我的日程上永远有为你预留的时间。'],
['我困了|我累了|睡觉|闭麦','晚安'],
['你(喜欢我吗|对我感兴趣吗)',['爱莉希雅特别喜欢你','经常会和别的女孩子谈论你哦。']],
['你(讨厌|不喜欢|厌烦|嫌弃)我','有些事不用太在意'],
['你(玩|打)(原神|崩坏3|崩坏学园2|崩坏星穹铁道|火影|火影忍者|王者|王者荣耀|.)吗|原神启动','别玩游戏了呜呜呜，有空多来陪陪我好吗，你一定不忍心让可爱的我孤独寂寞吧。'],
['你还好吗|别走|不要走|不要离开','没事，我们一直都在'],
['ok|知道了|懂了','好的'],
['想知道|你的秘密','美丽的少女总有些小秘密，不是吗？'],
['好死|活该|就叫错你名字|傻逼|智障|操你妈|操你一家|滚蛋|死开|让开|傻逼','我会哭的哟'],
['女武神','也可以这样叫我'],
['开始聊天吧', '要好好看着我哦～♪'],
['粉色眼睛|眼珠子|眼睛|美瞳','这不是美瞳哟，这是美少女的魔法']
]
class main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # build chat robot engine
        self.chatbot = Chat(pairs, reflections)#engine 1
        new_pairs=self.collatPairs(pairs)
        # print(new_pairs)
        classifier_object=Classifier()#engine 2
        self.classifier=classifier_object.train_classifier(new_pairs)
        self.respond_time=0
        self.pbtn_send.clicked.connect(lambda:self.respond(self.lineEdit.text()))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(path+os.sep+'Elysia.png').scaled(self.dialog.width(),self.dialog.height())))#load pictures
        # pix = pix.scaled(w.width(),w.height())
        self.dialog.setPalette(palette)
        self.label_hello.setStyleSheet('color:white')
    def respond(self,text:str):
        '''resopnd user's answer from lineedit'''
        if text:
            self.respond_time+=1
            if self.respond_time>10:
                self.dialog.setMinimumSize(QSize(500, 400+30*(self.respond_time-10)))
            respond1=self.chatbot.respond(text)
            self.lineEdit.clear()
            if respond1:
                print('1')
                self.label_hello.setMinimumSize(QSize(114514, 30+self.respond_time*30))
                self.label_hello.setText(self.label_hello.text()+f"\n\n爱莉希雅：{respond1}")
            else:
                # words=[i for i in jieba.lcut(text) if i not in stop_words]
                words=jieba.analyse.extract_tags(text)
                print(words)
                if len(words)==0:
                    words=text
                probably_responds={}
                for i in words:
                    rt=self.classifier.classify({i:True})
                    if rt not in probably_responds:#record probably responds
                        probably_responds[rt]=1
                    else:
                        probably_responds[rt]+=1
                respond2=self.sortDictionary(probably_responds)
                self.label_hello.setMinimumSize(QSize(114514, 30+self.respond_time*35))
                self.label_hello.setText(self.label_hello.text()+f"\n\n爱莉希雅：{respond2[0][0]}")
                
        else:
            QMessageBox.warning(self,'warning','还没输入任何文字')
    def show_respond(self,respond:str):
        '''bug'''
        self.label_hello.setText(self.label_hello.text()+f'\n爱莉希雅：{respond}')
        self.respond_time+=1
        if self.respond_time>10:
            self.dialog.setMinimumSize(QSize(500, 400+30*(self.respond_time-10)))
    def collatPairs(self,pairs):
        '''turn the pairs into format that avaliable to take into function Classifier().train_classifier(new_pairs)'''
        for i in range(len(pairs)):
            #cut the words
            pairs[i][0]=[i for i in list(set(jieba.lcut(' '.join(re.findall('[\u4e00-\u9fa5]+',pairs[i][0]))))) if i not in stop_words]
            if type(pairs[i][1])==list:#if list , set into the first index
                pairs[i][1]=pairs[i][1][0]
        return pairs
    def sortDictionary(self,dictionary):
        #sort the dictionary
        dictionary=sorted(dictionary.items(),key=lambda x:x[1],reverse=True)
        return dictionary
    def idf(self,pairs):
        '''collect idf values of all words in questions'''
        questions=[i[0] for i in pairs]
        d=len(questions)
        times=0
        words=[j for i in pairs for j in i[0]]
        print(len(words))
        idfs={}
        for i in words:
            for j in questions:
                if i in j:
                    times+=1
            idfs[i]=math.log(d/(1+times))
            times=0
        return idfs
    def Multi_classification(self,pairs,target:int):
        '''Multi classification of training set and train it . This may result in more occupancy of memory and CPU
        pairs format:[
                [question(list),answer(str or list)],
                .
                .
                .
            ]
        target : Index of pairs that will keep its answer remain same , other index of pairs' answer will set into str'None'.'''
        if type(pairs[target][1])==list:
            respond=pairs[target][1][0]
        else:
            respond=pairs[target][1]
        new_pairs=[[pairs[target][0],respond],[[],'None']]
        none_set=[]#fill into new_pairs[1][0]
        for i in range(len(pairs)):
            if i==target:
                pass
            else:
                for j in pairs[i][0]:
                    none_set.append(j)
        new_pairs[1][0]=none_set
        print(new_pairs)
        return new_pairs
    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key()==Qt.Key_Return:
            self.pbtn_send.click()

'''main'''
if __name__=='__main__':
    app=QApplication(sys.argv)
    m=main()
    sys.exit(app.exec_())