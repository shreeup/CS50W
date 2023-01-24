from django.shortcuts import render
import pdb;
from . import util
from django import forms
from django.http import HttpResponseRedirect,HttpResponseNotFound,Http404
from django.urls import reverse
from random import randint

class NewEntryForm(forms.Form):
    messages=[]
    entrytitle = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    entrydesc = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detailview(request,vname):
    page=util.get_entry(vname)
    return render(request, "encyclopedia/detailview.html",{
        "title":vname,
        "content":page
    })
def update(request,name):
    #pdb.set_trace()
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            entrytitle = form.cleaned_data["entrytitle"]
            entrydesc = form.cleaned_data["entrydesc"]
            util.save_entry(title=entrytitle,content=entrydesc)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/update.html", {
                "form": form
            })  
    else:
        title = name
        content = util.get_entry(title)
        form = NewEntryForm({"entrytitle": title, "entrydesc": content})
        form.fields["entrytitle"].label=title
        return render(
            request,
            "encyclopedia/update.html",
            {"form": form, "title": title},
        )   

def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        raise Http404 
    
    entries = util.list_entries()
    
    if entries!=None:
        found_entries = [
            valid_entry
            for valid_entry in entries
            if query.lower() in valid_entry.lower()
        ]
        if found_entries!=None and len(found_entries)>0:
            return render(request, "encyclopedia/index.html", {"entries": found_entries})
        else:
            raise Http404
    else:
        raise Http404  

def random(request): 
    entries = util.list_entries()
    entry=entries[randint(0, len(entries) - 1)]
    url = reverse('detailview', kwargs={'vname': entry})
    return HttpResponseRedirect(url)

def add(request):
    
    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            entrytitle = form.cleaned_data["entrytitle"]
            entrydesc = form.cleaned_data["entrydesc"]

            # Add the new task to our list of tasks
            #tasks.append(task)

            if entrytitle.lower() in [entry.lower() for entry in util.list_entries()]:
                
                #form.messages.append("This page already exits.")
                return render(request, "encyclopedia/new.html", {
                    "messages":["This page already exits."],
                    "form": form
                })
            else:
                with open(f"entries/{entrytitle}.md", "w") as file1:
                # Writing data to a file
                    file1.write(entrydesc)
                return HttpResponseRedirect(reverse("index"))
            

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })


# def handler404(request, *args):
#     #pdb.set_trace()
#     return render(request, "404.html", {})