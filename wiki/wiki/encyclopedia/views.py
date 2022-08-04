from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
import random

from . import util

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        query = request.POST['q'].strip()

        page_text = util.get_entry(query)

        if page_text:
            return HttpResponseRedirect(f"/wiki/{query}")
        
        results = [entry for entry in entries if query.lower() in entry.lower()]

        return render(request, "encyclopedia/search.html", {
            "results" : results
        })


    return render(request, "encyclopedia/index.html", {
        "entries": entries,
    })

def entry(request, title):
    entries = util.list_entries()
    lowered_entries = list(map(str.lower, entries))
    if title not in entries and title not in lowered_entries:
        message = "Page Not Found: 404"
        return render(request, "encyclopedia/error.html", {
            "message" : message,
        })

    md = util.get_entry(title)
    page_text = markdown2.markdown(md)

    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "page_text" : page_text,
    })

def add(request):
    entries = util.list_entries()
    lowered_entries = list(map(str.lower, entries))
    if request.method == "POST":
        title = request.POST['title']
        page_text = request.POST['page_text']

        if title.lower() in lowered_entries:
            message = "Page Already Exists: 403"
            return render(request, "encyclopedia/error.html", {
                "message" : message,
                "random_page": random.choice(entries)
            })

        with open(f"entries/{title}.md", "w") as fh:
            fh.write(page_text)

        return HttpResponseRedirect(f"/wiki/{title}")        

    return render(request, "encyclopedia/add.html", {
    })

def edit(request, title):
    if request.method == "POST":
        page_text = request.POST['page_text']

        with open(f"entries/{title}.md", "w") as fh:
            fh.write(page_text.strip())
        
        return HttpResponseRedirect(f"/wiki/{title}")

    page_text = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "page_text": page_text,
        "title": title,
    })

def random_entry(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{entry}")