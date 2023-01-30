

 **

## FromWebToExeTool

**
**DESCRIPTION:**

This tool is needed for converting any website from web to desktop app.
Finally you get zip file - which including all dependency files and file for execution.
Supported output platform is WINDOWS, LINUX, MAC  | arch=x64
App running over Nativefier: [source code](https://github.com/nativefier/nativefier)
____________________

**FIRST STEPS** **INSTALL DEPENDENCIES**:


1. For using this tool you need to [install step-by-step](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) docker and pull image from dockerhub :

    **docker pull nativefier/nativefier**

2.  Or you can use npm for install  (of course npm was been installed):

    **npm install -g nativefier**

3. Wine is needed for  generating windows exe on linux: 

    **sudo apt-get install wine-stable**

4.  You need to install **requirements.txt**

_____________________________________________

**[USAGE IN DJANGO]**

1. Copy exemaker.py file to your project app folder.
2. Need create instance of class :

`   
maker=ExeMaker(url="https://translate.google.com/",os_type="linux",convert_mode="docker",config=None)
`

views.py

    def handler(request):
	
	    if request.method == "POST":
			url = request.POST.get('url')
			os_choices = request.POST.get('os_choices')

			if url and os_choices:

				maker=ExeMaker(
                                url=url,
                                os_type=os_choices,
                                convert_mode="docker",# or npm
								)
				
				return maker.django_response()

        return render(request, 'index.html')

