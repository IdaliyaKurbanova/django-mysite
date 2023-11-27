from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def file_upload(request: HttpRequest) -> HttpResponse:
  context = {}
  if request.method == "POST" and request.FILES.get("myfile"):
    file_to_upload = request.FILES.get("myfile")
    try:
      if file_to_upload.size <= 1048576:
        fs = FileSystemStorage()
        saved_file_name = fs.save(file_to_upload.name, file_to_upload)
        print(f'File {saved_file_name!r} was successfully saved')
        context['saved_file_name'] = saved_file_name
      else:
        message_for_user = 'File was not saved!  Limit for file size - 1 Mb'
        context['message_for_user'] = message_for_user
        raise BaseException
    except BaseException:
      print(f"FileSizeError was occured during saving file {file_to_upload.name}!!!")
  return render(request, "requestdataapp/file-upload.html", context=context)

