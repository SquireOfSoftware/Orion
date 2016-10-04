from django.http import HttpResponse
from django.http import JsonResponse
import json

def test(request):
    response = HttpResponse(json.dumps({"name":"Test"}));

    response["Access-Control-Allow-Origin"] = "*";
    #response["Access-Control-Allow-Credentials"] = "false";
    response['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept";
    response['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE";
    response['Access-Control-Allow-Max-Age'] = "3600";
    response['Method'] = "POST";
    #response['Content-Type'] = 'application/json';
    return response;

def page(request):
    page = (open("/Users/JarvisWalker/Documents/Git/Orion/web-gui/htdocs/index.html"));
    print(page);
    return page;