from django.shortcuts import render, redirect
from . import util
from django.http import HttpResponseRedirect, HttpResponse
import markdown2
from django import forms
from django.urls import reverse
import random
from random import choice



class NewEntry(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Title',
        'id' : 'new-entry-title'
    }))

    data = forms.CharField(label='', widget=forms.Textarea(attrs={
        'id' : 'new-entry'
    }))

class NewEdit(forms.Form):
    content = forms.CharField(label ='', widget=forms.Textarea)
    




def search(request):
    query = request.GET.get('q')
    subquery = []
    if query in util.list_entries():
        return HttpResponseRedirect('wiki/'+query)
    else:
        all_entries = util.list_entries()
        for sub in all_entries:
            a = str(query).lower()
            b = str(sub).lower()
            if (b.find(a) != -1):
                subquery.append(sub)
        if len(subquery) == 0:
            return render(request, 'encyclopedia/error.html')
        else:
            return render(request, 'encyclopedia/found.html',{
                "entry" : subquery
    })




def main_page(request):
    return render(request, 'encyclopedia/main_page.html',{
        "entries":util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, 'encyclopedia/error.html') 
    else:
        return render(request, 'encyclopedia/entry.html',{
            "entry": markdown2.markdown(entry),
            "title": title
        })

def create(request):
    if request.method == 'POST':
        created_entry = NewEntry(request.POST)
        if created_entry.is_valid():
            title = created_entry.cleaned_data['title']
            data = created_entry.cleaned_data['data']
            entries_all = util.list_entries()
            for entry in entries_all:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/create.html", {
                       
                        "newentry": NewEntry(),
                        "error": "That entry already exists!"
                    })
            new_entry_title = '> ' + title 
            new_entry_data = '\n' + data 

            new_entry_content = new_entry_title + new_entry_data 
            util.save_entry(title ,new_entry_content)
            entry = util.get_entry(title)
            return render(request, 'encyclopedia/entry.html',{
                "title":title,
                "entry":markdown2.markdown(entry),
                "newentry":NewEntry()
            })
    return render(request, 'encyclopedia/create.html', {
        'newentry' : NewEntry()
    }) 

  
def edit(request, title):
    if request.method == "GET":
        initial = {"content" : util.get_entry(title)}
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : NewEdit(initial=initial)
        })
    else:
        form = NewEdit(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(f'/{title}')


def random_choice(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry = util.get_entry(title)
    return HttpResponseRedirect(reverse('entry', args=[title]))



    
