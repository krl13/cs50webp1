from django.shortcuts import render, redirect
from . import util
from random import choice
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    # Pronađi tačan naslov iz liste, bez obzira na velika/mala slova
    correct_title = next((entry for entry in entries if entry.lower() == title.lower()), None)
    content = markdown(util.get_entry(correct_title))

    if correct_title:
        return render(request, "encyclopedia/entry.html", {
            "entry": content,
            "entries": entries,
            "title": correct_title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist"
        })
    
def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    exact_match = next((entry for entry in entries if entry.lower() == query.lower()), None)
    if exact_match:
        return redirect('entry', title=exact_match)
    
    suggestions = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "suggestions": suggestions
    })

def new_page(request):
    return render(request, "encyclopedia/new_page.html")

def add(request):
    if request.method == "POST":
        content = request.POST.get("new_page", "")


        title = util.get_title_from_markdown(content)
        entries = util.list_entries()

        if title == None:
            return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist"
        })

        if title in entries:
            return render(request, "encyclopedia/already_exists.html", {
                "message": "This page already exists"
            })
        
        util.save_entry(title, content)

        return redirect("entry", title=title)
    
    return redirect("new_page")

def edit_page(request, title):
    content = util.get_entry(title)
    

    return render(request, "encyclopedia/edit_page.html", {
         "content": content
     })
    
def edit(request):
    if request.method == "POST":
        content = request.POST.get("edit_page", "")


        title = util.get_title_from_markdown(content)
        entries = util.list_entries()

        if title == None:
            return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist"
        })

        
        
        util.save_entry(title, content)

        return redirect("entry", title=title)
    
    return redirect("edit_page")

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect('entry', title=entry)
