from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                CreateView,
                                DeleteView,
                                DetailView,
                                UpdateView,
                                View,RedirectView
                                )
from functools import reduce
import operator
from django.db.models import Q
from .. models import Bookmark,Collection
from django.utils import timezone
from taggit.managers import TaggableManager

class Search(LoginRequiredMixin,ListView):
    model = Bookmark

    def get_queryset(self):
        qs = Bookmark.objects.current(self.request.user)
        words = self.request.GET.get('q')
        #Kennoth solution # SQL all  AND)
        # q_objects = (
        #         Q(title__icontains = word)|Q(description__icontains=word)
        #         for word in words.split()
        #     )
        # print(q_objects)
        # return = qs.filter(*[q for q in q_objects]) # SQL all  AND)
        # my solution: #  SQL all  OR)
        if words:
            query_list = words.split()
            result = qs.filter(
                reduce(operator.or_,
                       (Q(title__icontains=word) for word in query_list)) |
                reduce(operator.or_,
                       (Q(description__icontains=word) for word in query_list))
            )
            return result



class ListBookmarks(LoginRequiredMixin,ListView):
    model = Bookmark

    def get_queryset(self):
        """
        objects which are NOT "soft-deleted" AND belong to the particular user
        """
        qs = Bookmark.objects.current(self.request.user)
        print(self.kwargs)
        tag = self.kwargs.get('tag')
        if tag:
            qs = qs.filter(tags__name__in=[tag])
        return qs
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['list'] = True
        return context

class CreateBookmark(LoginRequiredMixin,CreateView):
    model = Bookmark
    fields = ['title','url','description','tags']
    success_url = reverse_lazy('my_bookmarks:list')

    def form_valid(self,form):
        bookmark = form.save(commit=False)
        bookmark.user = self.request.user
        bookmark.save()
        form.save_m2m()
        return super().form_valid(form)

class UpdateBookmark(LoginRequiredMixin,UpdateView):
    model = Bookmark
    fields = ['title','url','description','tags']
    success_url = reverse_lazy('my_bookmarks:list')

    def get_queryset(self):
        # otherwise search for an object will be in whole qs
        # inclusive other users
        return Bookmark.objects.current(self.request.user)


class  SoftDeleteBookmark(LoginRequiredMixin,UpdateView):
    """
    class replaces ordinary DeleteView
    instead due to new field(deleted_at) obj can be updated
    """
    fields =()
    model = Bookmark
    # built-in ==> template_name_suffix = 'bookmark_confirm_delete'
    template_name = 'my_bookmarks/soft_delete.html'
    success_url = reverse_lazy('my_bookmarks:list')

    def get_queryset(self):
        # otherwise search for an object will be in whole qs
        # inclusive other users
        return self.request.user.bookmarks.filter(deleted_at__isnull=True)
    def form_valid(self,form):
        bookmark = form.save(commit=False)
        bookmark.deleted_at = timezone.now()
        bookmark.save()
        return super().form_valid(form)





class Trash(LoginRequiredMixin,ListView):
    model = Bookmark
    def get_queryset(self):
        return Bookmark.objects.deleted(self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['trash'] = True
        return context

class Restore(LoginRequiredMixin,RedirectView):
    url = reverse_lazy('my_bookmarks:list')
    def get_object(self):
        return get_object_or_404(
                        Bookmark,
                        user=self.request.user,
                        pk=self.kwargs.get('pk'),
                        deleted_at__isnull=False
                        )
    def get(self,request,*args,**kwargs):
        obj = self.get_object()
        obj.deleted_at = None
        obj.save()
        return super().get(request,*args,**kwargs)

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['restore'] = True
    #     return context

class FinalTrash(LoginRequiredMixin,DeleteView):
    model = Bookmark
    template_name = 'my_bookmarks/final_delete.html'
    success_url = reverse_lazy('my_bookmarks:list')

    def get_queryset(self):
        return Bookmark.objects.deleted(self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['final_del'] = True
        return context


class AddBookmarkToCollection(LoginRequiredMixin,RedirectView):
    """
    стоя в bookmark detail,добавляю её в коллецию through slug;
    let op: RedirectView doesn't have .get_object()
    """
    def get_bookmark(self,request):
        pk = request.GET.get('bookmark')
        print(pk,'pk is')
        bookmark = get_object_or_404(Bookmark,
                            user= self.request.user,
                            id=pk)
        return bookmark
        # bookmark.bm_collect.add(collection)
    def get_collection(self,request):
        slug = self.request.GET.get('collection')
        print('slug is:',slug)
        collection = get_object_or_404(Collection,user=self.request.user,slug=slug)
        return collection
    def get(self,request,*args,**kwargs):
        self.bookmark = self.get_bookmark(request)
        self.collection = self.get_collection(request)
        self.bookmark.collections.add(self.collection)
        return super().get(request,*args,**kwargs)
    def get_redirect_url(self,*args,**kwargs):
        """
        redirect to the same collection after adding a bookmark
        """
        return self.collection.get_absolute_url()


# class AddBookmarkToCollection(LoginRequiredMixin,RedirectView):
#     """
#     стоя в bookmark detail,добавляю её в коллецию through slug;
#     let op: RedirectView doesn't have .get_object()
#     """
#     def get_redirect_url(self,*args,**kwargs):
#         """
#         redirect to the same collection after adding a bookmark
#         """
#         collection = self.get_collection()
#         return collection.get_absolute_url()
#
#     def get_bookmark(self):
#         pk = self.kwargs.get('pk')
#         bookmark = get_object_or_404(Bookmark,user= self.request.user,pk=pk)
#         return bookmark
#         # bookmark.bm_collect.add(collection)
#     def get_collection(self):
#         slug = self.kwargs.get('slug')
#         collection = get_object_or_404(Collection,user=self.request.user,slug=slug)
#         return collection
#     def get(self,*args,**kwargs):
#         bookmark = self.get_bookmark()
#         bookmark.collections.add(self.get_collection())
#         return super().get(*args,**kwargs)
