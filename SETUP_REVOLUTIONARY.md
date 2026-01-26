# 🚀 Setup Funzionalità Rivoluzionarie

## 📦 Installazione

### 1. Esegui le Migrazioni

```bash
# Crea le migrazioni per i nuovi modelli
python manage.py makemigrations

# Applica le migrazioni
python manage.py migrate
```

### 2. Crea gli Achievement Predefiniti

```bash
# Popola il database con gli achievement
python manage.py create_achievements
```

Questo comando creerà automaticamente tutti i 10 achievement:
- 🎉 Primo Post
- 📝 10 Post
- 💯 100 Post
- 👥 Primo Follower
- ⭐ 50 Follower
- 🌟 100 Follower
- 🔥 Post Virale (100+ reazioni)
- 📅 Attivo 7 giorni
- 🦋 100 commenti
- 👑 1000 follower

### 3. Crea le Cartelle Media per Stories e Gruppi

```bash
# Crea le cartelle necessarie
mkdir media\stories
mkdir media\stories\videos
mkdir media\groups
mkdir media\groups\covers
```

## 🎯 Nuove Funzionalità Disponibili

### ✅ Già Implementate (Backend)

1. **Stories 24h** 📸
   - Modelli: `Story`, `StoryView`
   - Scadenza automatica dopo 24 ore
   - Tracciamento visualizzazioni

2. **Reazioni Multiple** 😍🔥👏
   - Modello: `Reaction`
   - 8 tipi di reazioni diverse
   - Sostituisce/integra i like tradizionali

3. **Hashtag & Trending** #️⃣
   - Modelli: `Hashtag`, `PostHashtag`
   - Algoritmo trending basato su attività 24h
   - Auto-rilevamento hashtag nei post

4. **Achievement System** 🏆
   - Modelli: `Achievement`, `UserAchievement`
   - 10 achievement predefiniti
   - Sistema punti e notifiche WebSocket
   - Controlli automatici via signals

5. **Gruppi/Communities** 👥
   - Modelli: `Group`, `GroupMembership`, `GroupPost`
   - Gruppi pubblici e privati
   - Sistema di ruoli (Admin, Moderatore, Membro)
   - Post dedicati ai gruppi

6. **Preferenze Utente** ⚙️
   - Modello: `UserPreferences`
   - Dark mode, notifiche, lingua, privacy

## 🔧 Prossimi Passi

### Frontend da Implementare

Per rendere queste funzionalità utilizzabili, devi creare:

#### 1. **Stories UI**
- Barra stories nella navbar (cerchi colorati)
- Modal per visualizzare stories
- Form per creare nuove stories
- Swipe gesture per navigare

**Template da creare:**
- `templates/social/stories.html`
- `templates/social/create_story.html`
- `templates/social/story_viewer.html`

**Views da creare:**
- `stories_list()` - Lista stories disponibili
- `create_story()` - Crea nuova story
- `view_story()` - Visualizza story e registra view
- `delete_story()` - Elimina story

#### 2. **Reazioni UI**
- Sostituire pulsante like con selector reazioni
- Mostrare conteggio per tipo di reazione
- Animazioni al click

**Modifiche template:**
- `feed.html`, `post_detail.html`, `profile.html`
- Aggiungere popup reazioni stile Facebook

**Views da creare:**
- `react_to_post()` - Aggiungi/cambia reazione

#### 3. **Hashtag UI**
- Auto-completamento hashtag durante scrittura
- Pagina trending hashtag
- Pagina risultati per hashtag

**Template da creare:**
- `templates/social/trending.html`
- `templates/social/hashtag_posts.html`

**Views da creare:**
- `trending_hashtags()` - Top hashtag
- `hashtag_posts()` - Post per hashtag

#### 4. **Achievement UI**
- Badge sul profilo utente
- Pagina achievement utente
- Toast notification quando sblocchi
- Classifica globale

**Template da creare:**
- `templates/social/achievements.html`
- `templates/social/leaderboard.html`

**Modifiche template:**
- `profile.html` - Mostrare badge earned

#### 5. **Gruppi UI**
- Pagina lista gruppi
- Pagina dettaglio gruppo
- Form crea/modifica gruppo
- Gestione membri

**Template da creare:**
- `templates/social/groups.html`
- `templates/social/group_detail.html`
- `templates/social/create_group.html`

**Views da creare:**
- `groups_list()` - Lista gruppi
- `group_detail()` - Dettaglio gruppo
- `create_group()` - Crea gruppo
- `join_group()` - Unisciti a gruppo
- `leave_group()` - Lascia gruppo

#### 6. **Dark Mode UI**
- Toggle nella navbar
- CSS variabili per colori
- Salvataggio preferenza

**JavaScript da aggiungere:**
```javascript
function toggleDarkMode() {
    // Toggle classe dark su body
    // Salva preferenza via AJAX
    // Aggiorna CSS
}
```

## 📝 Esempio: Implementare Stories

### Step 1: Crea le Views

```python
# In social/views.py

@login_required
def stories_list(request):
    # Stories non scadute degli utenti seguiti
    following_ids = request.user.profile.following.values_list('following__user__id', flat=True)
    stories = Story.objects.filter(
        author__id__in=following_ids,
        expires_at__gt=timezone.now()
    ).select_related('author').prefetch_related('views')
    
    context = {'stories': stories}
    return render(request, 'social/stories.html', context)

@login_required
def create_story(request):
    if request.method == 'POST':
        # Gestisci upload immagine/video o testo
        story = Story.objects.create(
            author=request.user,
            image=request.FILES.get('image'),
            text_content=request.POST.get('text_content'),
            background_color=request.POST.get('background_color', '#FF69B4')
        )
        return redirect('stories_list')
    return render(request, 'social/create_story.html')

@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    # Registra visualizzazione
    StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    context = {'story': story}
    return render(request, 'social/story_viewer.html', context)
```

### Step 2: Aggiungi URL

```python
# In social/urls.py
urlpatterns = [
    # ... existing urls ...
    path('stories/', views.stories_list, name='stories_list'),
    path('stories/create/', views.create_story, name='create_story'),
    path('stories/<int:story_id>/', views.view_story, name='view_story'),
]
```

### Step 3: Crea Template

```html
<!-- templates/social/stories.html -->
{% extends 'base.html' %}

{% block content %}
<div class="stories-container">
    {% for story in stories %}
    <div class="story-circle" onclick="window.location.href='{% url 'view_story' story.id %}'">
        <img src="{{ story.author.profile.profile_picture.url }}" class="rounded-full">
        <span>{{ story.author.username }}</span>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

## 🎨 Design System

### Colori Dark Mode

```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --text-primary: #111827;
    --text-secondary: #6b7280;
    --border-color: #e5e7eb;
}

[data-theme="dark"] {
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --border-color: #374151;
}
```

### Icone Reazioni

```html
<div class="reactions-picker">
    <button data-reaction="like">❤️</button>
    <button data-reaction="love">😍</button>
    <button data-reaction="haha">😂</button>
    <button data-reaction="wow">😮</button>
    <button data-reaction="sad">😢</button>
    <button data-reaction="angry">😠</button>
    <button data-reaction="fire">🔥</button>
    <button data-reaction="clap">👏</button>
</div>
```

## 🧪 Testing

### Test Achievement System

```python
# Test in Django shell
from django.contrib.auth.models import User
from social.models import Post
from social import achievement_checker

user = User.objects.first()

# Crea primo post
post = Post.objects.create(author=user, content="Test")
# Dovrebbe sbloccare "Primo Post"

# Verifica achievement
user.user_achievements.all()
```

### Test Stories

```python
from social.models import Story
from django.utils import timezone

# Crea story
story = Story.objects.create(
    author=user,
    text_content="Test story",
    background_color="#FF69B4"
)

# Verifica scadenza
print(story.is_expired)  # False
print(story.expires_at)  # 24 ore da ora
```

## 📊 Admin Interface

Tutti i nuovi modelli sono già registrati nell'admin Django:

- **Stories** - Gestisci stories e visualizzazioni
- **Reactions** - Vedi tutte le reazioni
- **Hashtags** - Gestisci hashtag e trending
- **Achievements** - Modifica achievement
- **User Achievements** - Vedi chi ha sbloccato cosa
- **Groups** - Gestisci gruppi e membri
- **User Preferences** - Modifica preferenze utenti

Accedi su: http://localhost:8000/admin

## 🚀 Deployment

### Variabili Ambiente Aggiuntive

Aggiungi al `.env`:

```env
# Achievement notifications
ACHIEVEMENT_NOTIFICATIONS_ENABLED=True

# Stories
STORIES_DURATION_HOURS=24
MAX_STORY_SIZE_MB=10

# Groups
MAX_GROUP_MEMBERS=1000
```

### Cron Jobs

Per pulire stories scadute:

```python
# social/management/commands/cleanup_stories.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from social.models import Story

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        expired = Story.objects.filter(expires_at__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.stdout.write(f'Deleted {count} expired stories')
```

Aggiungi a crontab:
```
0 * * * * cd /path/to/project && python manage.py cleanup_stories
```

## 📱 Mobile Responsive

Tutte le funzionalità devono essere mobile-first:

- **Stories**: Swipe gesture su mobile
- **Reazioni**: Long-press per aprire picker
- **Gruppi**: Lista scrollabile
- **Achievement**: Badge compatti

## 🎯 Metriche da Monitorare

- Stories create/giorno
- Reazioni per tipo
- Hashtag più usati
- Achievement più rari
- Gruppi più attivi
- Utenti dark mode vs light mode

---

**Pronto per rivoluzionare il social networking!** 🚀
