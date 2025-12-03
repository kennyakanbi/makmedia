from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from myapp.models import Contact, Blog, Internship
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import re
from .models import Blog

def home(request):
    return render(request, 'home.html')

def blog_list(request):
    posts = Blog.objects.all()
    return render(request, "blog_list.html", {"posts": posts})


from django.shortcuts import render, get_object_or_404
import re

def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)

    # raw content
    raw = post.content or ""

    # OPTIONAL: convert **bold** → <strong> (if you want inline bold markers)
    raw = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', raw, flags=re.DOTALL)

    # split paragraphs by blank line (author separates with blank line)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw) if p.strip()]
    if not paragraphs:
        paragraphs = [p.strip() for p in raw.splitlines() if p.strip()]

    # get extra images safely (use try/except in case relation missing)
    try:
        extra_images = list(post.extra_images.all())
    except Exception:
        extra_images = []

    n_par = len(paragraphs)
    n_img = len(extra_images)

    # compute positions after which to insert images (1-based)
    insert_after = []
    if n_img > 0 and n_par > 0:
        # spread images evenly: positions are 1..n_par
        for i in range(n_img):
            pos = round((i + 1) * n_par / (n_img + 1))
            pos = max(1, min(n_par, pos))
            insert_after.append(pos)

    # build content_blocks list (ordered)
    content_blocks = []
    img_i = 0
    for i, para in enumerate(paragraphs, start=1):
        content_blocks.append({"type": "p", "text": para})
        while img_i < n_img and insert_after and insert_after[img_i] == i:
            content_blocks.append({"type": "img", "image": extra_images[img_i]})
            img_i += 1

    while img_i < n_img:
        content_blocks.append({"type": "img", "image": extra_images[img_i]})
        img_i += 1

    # DEBUG: temporarily print so you can see ordering in console
    print("DEBUG: content_blocks:", [(b["type"], (b.get("text")[:30] if b["type"]=="p" else getattr(b["image"], 'image', None))) for b in content_blocks])

    return render(request, "blog_detail.html", {
        "post": post,
        "content_blocks": content_blocks,
    })


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




    
