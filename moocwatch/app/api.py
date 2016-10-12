import json
import urllib
import sys
from app import models

providers = {'udacity':'https://udacity.com/public-api/v0/courses',
             'coursera':'https://api.coursera.org/api/courses.v1',
             'edx':'https://courses.edx.org/api/courses/v1/courses/',
             'udemy':'https://udemy.com/api-2.0/courses/?is_paid=False&include_spam=False',
}

headers = {
    'udemy': {'Authorization': 'Basic Q0lhTHFha2VXbnppUW9ESWx0ZGdNUXpZQ25Pbm93Sno2c0k3MnM3QTpUOWZhNW8xTktFd0ZSQmtyaXhDOXEyY0VrVllrcUJ6Mk42azNtQ1hwQmpCMVpKZkZCR3Zrd29lRjk2eDdWeVBWUGlYRFB4VmEyaXFicVdiVUxmdW9ZRVo5aXBZT1NqaU5QMWZxZWZPNUM3ZWNtSjY4Y0thTkRuM1R3V3cyUVVhUg==',
    }
}

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

isascii = lambda s: len(s) == len(s.encode())

def makeApiReq(provider):
    if provider == providers['udemy']:
        response = urllib.request.urlopen(urllib.request.Request(provider, headers = headers['udemy'], method='GET')).read().decode('utf8')
        print(response)
    else:
        response = urllib.request.urlopen(provider).read().decode("utf8")
    json_response = json.loads(response)
    if urllib.parse.urlsplit(provider).netloc == urllib.parse.urlsplit(providers['udacity']).netloc:
        if 'courses' in json_response:
            for courses in json_response['courses']:
                url = courses['homepage']
                course = courses['title']
                image = courses['image']
                description = courses['summary']
                provider = 'udacity'
                addEntry(url, course, image, description, provider)
            return True
    elif urllib.parse.urlsplit(provider).netloc == urllib.parse.urlsplit(providers['edx']).netloc:
        if 'results' in json_response:
            for courses in json_response['results']:
                course = courses['name']
                if checkCourse(course):
                    url = urllib.parse.quote_plus("https://www.edx.org/course?search_query=" + course + ' ' + courses['org'], safe=':=?&/').encode('utf8')
                    image = courses['media']['image']['small']                    
                    description = ''
                    provider = 'edx'
                    print(url)
                    addEntry(url, course, image, description, provider)
                else:
                    print("Do not add")
            return True
    elif urllib.parse.urlsplit(provider).netloc == urllib.parse.urlsplit(providers['coursera']).netloc:
        if 'elements' in json_response:
            for courses in json_response['elements']:
                course = courses['name']
                if checkCourse(course):
                    slug = courses['slug']
                    url = urllib.parse.quote_plus("https://www.coursera.org/learn/" + slug, safe=':=?&/').encode('utf8')
                    image = ''
                    description = ''
                    provider = 'coursera'
                    addEntry(url, course, image, description, provider)
                else:
                    print("Do not add")
            return True
    elif urllib.parse.urlsplit(provider).netloc == urllib.parse.urlsplit(providers['udemy']).netloc:
        if 'results' in json_response:
            for courses in json_response['results']:
                if courses['_class'] == 'course':
                    course = courses['title']
                    if checkCourse(course):
                        url = urllib.parse.quote_plus("https://www.udemy.com" + courses['url'], safe=':=?&/').encode('utf8')
                        image = courses['image_480x270']                    
                        description = ''
                        provider = 'udemy'
                        uprint(url)
                        addEntry(url, course, image, description, provider)
                    else:
                        print("Do not add")
            return True
    return False

def checkCourse(course):
    if isascii(course):
        lowcourse = course.lower()
        if lowcourse.rfind(' test') or lowcourse.rfind(' demo') or lowcourse.rfind('demo ') or lowcourse.rfind('test ') or lowcourse.startswith('delete') or lowcourse.startswith('deprecated') or lowcourse.startswith('obsolete') or lowcourse.startswith('null') or lowcourse.startswith('void') or lowcourse.startswith('old') or lowcourse.startswith('course outdated') or lowcourse.startswith('outdated') or lowcourse.startswith('(abandoned)'):
            return False
        else:
            return True
    return False

def addEntry(url, course, image, description, provider):
    all_entries = models.Course.objects.all()
    if not all_entries.filter(url=url):
        uprint(str(isinstance(course, str)) + "Adding %s " % course)
        course = models.Course(url=url,
                                course=course,
                                image=image,
                                description=description,
                                provider=provider)
        course.save()
    else:             
        uprint("Course %s already added" % course)


edxlink = providers['edx'] + '?page='

count = 1

#while True:
#    str1 = str(edxlink + str(count))
#    print(str1)
#    bool = makeApiReq(str1)
#    count += 1
#    if bool == False:
#        break

# makeApiReq(providers['udemy'])