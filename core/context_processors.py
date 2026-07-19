from .models import Profile

def global_variables(request):
    profile = Profile.objects.first()
    return {
        'site_profile': profile,
    }
