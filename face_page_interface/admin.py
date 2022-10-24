from xml.etree.ElementTree import Comment
from django.contrib import admin

from face_page_interface.models import CustomUser, Post, CommentModel

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(CommentModel)