from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
nextId = 4
topics = [
  {'id':1,'title':'routing','body':'Routing is ..'},
  {'id':2,'title':'view','body':'View is ..'},
  {'id':3,'title':'Model','body':'Model is ..'}
]

def HTMLTemplate(articleTag, id=None):
  global topics
  contextUI = ''
  if id != None:
    contextUI = f'''
      <li>
        <form action='/account/delete/' method='post'>
          <input type="hidden" name='id' value={id}>
          <input type="submit" value='delete'>
        </form>
      </li>
      <li><a href="/account/update/{id}">update</a></li>
    '''
  ol = ''
  for topic in topics:
    ol += f'<li><a href="/account/read/{topic["id"]}">{topic["title"]}</a></li>'
  return f'''
  <html>
  <body>
    <h1><a href="/account">Django</a></h1>
    <ul>
      {ol}
    </ul>
    {articleTag}
    <ul>
      <li><a href="/account/create/">create</a></li>
      {contextUI}
    </ul>
  </body>
  </html>
  '''

def index(request):
  article = '''
  <h2>Welcome</h2>
  Hello, Django'''
  return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
  global nextId

  # create 버튼을 눌렀을 때
  if request.method == 'GET':
    # <form method='post'> --> submit버튼을 누를 시 post로 전송됨
    article = '''
    <form action="/account/create/" method="post"> 
      <p><input type="text" name="title" placeholder="title"></p>
      <p><textarea name='body' placeholder="body"></textarea></p>
      <p><input type="submit"></p>
    </form>
    '''
    return HttpResponse(HTMLTemplate(article))

  # 제출 버튼을 눌렀을 때
  elif request.method == 'POST':
    title = request.POST['title']
    body = request.POST['body']
    newTopic = {'id':nextId,'title':title,'body':body}
    nextId += 1
    topics.append(newTopic)
    return redirect(f'/account/read/{nextId-1}')


def read(request, id):
  global topics
  article = ''
  for topic in topics:
    if topic['id'] == int(id):
      article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    
  # for topic in topics:
  #   if topic['id'] == int(id):
  #     article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
  return HttpResponse(HTMLTemplate(article, id))


@csrf_exempt
def update(request, id):
  global topics
  if request.method == 'GET':
    for topic in topics:
      if topic['id'] == int(id):
        selectedTopic = {
          'title':topic['title'],
          'body':topic['body'],
        }
    article = f'''
    <form action="/account/update/{id}/" method="post">
      <p><input type="text" name="title" placeholder="title" value={selectedTopic['title']}></p>
      <p><textarea name='body' placeholder="body">{selectedTopic['body']}</textarea></p>
      <p><input type="submit"></p>
    </form>
    '''
    return HttpResponse(HTMLTemplate(article, id))

  elif request.method == 'POST':
    title = request.POST['title']
    body = request.POST['body']
    for topic in topics:
      if topic['id'] == int(id):
        topic['title'] = title
        topic['body'] = body
    return redirect(f'/account/read/{id}')


@csrf_exempt
def delete(request):
  global topics
  if request.method == 'POST':
    id = request.POST['id']
    newTopics = []
    for topic in topics:
      if topic['id'] != int(id):
        newTopics.append(topic)
    topics = newTopics
    return redirect('/account/')
