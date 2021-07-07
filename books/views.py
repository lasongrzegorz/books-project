from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django_filters.views import FilterView

import django_filters

from books.models import Books


class MainPageView(TemplateView):
    template_name = "main.html"


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="iexact")
    author = django_filters.CharFilter(lookup_expr="iexact")
    language = django_filters.CharFilter(lookup_expr="iexact")
    published__gt = django_filters.DateFilter(
        field_name="published",
        lookup_expr="gt",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Published after",
    )
    published__lt = django_filters.DateFilter(
        field_name="published",
        lookup_expr="lt",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Published before",
    )

    class Meta:
        model = Books
        fields = ["title", "author", "language", "published__gt", "published__lt"]


class ListBookView(FilterView):
    model = Books
    template_name = "books_list.html"
    context_object_name = "books"
    filterset_class = BookFilter
    paginate_by = 20


class BookCreateUpdateForm(forms.ModelForm):
    published = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Books
        fields = "__all__"


class CreateBookView(CreateView):
    model = Books
    template_name = "book_create.html"
    form_class = BookCreateUpdateForm
    success_url = reverse_lazy("book-list")


class UpdateBookView(UpdateView):
    model = Books
    success_url = reverse_lazy("book-list")
    template_name = "book_update.html"
    form_class = BookCreateUpdateForm


class DeleteBookView(DeleteView):
    model = Books
    success_url = reverse_lazy("book-list")
