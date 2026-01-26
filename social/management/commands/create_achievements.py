from django.core.management.base import BaseCommand
from social.models import Achievement


class Command(BaseCommand):
    help = 'Crea gli achievement predefiniti nel database'

    def handle(self, *args, **kwargs):
        achievements = [
            {
                'name': 'first_post',
                'description': 'Hai pubblicato il tuo primo post!',
                'icon': '🎉',
                'points': 10
            },
            {
                'name': 'ten_posts',
                'description': 'Hai raggiunto 10 post pubblicati!',
                'icon': '📝',
                'points': 25
            },
            {
                'name': 'hundred_posts',
                'description': 'Incredibile! 100 post pubblicati!',
                'icon': '💯',
                'points': 100
            },
            {
                'name': 'first_follower',
                'description': 'Qualcuno ha iniziato a seguirti!',
                'icon': '👥',
                'points': 10
            },
            {
                'name': 'fifty_followers',
                'description': 'Hai raggiunto 50 follower!',
                'icon': '⭐',
                'points': 50
            },
            {
                'name': 'hundred_followers',
                'description': 'Sei popolare! 100 follower!',
                'icon': '🌟',
                'points': 100
            },
            {
                'name': 'popular_post',
                'description': 'Un tuo post ha ottenuto 100+ reazioni!',
                'icon': '🔥',
                'points': 75
            },
            {
                'name': 'active_week',
                'description': 'Hai effettuato il login per 7 giorni consecutivi!',
                'icon': '📅',
                'points': 30
            },
            {
                'name': 'social_butterfly',
                'description': 'Hai scritto 100 commenti!',
                'icon': '🦋',
                'points': 50
            },
            {
                'name': 'influencer',
                'description': 'Sei un influencer! 1000 follower!',
                'icon': '👑',
                'points': 500
            },
        ]

        created_count = 0
        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults={
                    'description': achievement_data['description'],
                    'icon': achievement_data['icon'],
                    'points': achievement_data['points']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creato: {achievement.icon} {achievement.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Già esistente: {achievement.icon} {achievement.get_name_display()}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Processo completato! {created_count} nuovi achievement creati.')
        )
