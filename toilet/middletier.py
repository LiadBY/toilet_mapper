from models import Toilet
from review.models import Review
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse


#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict(request.POST)
        print request.user.is_authenticated()
        if not request.user.is_authenticated():
            status = 401
            error += 'Unauthorized creation of restroom. Please log in.\n'
        
        else:
            t = Toilet()
            data['date'] = currentTime()
            data['creator'] = request.user
            t.setattrs(data)
            t.save()

            response = serialize([t])
    else:
        error += 'No POST data in request.\n'
        status = 415

    return HttpResponse(package_error(response,error), status=status)



def listing(request):
    response = ''
    error = ''
    status = 201

    toilet_set = Toilet.objects.all()
    review_set = Review.objects.all()

    l = []

    for t in toilet_set:
        t_rs = review_set.filter(toilet=t)
        total = 0.0
        count = len(list(t_rs))
        if count == 0:
            total = -1
        else:
            for r in t_rs:
                total += r.rank
            total /= count
        
        l.append({"t" : json.loads(serialize(t)), "ranking" : total, "count" : count})
        
    response = json.dumps(l)
    return HttpResponse(response,status=status)
