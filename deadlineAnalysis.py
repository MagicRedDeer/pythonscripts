import site
site.addsitedir(r'D:\talha.ahmed\workspace\pyenv_maya')
site.addsitedir(r'D:\talha.ahmed\workspace\pyenv_common')
site.addsitedir(r'D:\talha.ahmed\workspace\pyenv_maya\tactic')
import ideadline
import datetime


def parsetime(datestring):
    return datetime.datetime.strptime(datestring, '%b %d/%y  %H:%M:%S')


def tasktime(task):
    try:
        return datetime.datetime.strptime(task['TaskTime'].split('.')[0], '%H:%M:%S') - datetime.datetime(1900, 1, 1, 0)
    except:
        return datetime.timedelta()

readItems = ideadline.deadlineWrapper.getItemsFromOutput

def gettask(jobid):
    return readItems(ideadline.deadlineCommand('GetJobTasks', jobid['JobId']))

def gettasksbyjobs(jobs):
    return [gettask(job) for job in jobs]

def minstart(jobs):
    return parsetime(min(jobs,
        key=lambda x: datetime.datetime.strptime(x['JobStartedDateTime'], '%b %d/%y %H:%M:%S')
        )['JobStartedDateTime'])

def maxend(jobs):
    return parsetime(max(jobs,
        key=lambda x: datetime.datetime.strptime(x['JobCompletedDateTime'], '%b %d/%y %H:%M:%S')
        )['JobCompletedDateTime'])

def numframes(job):
    return len(job['Frames'].split(','))

def printdata(name, jobs, jobtasks, minstart, maxend, tasks, taskdeltas,
        totaltasktime):
    print '\n======\n'
    print name
    print 'first job started: ', minstart.strftime('%Y-%m-%d %H:%M:%S')
    print 'last job finished:', maxend.strftime('%Y-%m-%d %H:%M:%S')
    print 'time elapsed', maxend - minstart
    print 'total number of frames', sum([numframes(job) for job in jobs])
    print 'number of jobs', len(jobs)
    print 'number of tasks', len(tasks)
    print 'task time', totaltasktime
    print '\n======\n'

class A:

    def __init__(self):
        pass


if __name__ == '__main__':
    pass

alljobs = ideadline.getJobs()

ep23name = 'ep23'
ep23jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
    'EP023_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
        'Jan 01/01.*')], match_any=False)
ep23jobtasks = gettasksbyjobs(ep23jobs)
ep23minstart = minstart(ep23jobs)
ep23maxend = maxend(ep23jobs)
ep23tasks = reduce(lambda x, y: x+y, ep23jobtasks, [])
ep23taskdeltas = [tasktime(task) for task in ep23tasks]
totaltasktime_ep23 = sum(ep23taskdeltas, datetime.timedelta())

printdata(ep23name, ep23jobs, ep23jobtasks, ep23minstart, ep23maxend,
        ep23tasks, ep23taskdeltas, totaltasktime_ep23)

if False:

    ep19name = 'ep19'
    ep19jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
        'EP019_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
            'Jan 01/01.*')], match_any=False)
    ep19jobtasks = gettasksbyjobs(ep19jobs)
    ep19minstart = minstart(ep19jobs)
    ep19maxend = maxend(ep19jobs)
    ep19tasks = reduce(lambda x, y: x+y, ep19jobtasks, [])
    ep19taskdeltas = [tasktime(task) for task in ep19tasks]
    totaltasktime_ep19 = sum(ep19taskdeltas, datetime.timedelta())

    ep22name = 'ep22'
    ep22jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
        'EP022_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
            'Jan 01/01  00:00:00')], match_any=False)
    ep22jobtasks = gettasksbyjobs(ep22jobs)
    ep22minstart = minstart(ep22jobs)
    ep22maxend = maxend(ep22jobs)
    ep22tasks = reduce(lambda x, y: x+y, ep22jobtasks, [])
    ep22taskdeltas = [tasktime(task) for task in ep22tasks]
    totaltasktime_ep22 = sum(ep22taskdeltas, datetime.timedelta())


    printdata(ep19name, ep19jobs, ep19jobtasks, ep19minstart, ep19maxend,
            ep19tasks, ep19taskdeltas, totaltasktime_ep19)
    printdata(ep22name, ep22jobs, ep22jobtasks, ep22minstart, ep22maxend,
            ep22tasks, ep22taskdeltas, totaltasktime_ep22)

    ep14name = 'ep14'
    ep14jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
        'EP014_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
            'Jan 01/01  00:00:00')], match_any=False)
    ep14jobtasks = gettasksbyjobs(ep14jobs)
    ep14minstart = minstart(ep14jobs)
    ep14maxend = maxend(ep14jobs)
    ep14tasks = reduce(lambda x, y: x+y, ep14jobtasks, [])
    ep14taskdeltas = [tasktime(task) for task in ep14tasks]
    totaltasktime_ep14 = sum(ep14taskdeltas, datetime.timedelta())


    ep20name = 'ep20'
    ep20jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
        'EP020_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
            'Jan 01/01  00:00:00')], match_any=False)
    ep20jobtasks = gettasksbyjobs(ep20jobs)
    ep20minstart = minstart(ep20jobs)
    ep20maxend = maxend(ep20jobs)
    ep20tasks = reduce(lambda x, y: x+y, ep20jobtasks, [])
    ep20taskdeltas = [tasktime(task) for task in ep20tasks]
    totaltasktime_ep20 = sum(ep20taskdeltas, datetime.timedelta())


    ep17name = 'ep17'
    ep17jobs = ideadline.filterItems(alljobs, filters=[('JobName', 'contains',
        'EP017_SQ'), ('Status', 'Completed'), ('JobStartedDateTime', 'not matches',
            'Jan 01/01  00:00:00')], match_any=False)
    ep17jobtasks = gettasksbyjobs(ep17jobs)
    ep17minstart = minstart(ep17jobs)
    ep17maxend = maxend(ep17jobs)
    ep17tasks = reduce(lambda x, y: x+y, ep17jobtasks, [])
    ep17taskdeltas = [tasktime(task) for task in ep17tasks]
    totaltasktime_ep17 = sum(ep17taskdeltas, datetime.timedelta())

    printdata(ep14name, ep14jobs, ep14jobtasks, ep14minstart, ep14maxend,
            ep14tasks, ep14taskdeltas, totaltasktime_ep14)
    printdata(ep20name, ep20jobs, ep20jobtasks, ep20minstart, ep20maxend,
            ep20tasks, ep20taskdeltas, totaltasktime_ep20)
    printdata(ep17name, ep17jobs, ep17jobtasks, ep17minstart, ep17maxend,
            ep17tasks, ep17taskdeltas, totaltasktime_ep17)
