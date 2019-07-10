from django.shortcuts import render,get_object_or_404,reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (CreateView,
                                    ListView,
                                    DetailView,
                                    RedirectView
                                    )
from .. models import Collection


class ListCollections(LoginRequiredMixin,ListView):
    model = Collection

    def get_queryset(self):
        return self.request.user.collections.all()

class CollectionDetail(LoginRequiredMixin,DetailView):
    model  = Collection

    def get_queryset(self):
        return self.request.user.collections.all()


class Create(LoginRequiredMixin,CreateView):
    # template_name='my_bookmarks/collection_form.html'
    fields = ('name',)
    model = Collection
    # success_url = reverse_lazy('collection:all-collections')

    def form_valid(self,form):
        print(self.request.POST)
        collection= form.save(commit=False)
        collection.user = self.request.user
        collection.save()
        return super().form_valid(form)
