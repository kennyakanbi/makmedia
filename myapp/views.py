from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from myapp.models import Contact, Blog, Internship
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import re
from .models import Blog
from django.db.models import F, Q

def home(request):
    return render(request, 'home.html')


def blog_list(request):
    """
    Display a list of all blog posts.
    """
    posts = Blog.objects.all().order_by('-created_at')  # latest first
    return render(request, "blog_list.html", {"posts": posts})



def blog_detail(request, slug):
    """
    Display a single blog post with paragraphs and extra images.
    Robust: works if related name is 'extra_images' or the default 'blogimage_set'.
    """
    post = get_object_or_404(Blog, slug=slug)

    # --- Process content paragraphs ---
    raw_content = post.content or ""
    raw_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', raw_content, flags=re.DOTALL)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw_content) if p.strip()]
    if not paragraphs:
        paragraphs = [p.strip() for p in raw_content.splitlines() if p.strip()]

    # --- Get extra images robustly ---
    extra_images = []
    if hasattr(post, "extra_images"):
        try:
            extra_images = list(post.extra_images.all())
        except Exception:
            extra_images = []
    else:
        try:
            extra_images = list(post.blogimage_set.all())
        except Exception:
            extra_images = []

    # --- Determine positions for images ---
    content_blocks = []
    n_par = len(paragraphs)
    n_img = len(extra_images)
    insert_after = []
    if n_img > 0 and n_par > 0:
        for i in range(n_img):
            pos = round((i + 1) * n_par / (n_img + 1))
            pos = max(1, min(n_par, pos))
            insert_after.append(pos)

    # Build blocks: paragraphs and inline image blocks
    img_index = 0
    for i, para in enumerate(paragraphs, start=1):
        content_blocks.append({"type": "p", "text": para})
        while img_index < n_img and insert_after and insert_after[img_index] == i:
            img_obj = extra_images[img_index]
            image_url = getattr(img_obj.image, "url", None) if img_obj else None
            if image_url:
                content_blocks.append({"type": "img", "image_url": image_url})
            img_index += 1

    while img_index < n_img:
        img_obj = extra_images[img_index]
        image_url = getattr(img_obj.image, "url", None) if img_obj else None
        if image_url:
            content_blocks.append({"type": "img", "image_url": image_url})
        img_index += 1

    # --- Recent posts ---
    recent_posts = Blog.objects.exclude(pk=post.pk).order_by('-created_at')[:5]

    # --- Previous and Next posts ---
    prev_post = Blog.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()
    next_post = Blog.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()

    return render(request, "blog_detail.html", {
        "post": post,
        "content_blocks": content_blocks,
        "recent_posts": recent_posts,
        "prev_post": prev_post,
        "next_post": next_post,
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

