from django.shortcuts import render

def index(request):
    # позже сюда можно передавать любые данные: ссылки на бота, тексты и т.п.
    context = {
        'bot_link': 'https://t.me/bobwinchester_1',
        'headline': 'Добро пожаловать! Получите консультацию в Telegram',
        'description': 'Нажмите кнопку ниже, чтобы начать диалог с нашим AI-ассистентом'
    }
    return render(request, 'index.html', context)


def lifestyle(request):
    return render(request, "home-lifestyle-blog.html")