from django.http import Http404
from django.shortcuts import render, redirect

from .forms import TopicForm, EntryForm
from .models import Topic


def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # if topic.owner != request.user:
    #     raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context ={'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':  # Veri gönderilmedi; boş form oluştur
        form = TopicForm()
    else:                         # POST verisi gönderildi, veriyi işle.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # boş veya geçersiz formu görüntüle.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)