# Подключение нужных библиотек
from datetime import datetime
import requests
import plotly.graph_objects as go
from jinja2 import Template

# Данные и токен для использования
Name = ''
Group = ''
taigaPjName = ''
taigaUsername = ''
mEmail = ''
eEmail = ''
token = ''

# Получение текущей даты и времени
currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Проверка относится ли даты date1 и date2 к одной неделе
def checkweek(date1, date2):
    week1 = datetime.strptime(date1, '%Y-%m-%d').isocalendar().week
    week2 = datetime.strptime(date2, '%Y-%m-%d').isocalendar().week
    if week1 == week2:
        return True
    else:
        return False


# Получение данных из Zulip
def getZulipData(email, usertoken):
    body = {
        "studEmail": email,
        "beginDate": "2022-01-01",
        "endDate": "2022-03-31",
        "timeRange": 1,
        "token": usertoken
    }

    # Получение ответа на POST запрос на API зулипа и сохранение его в виде JSON
    r = requests.post('http://94.79.54.21:3000/api/zulip/getaigainfo', json=body).json()

    # Получение общего кол-ва сообщений и списка комнат
    rooms = []
    ids = []
    messagescount = 0
    for message in r['messages']:
        messagescount += 1
        if message['stream_name'] not in ids:
            rooms.append(message['stream_name'] + ', ')
            ids.append(message['stream_name'])

    # Получение кол-ва сообщений по дням
    days = []
    messages = []
    for day in r['stats']:
        days.append(day['beginDate'][:15])
        messages.append(day['messageCount'])

    # Построение графиков
    linegraph = go.Figure([go.Scatter(x=days, y=messages)]).to_html()
    barchart = go.Figure([go.Bar(x=days, y=messages)]).to_html()

    return messagescount, rooms, linegraph, barchart


# Получение данных из Jitsi
def getJitsiData(email1, usertoken):
    body = {
        "studEmail": email1,
        "beginDate": "2021-09-01",
        "endDate": "2022-03-31",
        "beginTime": "09:00:00.000",
        "endTime": "21:00:00.000",
        "token": usertoken
    }

    r = requests.post('http://94.79.54.21:3000/api/jitsi/sessions', json=body).json()

    sessioncount = len(r)  # Получение общего кол-ва посещенных занятий

    rooms = []
    pssessions = []
    pssessionsdays = []
    weeks = ['2022-01-01', '2022-01-08', '2022-01-15', '2022-01-22', '2022-01-29', '2022-02-05', '2022-02-12',
             '2022-02-19', '2022-02-26', '2022-03-05', '2022-03-12', '2022-03-19', '2022-03-26']
    sessions = []
    for session in r:
        if session['room'] not in rooms:  # Получение списка посещенных комнат
            rooms.append(session['room'])

            # Посещение занятий по проектному семинару по дням
        if (session['room'] == 'ps1' or session['room'] == 'ps') and (session['date'] not in pssessionsdays):
            pssessions.append('1')
            pssessionsdays.append(session['date'])
    rooms = ", ".join(rooms)

    for week in weeks:  # Посещение занятий по неделям
        counter = 0
        for session in r:
            if checkweek(session['date'], week):
                counter += 1
        sessions.append(counter)

    pslinegraph = go.Figure([go.Scatter(x=pssessionsdays, y=pssessions)]).to_html()

    linegraph = go.Figure([go.Scatter(x=weeks, y=sessions)]).to_html()
    barchart = go.Figure([go.Bar(x=weeks, y=sessions)]).to_html()

    return sessioncount, linegraph, barchart, rooms


# Получение данных из GitLab
def getGitlabData(email, usertoken):
    body = {
        "studEmail": email,
        "beginDate": "2022-01-01",
        "endDate": "2022-04-28",
        "hideMerge": True,
        "token": usertoken
    }

    r = requests.post('http://94.79.54.21:3000/api/git/getaigainfoPerWeek', json=body).json()

    commitcount = 'no data'

    for project in r['projects']:  # Получение кол-ва коммитов в репозитории проекта
        if project['name'] == taigaPjName:
            commitcount = project['commitCount']

    weeks = []
    commits = []
    for week in r['commits_stats']:
        weeks.append(week['beginDate'][:15])
        commits.append(week['commitCount'])

    barchart = go.Figure([go.Bar(x=weeks, y=commits)]).to_html()
    linegraph = go.Figure([go.Scatter(x=weeks, y=commits)]).to_html()

    return commitcount,linegraph, barchart


# Получение данных из Taiga
def getTaigaData():
    epicid = 0

    # Получение id эпика
    header = {"x-disable-pagination": "true"}
    userstoryr = requests.get('https://track.miem.hse.ru/api/v1/userstories',
                                     headers=header, timeout=None).json()
    for us in userstoryr:
        if (us['project_extra_info']['name'] == 'Проектный семинар БИВ21X') and \
                (us['owner_extra_info']['username'] == taigaUsername):
            epicid = us['epics'][0]['id']

    # Получение кол-ва юзерстори в эпике и их id
    url = 'https://track.miem.hse.ru/api/v1/epics/' + str(epicid) + '/related_userstories'
    userstories = requests.get(url, timeout=None).json()
    uscount = len(userstories)
    usidlist = []

    for us in userstories:
        usidlist.append(us['user_story'])

    # Получение общего кол-ва задач и по неделям
    date = []
    taskcount = 0
    tasks = []
    taskr = requests.get("https://track.miem.hse.ru/api/v1/tasks", headers=header, timeout=None).json()
    for task in taskr:
        if task['user_story_extra_info'] is not None and task['user_story_extra_info']['id'] in usidlist:
            taskcount += 1
            date.append(task['created_date'])
            tasks.append(taskcount)

    linegraph = go.Figure([go.Scatter(x=date, y=tasks)]).to_html()

    return uscount, taskcount, linegraph


if __name__ == '__main__':
    templatePath = 'templates/base.html'
    pagePath = 'outputpage.html'

    gitData = getGitlabData(eEmail, token)
    taigaData = getTaigaData()
    zulipData = getZulipData(mEmail, token)
    jitsiData = getJitsiData(eEmail, token)

    params = {'creationTime': currentDate,
              'name': Name,
              'group': Group,
              'gitlab_commits_count': gitData[0],
              'gitlab_graph_line': gitData[1],
              'gitlab_graph_bar': gitData[2],

              'taiga_userstories_count': taigaData[0],
              'taiga_tasks_count': taigaData[1],
              'taiga_graph': taigaData[2],

              'zulip_messages_count': zulipData[0],
              'zulip_chanels': zulipData[1],
              'zulip_messages_graph_line': zulipData[2],
              'zulip_messages_graph_bar': zulipData[3],

              'jitsi_meetings_count': jitsiData[0],
              'jitsi_meetings_graph_line': jitsiData[1],
              'jitsi_meetings_graph_bar': jitsiData[2],
              'jitsi_visited_rooms': jitsiData[3]
              }

    template = Template(open(templatePath, 'r', encoding="utf-8").read())

    # Рендер итоговой страницы
    with open(pagePath, "w+", encoding="utf-8") as htmlPage:
        htmlPage.write(template.render(params))