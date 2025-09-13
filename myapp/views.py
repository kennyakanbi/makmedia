from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from myapp.models import Contact, Blog, Internship
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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


@login_required(login_url="/auth/login/")
def internshipdetails(request):
    if request.method == "POST":
        # pull + sanitize
        fname       = (request.POST.get("name") or "").strip().upper()
        femail      = (request.POST.get("email") or "").strip().lower()
        fusn        = (request.POST.get("usn") or "").strip().upper()
        fcollege    = (request.POST.get("cname") or "").strip().upper()
        foffer      = (request.POST.get("offer") or "").strip().upper()
        fstartdate  = (request.POST.get("startdate") or "").strip() or None
        fenddate    = (request.POST.get("enddate") or "").strip() or None
        fprojreport = (request.POST.get("projreport") or "").strip().upper()


        # simple duplicate check
        if Internship.objects.filter(usn=fusn).exists() or Internship.objects.filter(email=femail).exists():
            messages.warning(request, "Your details are already stored.")
            return redirect(reverse("intern"))  # your URL name
        Internship.objects.create(
            fullname=fname,
            usn=fusn,
            email=femail,
            college_name=fcollege,
            offer_status=foffer,
            start_date=fstartdate,
            end_date=fenddate,
            proj_report=fprojreport,
        )

        messages.success(request, "Form submitted successfully.")
        return redirect(reverse("intern"))

    # GET -> render form
    return render(request, "intern.html")

 
def contact(request):
    if request.method == "POST":
        fname = request.POST.get('name') 
        femail = request.POST.get('email')
        fmessage = request.POST.get('message')   # ✅ fixed
        fphoneno = request.POST.get('phone')

        query = Contact(name=fname, email=femail, phone=fphoneno, message=fmessage)
        query.save()
        messages.success(request, "Thanks for contacting us! We’ll get back to you soon.")
        return redirect('/contact')
    return render(request, 'contact.html')




    
