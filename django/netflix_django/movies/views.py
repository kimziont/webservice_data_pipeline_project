from pytz import timezone
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from script.my_favorite import recommend




def index(request):
    return render(request, 'movies/index.html')

def moviePlay(request, id):
    time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    print("영상을 재생중 입니다")
    with open('/opt/netflix/logs/netflix.log', 'a') as f:
        f.write(f'[{time}] method={request.method} user={request.user} path={request.path} movie_id={id}\n')
    return render(request, 'movies/play.html')
    


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    ordering = ['-release_date']
    paginate_by = 8 # page 객체 page_obj로 전달
    page_kwarg = 'page' # url 안에서 적용되는 키워드

class FavoriteMovieListView(ListView):
    model = Movie
    template_name = 'movies/my_favorite_movie_list.html'
    ordering = ['-release_date']
    paginate_by = 20 # page 객체 page_obj로 전달
    page_kwarg = 'page' # url 안에서 적용되는 키워드

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_filter'] = recommend(self.request.user)
        context['user'] = self.request.user
        return context


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'
    context_object_name = 'form'

    def get_success_url(self):
        print("포스팅 성공")
        print(self.object.id)
        return reverse('movie-detail', kwargs={'movie_id': self.object.id})


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'movies/comment_form.html'
    context_object_name = 'form'
    
    # 유저 id를 자동 주입하기 위해 추가 
    # https://stackoverflow.com/questions/65733442/in-django-how-to-add-username-to-a-model-automatically-when-the-form-is-submit
    def form_valid(self, form):
        result = self.request.POST
        form = CommentForm(result)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = self.request.user
            task_list.save()

            # 로그 
            time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
            with open('/opt/netflix/logs/netflix.log', 'a') as f:
                f.write(f'[{time}] method={self.request.method} user={self.request.user} path={self.request.path} movie_id={result.get("movie")}\n')
            return redirect('movie-list')

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    pk_url_kwarg = 'movie_id'
    context_object_name = 'object'