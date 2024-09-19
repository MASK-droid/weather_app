from django.shortcuts import render , HttpResponse
from django.contrib import messages
import requests
import datetime

# Create your views here.
api_key = 'ea9510f1b0cc6f97eb18cad39531219c'

def home(request):
    city = 'kasaragod'
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
        if not city:
            city = 'kasaragod'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    PARAMS = {'units' : 'metric'}

    API_KEY = 'AIzaSyALc_kJGuFhpL7bx6O0l9La6gPWApFj2mA'
    SERACH_ENGINE_ID = 'a56711fd332814328'

    query = city
    page = 1
    start = (page-1)*10+1
    searchType = 'image'
    
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SERACH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items",[])
    # image_url = search_items[1]['link']
    # print(image_url)
    print(search_items)
    
    # image_url = search_items[1]['link']
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']
        print(image_url)
    else:
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
        print("No sufficient search results found.")
  
    try:
        data = requests.get(url,PARAMS).json()
        # print(data)
        print(data)
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()
        res = {
            'description': description,
            'icon'       : icon,
            'temp' : temp,
            'day': day ,
            'city':city,
            'exception_occurred':False,
            'image_url':image_url,
        }
        messages.success(request,'Your Request is Successfull')
        return render(request,'base/index.html',res)
    
    except:
        exception_occurred = True
        messages.error(request,'entered data is not available to API')
        day = datetime.date.today()
        res = {
            'description': 'clear sky',
            'icon'       : '01d',
            'temp' : 25,
            'day': day ,
            'city':city,
            'exception_occurred':exception_occurred,
        }
        return render(request,'base/index.html',res)