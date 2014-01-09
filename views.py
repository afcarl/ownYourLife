from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from ownYourLife.models import Category, Entry

class IndexView(generic.ListView):
    model = Entry
    template_name = 'ownYourLife/index.html'
    context_object_name = 'model'

    def get_queryset(self):
        """Return the last five recorded entries."""
        return Entry.objects.all() #order_by('-timestamp')[:5]

class AddView(generic.DetailView):
    model = Entry
    template_name = 'ownYourLife/add.html'

class EntryDetailView(generic.DetailView):
    model = Entry
    template_name = 'ownYourLife/detail.html'

def buildCategoryTree(l):
    """ builds a tree of categories using dictionaries """
    # 1. Find all the leaf nodes
    # 2. Find all the children's names
    # 3. For each child, recurse
    tree = dict()
    children = dict()
    for (s, c) in l:
        if '/' in s: # if there's at least one more level
            parts = s.partition('/')
            head = parts[0]
            tail = parts[2]
            if head not in children:
                children[head] = [(tail, c)]
            else:
                children[head].append((tail, c))
        else: # this is a leaf node
            tree[s] = c

    for child in children:
        tree[child] = buildCategoryTree(children[child])

    return tree 

def flattenCategoryTree(catTree, label='main', title='main', subIdx=0):
    """ 
    From the category tree, flatten it to generate panels of buttons
    suitable as a quick user interface

    +- a +- 1
    |    |
    |    +- 2
    |    |
    |    +- 3
    |
    +- b
    |
    +- c +- d
         |
         +- e +- 4
         |    |
         |    +- 5
         |
         +- f
    
    will become a list of

    main: (a->sub1, b, c->sub2)
    sub1: (1, 2, 3)
    sub2: (d, e->sub3, f)
    sub3: (4, 5)
    """
    # Each hashtable becomes a tuple via recursion (depth-first)
    panels = [] # outer list that contains each panel tuple
    currentLevel = [] # items in this level in the tree

    for key in catTree:
        if type(catTree[key]) == dict:
            slabel = 'sub' + str(subIdx)
            subIdx += 1
            innerPanels, subIdx = flattenCategoryTree(catTree[key], key, slabel, subIdx)
            panels.extend(innerPanels)
            currentLevel.append((key, slabel, None))
        else:
            currentLevel.append((key, None, catTree[key]))

    panels.append((label, title, currentLevel))

    # returns
    #   1. panels that can be recursively extended
    #   2. global index that increased due to sub-sub-trees and what not
    return panels, subIdx

def tree(request):
    """ grab all the categories and build a tree """
    try:
        cats = list(Category.objects.order_by('name')) # get them all in memory
    except Category.DoesNotExist:
        raise Http404

    l = []
    for c in cats:
        l.append((c.name, c))

    catTree = buildCategoryTree(l)
    
    panels, __ = flattenCategoryTree(catTree)

    return render(request, 'ownYourLife/tree.html', {'cats': cats, 'panels': panels})
