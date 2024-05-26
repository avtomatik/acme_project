from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


def edit_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk, author=request.user)
    if instance.author != request.user:
        raise PermissionDenied


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self) -> bool | None:
        object = self.get_object()
        return object.author == self.request.user


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
