**[DESCRIPTION]**

This tool is needed for converting any website from web to desktop app.


This tool is needed for converting any website from web to desktop app.

Finally you get zip file - which including all dependency files and file for execution.

Supported output platform is WINDOWS, LINUX, MAC  | arch=x64.   

App based on Nativefier: [source code](https://github.com/nativefier/nativefier)


**[INSTALL]**

```
git clone https://github.com/ImranRahimov1995/FromWebToExeTool.git
cd FromWebToExeTool

# The first you need to install dependecies[Nodejs,Docker,Npm,Nativefier] use script:

. ./exemaker.sh

# After setup your environment

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


**[USAGE]**

```
from src.exemaker import ExeMaker

BASE_DIR = str(Path(__file__).resolve().parent.parent)


settings = Settings(
    nativefier_dir=os.path.join(BASE_DIR, 'nativefier-apps'),
    zip_dir=os.path.join(BASE_DIR, 'zips'),
)

maker = ExeMaker(
    url="https://translate.google.com/", # any website link
    os_type="linux", # "windows/mac/linux"
    convert_mode="npm", # you can use npm or docker.
    config=settings, # If use django is not needed , you can pass
)

filepath = maker.get_zip_filepath() # Zip file
response = maker.django_response() # Django response for return in view

```

**[USAGE IN DJANGO]**

in settings.py
```
HOME_DIR = os.path.expanduser('~')
NATIVEFIER_DIR = BASE_DIR / 'nativefier-apps/'
ZIP_DIR = BASE_DIR / 'zips/'
```
Create app, Create url, create template, create view .
Copy exemaker.py in your app and import in view ExeMaker class.
```
def handler(request):
    if request.method == "POST":
        # This is might be form .
        url = request.POST.get('url')
        os_choices = request.POST.get('os_choices')

        if url and os_choices:
            maker = ExeMaker(url=url, # https://github.com/
                             os_type=os_choices, # "windows/mac/linux"
                             convert_mode='npm') # you can use npm or docker.

            return maker.django_response()

    return render(request, 'index.html')


```



**[NOTES]**

Don't forget test for any platform. 
Nativefier must adapt and download all files for platforms.

**[TEST]**

`pytest -s src/test.py`


