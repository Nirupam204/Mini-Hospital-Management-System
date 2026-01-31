#Blocks from opening others dashboard


from django.http import HttpResponseForbidden


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_doctor():
            return HttpResponseForbidden("Doctor access only")
        return view_func(request, *args, **kwargs)

    return wrapper


def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_patient():
            return HttpResponseForbidden("Patient access only")
        return view_func(request, *args, **kwargs)

    return wrapper
