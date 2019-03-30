def logged_user(request):
    if request.user.is_authenticated:
        logged = request.user.username
        return {'logged': logged}
    else:
        return {'logged': 'You are not a registered user'}

