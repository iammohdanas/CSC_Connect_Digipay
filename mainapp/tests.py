from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

def logout_user(request):
    if request.method == 'GET':
        logout(request)
        # print("CSC Id",request.session.get('csc_Id'))
        return render(request, 'login.html', {'logged_out': True})
    else:
        return HttpResponse('Invalid request method', status=404)
    
