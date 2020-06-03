import os

from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
# Create your views here.
from app1 import models
from django.shortcuts import render, redirect
from django.utils.timezone import now

from app1.models import *

CHUNK = 1024
dir_path = 'F:\\大三下\\shuyin\\static'

def first(request):
    if request.method == "GET":
        chapterId = request.GET['chapterId']
        uid = request.GET['uid']

        return render(request, 'first.html', {'cid': chapterId,
                                              'uid': uid})


def chapter(request):
    if request.method == 'GET':
        chapterId = request.GET['chapterId']
        uid = request.GET['uid']

        max = ChapterthumbsUp.objects.filter(chapterid=chapterId).count()
        path = None
        ccomment = Ccomment.objects.filter(chapterid=chapterId)
        chapter = Chapter.objects.get(id=chapterId)
        cmax = ccomment.count()
        state = '未点赞'
        if ChapterthumbsUp.objects.filter(chapterid=chapterId, userid=uid).exists():
            state = '已点赞'
        audio = Audio.objects.all().order_by("id")
        return render(request, 'chapterReading.html', {'audios': audio,
                                                           'chapter': chapter,
                                                           'uid': uid, 'max':max,'state':state,
                                                           'ccomment':ccomment,
                                                           'cmax':cmax,})

def play(request):
    if request.method == 'GET':
        chapterId = request.GET['cid']
        uid = request.GET['uid']
        audioid = request.GET['audioid']
        file = Audio.objects.get(id=audioid)

        max = ChapterthumbsUp.objects.filter(chapterid=chapterId).count()
        ccomment = Ccomment.objects.filter(chapterid=chapterId)
        chapter = Chapter.objects.get(id=chapterId)
        cmax = ccomment.count()
        state = '未点赞'
        if ChapterthumbsUp.objects.filter(chapterid=chapterId, userid=uid).exists():
            state = '已点赞'
        audio = Audio.objects.all().order_by("id")
        atcount = Audiothumbsup.objects.count() # 音频点赞量
        acomment = Acomment.objects.filter(audioid=file.id)
        amax = acomment.count() # 音频评论量
        astate = '未点赞'
        if Audiothumbsup.objects.filter(worksid=file.id, userid=uid).exists():
            astate = '已点赞'
        return render(request, 'chapterReading.html', {'audios': audio,
                                                           'chapter': chapter,
                                                           'uid': uid, 'max':max,'state':state,
                                                           'ccomment':ccomment,'acomment':acomment,
                                                       'amax':amax,'astate':astate,
                                                           'cmax':cmax,'file':file,
                                                       'atcount':atcount})

    if request.method == 'POST':
        chapterId = request.POST.get('cid')
        uid = request.POST.get('uid')
        audioid = request.POST.get('audioid')
        file = Audio.objects.get(id=audioid)


        max = ChapterthumbsUp.objects.filter(chapterid=chapterId).count()
        ccomment = Ccomment.objects.filter(chapterid=chapterId)
        chapter = Chapter.objects.get(id=chapterId)
        cmax = ccomment.count()
        state = '未点赞'
        if ChapterthumbsUp.objects.filter(chapterid=chapterId, userid=uid).exists():
            state = '已点赞'
        audio = Audio.objects.all().order_by("id")
        atcount = Audiothumbsup.objects.count() # 音频点赞量
        acomment = Acomment.objects.filter(audioid=file.id)
        amax = acomment.count() # 音频评论量
        astate = '未点赞'
        if Audiothumbsup.objects.filter(worksid=file.id, userid=uid).exists():
            astate = '已点赞'
        return render(request, 'chapterReading.html', {'audios': audio,
                                                           'chapter': chapter,
                                                           'uid': uid, 'max':max,'state':state,
                                                           'ccomment':ccomment,'acomment':acomment,
                                                       'amax':amax,'astate':astate,
                                                           'cmax':cmax,'file':file,
                                                       'atcount':atcount})

# Upload File with ModelForm
def upload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        chapterId = request.POST.get('chapterId')
        uid = request.POST.get('uid')
        aid = request.POST.get('aid')
        myFile = request.FILES.get("myfile")  # 获取上传的文件，如果没有文件，则默认为None
        repath = ''
        if not aid:
            repath = '/chapter?chapterId=' + chapterId + '&uid=' + uid
        else:
            repath = '/play?cid=' + chapterId + '&uid=' + uid+'&audioid='+aid
        if not myFile:
            messages.error(request,"请先选择mp3文件")

            return redirect(repath)
        path = os.path.join(dir_path, myFile.name)
        destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print(chapterId)
        obj = User.objects.get(id=uid)
        chapter = Chapter.objects.get(id=int(chapterId))
        Audio.objects.create(userid=obj, content=myFile.name, chapterid=chapter, time=now())

        messages.success(request, "发布成功")
        return redirect(repath)

def showchapterthumbs(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        cid=request.POST.get('cid')

        aid = request.POST.get('aid')
        if not aid:
            repath = '/chapter?chapterId=' + cid + '&uid=' + uid
        else:
            repath = '/play?cid=' + cid + '&uid=' + uid+'&audioid='+aid
        print(uid,cid)
        chapter = Chapter.objects.get(id=cid)
        user = User.objects.get(id=uid)
        if ChapterthumbsUp.objects.filter(chapterid=chapter.id, userid=user.id).exists():
            messages.error(request,"不要重复点赞")
        else:
            ChapterthumbsUp.objects.create(userid=user,chapterid=chapter)
        return redirect(repath)


def ccomment(request):
    if request.method == 'POST':
        comment=request.POST.get('ccommentcontent')
        uid = request.POST.get('uid')
        cid=request.POST.get('cid')
        print(uid,cid)

        aid = request.POST.get('aid')
        if not aid:
            repath = '/chapter?chapterId=' + cid + '&uid=' + uid
        else:
            repath = '/play?cid=' + cid + '&uid=' + uid+'&audioid='+aid
        chapter = Chapter.objects.get(id=cid)
        user = User.objects.get(id=uid)

        Ccomment.objects.create(chapterid=chapter,userid=user,content=comment,time=now())

        return redirect(repath)
def acomment(request):
    if request.method == 'POST':
        acomment=request.POST.get('acommentcontent')
        uid = request.POST.get('uid')
        aid = request.POST.get('aid')
        user = User.objects.get(id = uid)
        audio = Audio.objects.get(id=aid)
        print(user.id)
        Acomment.objects.create(userid=user, audioid=audio,content=acomment)
        cid = audio.chapterid.id
        return redirect('/play?cid=' + str(cid) + '&uid=' + uid+'&audioid='+aid)

def showaudiothumbs(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        aid = request.POST.get('aid')
        user = User.objects.get(id=uid)
        audio = Audio.objects.get(id=aid)
        cid =audio.chapterid.id
        if Audiothumbsup.objects.filter(worksid=aid, userid=user.id).exists():
            messages.error(request,"请勿重复点赞")
        else:
            Audiothumbsup.objects.create(worksid=audio,userid=user)
        print(cid)

        return redirect('/play?cid=' + str(cid) + '&uid=' + uid+'&audioid='+aid)


def login(request):
    if request.method == "POST":
        userInfo = User.objects.all()
        userName = request.POST.get("username")
        passWord = request.POST.get("password")

        for i in range(len(userInfo)):
            if (userName == userInfo[i].username and passWord == userInfo[i].password):
                request.session['userid'] = userInfo[i].id
                request.session['username'] = userInfo[i].username
                request.session['password'] = userInfo[i].password
                request.session['personalsignature'] = userInfo[i].personalsignature
                return redirect("/main")
        messages.error(request,"用户名或密码不正确")
        return render(request, 'login.html')
    return render(request, 'login.html')

def adminlogin(request):
    if request.method == "POST":
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        if Admonistrators.objects.filter(username=userName,password=passWord).exists():
            return redirect("/feedback")
        messages.error(request,"用户名或密码不正确")
        return render(request, 'adminlogin.html')
    return render(request, 'adminlogin.html')

def showAll(request):
    # 测试向网页发送字符串
    # return HttpResponse("Hello world");
    # 查询所有数据库学生表的信息
    feedbacks = Feedback.objects.all()
    count = feedbacks.__len__()
    # 返回网页地址并携带学生数据
    return render(request, "feedback.html", context={"feedbacks": feedbacks, "count": count})
def addfeedback(request):
    if request.method == "POST":
        content=request.POST.get('content')
        uid = request.POST.get('uid')
        aid = request.POST.get('aid')
        user = User.objects.get(id = uid)
        audio = Audio.objects.get(id=aid)
        print(content)
        Feedback.objects.create(userid=user, audioid=audio,content=content,state=0)
        cid = audio.chapterid.id
        messages.success(request,'谢谢反馈')
        return redirect('/play?cid=' + str(cid) + '&uid=' + uid+'&audioid='+aid)

def deleteAudio(request):
    # 获取需要删除的学生对象的sid
    delete_sid=request.GET['delete_sid']
    # 先查找单个对象，然后进行删除
    Audio.objects.get(id=delete_sid).delete()
    # 删除之后，重定向到首页
    return redirect("feedback.html")

def register(request):
    if request.method == "POST":
        ids = User.objects.all()
        id = 10000000 + len(ids)
        userID = str(id)
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        if(len(userName)>20):
            massage = "请输入20字以内的用户名"
            return render(request, "register.html", {'massage': massage})

        User.objects.create(
            id=userID,
            username=userName,
            password=passWord
        )
        return redirect("/login")
    return render(request, "register.html")

def main(request):

    if request.method == "POST":
        search_book = request.POST.get("search")
        # 从数据库读入内容，存入数组中
        books = Book.objects.all()
        for booki in range(len(books)):
            if(search_book == books[booki].bookname):
                request.session['search_book'] = books[booki].bookname
                request.session['search_author'] = books[booki].author
                request.session['search_introduction'] = books[booki].introduction
                return redirect("/search")
    if request.method == "GET":
        # 从数据库读入内容，存入数组中
        books = Book.objects.all()
        chapters = Chapter.objects.all()
        chapterthumbs_ups = ChapterthumbsUp.objects.all()
        audios = Audio.objects.all()
        audiothumbs_ups = Audiothumbsup.objects.all()

        booksname = []
        booksauthor = []
        booksintroduction = []
        booksid = []
        chapterid = []
        books_thumbup_num = []
        audios_thumbup_num = []
        chapter_sort = []
        book_sort = []
        print(books)
        # 读出每本书的书名
        #for i in range(len(books)):
        #    booksname.append(books[i].bookname)
        # 计算每本书章节内容的总点赞数
        for booki in range(len(books)):
            book_thumbup_num = 0

            audio_thumbup_num = 0
            # 寻找在该书中的章节
            for chapteri in range(len(chapters)):
                if (chapters[chapteri].bookid.bookid == books[booki].bookid):
                    # 寻找每个章节的点赞，若是该章节的点赞，则对该书的点赞数加1
                    for chapterthumbs_upi in range(len(chapterthumbs_ups)):
                        if (chapterthumbs_ups[chapterthumbs_upi].chapterid.id == chapters[chapteri].id):
                            book_thumbup_num += 1
                    # 寻找该章节的配音作品
                    for audioi in range(len(audios)):
                        if (audios[audioi].chapterid.id == chapters[chapteri].id):
                            # 寻找该配音作品的点赞数
                            for audiothumbs_upi in range(len(audiothumbs_ups)):
                                if (audiothumbs_ups[audiothumbs_upi].worksid.id == audios[audioi].id):
                                    audio_thumbup_num += 1
                    audios_thumbup_num.append(audio_thumbup_num)
                    book_sort.append(books[booki].bookname)
                    chapter_sort.append(chapters[chapteri].cname)
                    chapterid.append(chapters[chapteri].id)
            # 将该书的书名和点赞数存入数组
            books_thumbup_num.append(book_thumbup_num)

        # 将书名按照点赞数顺序存入数组
        for booksi in range(len(books)):
            booksname.append(books[booksi].bookname)
            booksauthor.append(books[booksi].author)
            booksintroduction.append(books[booksi].introduction)
            booksid.append(books[booksi].bookid)

        print(books_thumbup_num, booksname, booksauthor, booksintroduction, booksid)
        booksSort = list(zip(books_thumbup_num, booksname, booksauthor, booksintroduction, booksid))
        audiosSort = list(zip(audios_thumbup_num, book_sort, chapter_sort, booksauthor, booksintroduction,chapterid))
        print(booksSort)
        booksSort.sort(key=lambda x: x[0], reverse=True)
        audiosSort.sort(key=lambda x: x[0], reverse=True)

        username = request.session['username']
        personalsignature = request.session['personalsignature']
        uid = request.session['userid']
        return render(request, "main.html", {'booksSort': booksSort, 'audiosSort': audiosSort,
                                            'uid':uid,'username': username, 'personalsignature': personalsignature})


def search(request):
    if request.method == "POST":
        books = Book.objects.all()
        search_book = request.POST.get("search")
        for booki in range(len(books)):
            if(search_book == books[booki].bookname):
                request.session['search_book'] = books[booki].bookname
                request.session['search_author'] = books[booki].author
                request.session['search_introduction'] = books[booki].introduction
                return render(request, "search.html")
    return render(request, "search.html")

def personal(request):

    if request.method == "POST":
        request.session['username'] = request.POST.get("username")
        request.session['personalsignature'] = request.POST.get("personalsignature")
        users = User.objects.all()
        for useri in range(len(users)):
            if users[useri].id == request.session["userid"]:
                users[useri].username = request.session['username']
                users[useri].personalsignature = request.session['personalsignature']
                users[useri].save()
    print('1234')
    username = request.session['username']
    userid = request.session['userid']
    personalsignature = request.session['personalsignature']

    books = Book.objects.all()
    chapters =Chapter.objects.all()
    chapterthumbs_ups = ChapterthumbsUp.objects.all()
    audios =Audio.objects.all()
    audiothumbs_ups = Audiothumbsup.objects.all()

    chaptersthumbup = []
    bookchapters = []
    audiosthumbup = []
    bookaudios = []
    publishaudios = []
    publishbooks = []
    # 计算每本书章节内容的总点赞数
    for booki in range(len(books)):
        # 寻找在该书中的章节
        for chapteri in range(len(chapters)):
            if (chapters[chapteri].bookid.bookid == books[booki].bookid):
                    # 寻找每个章节的点赞，若是该章节的点赞，则对该书的点赞数加1
                for chapterthumbs_upi in range(len(chapterthumbs_ups)):
                    if (chapterthumbs_ups[chapterthumbs_upi].chapterid.id == chapters[chapteri].id and chapterthumbs_ups[chapterthumbs_upi].userid.id == userid):
                            chaptersthumbup.append(books[booki].bookname)
                            bookchapters.append(chapters[chapteri].cname)
                    # 寻找该章节的配音作品
                for audioi in range(len(audios)):
                    if (audios[audioi].chapterid.id == chapters[chapteri].id):
                        if(audios[audioi].userid.id == userid):
                                publishaudios.append(chapters[chapteri].cname)
                                publishbooks.append(books[booki].bookname)
                            # 寻找该配音作品的点赞数
                    for audiothumbs_upi in range(len(audiothumbs_ups)):
                        if (audiothumbs_ups[audiothumbs_upi].worksid.id == audios[audioi].id and audiothumbs_ups[audiothumbs_upi].userid.id == userid):
                                        audiosthumbup.append(books[booki].bookname)
                                        bookaudios.append(chapters[chapteri].cname)

    chapter = list(zip(chaptersthumbup,bookchapters))
    audio = list(zip(audiosthumbup,bookaudios))
    publish = list(zip(publishbooks,publishaudios))
    return render(request, "personal.html", {'username':username,'personalsignature':personalsignature,
                                                 'publish':publish,'chapter':chapter,'audio':audio})


def book(request):
    if request.method == "GET":
        bookid = request.GET['bid']
        chapter = Chapter.objects.filter(bookid=bookid)
        userid = request.session['userid']

        book1 = Book.objects.get(bookid = bookid)
        bookname = book1.bookname
        bookauthor = book1.author
        bookintroduction = book1.introduction

        return render(request,'first.html',context={'bookauthor': bookauthor,
                                                   'bookname':bookname,
                                                   'bookintroduction':bookintroduction,
                                                   'chapter': chapter,
                                                   'uid':userid})
