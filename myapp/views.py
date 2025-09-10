from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from myapp.models import Contact, Blog, Internship

def home(request):
    return render(request, 'home.html')

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, "blog_list.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    return render(request, "blog_detail.html", {"post": post})

def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')

def internshipdetails(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to access this page")
        return redirect('/auth/login/')

    if request.method == "POST":
       fname= request.POST.get('name') 
       femail= request.POST.get('email')
       fusn= request.POST.get('usn')
       fcollege= request.POST.get('cname')
       foffer= request.POST.get('offer')
       fstartdate= request.POST.get('startdate')
       fenddate= request.POST.get('enddate')
       fprojreport= request.POST.get('projreport')

#converting to upper case
       fname=fname.upper()
       fusn=fusn.upper()
       fcollege=fcollege.upper()
       fprojreport= fprojreport.upper()
       foffer=foffer.upper()

#
       check1=Internship.objects.filter(usn=fusn)
       check2=Internship.objects.filter(email=femail)

       if check1 or check2:
          messages.warning(request, "Your Details are Stored Already")
          return redirect("/internshipdetails")

       query= Internship(fullname=fname, usn=fusn, email=femail,
       college_name=fcollege, offer_status=foffer, start_date=fstartdate, 
       end_date=fenddate, proj_report=fprojreport)
       query.save()

       messages.success(request, "Form is Submitted Successfully")
       return redirect('/internshipdetails')
    return render(request, 'intern.html')    

 
def contact(request):
    if request.method == "POST":
        fname = request.POST.get('name') 
        femail = request.POST.get('email')
        fdesc = request.POST.get('message')   # ✅ match template
        fphoneno = request.POST.get('phone')  # if you want to add a phone field later

        query = Contact(name=fname, email=femail, description=fdesc)
        query.save()
        messages.success(request, "Thanks for contacting us! We’ll get back to you soon.")
        return redirect('/contact')
    return render(request, 'contact.html')



    
