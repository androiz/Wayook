from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q

from chatWayook.forms import ChatForm
from chatWayook.models import Chat, Message


class Home(TemplateView):
    template_name = "home.html"

    def get(self, request):
        context = {
            'users': User.objects.all()
        }
        return render(request, template_name=self.template_name, context=context)

class UserView(TemplateView):
    template_name = "userView.html"

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        users = list(User.objects.all().exclude(pk=user.id))

        users_chats = dict()
        for u in users:
            try:
                chat = Chat.objects.get(Q(user1=user, user2=u) | Q(user1=u, user2=user))
            except Chat.DoesNotExist:
                chat = None
            users_chats[u] = chat

        users_with_chat = dict((x, users_chats[x]) for x in users_chats if users_chats[x])
        users_without_chat = [x for x in users_chats if not users_chats[x]]

        context = {
            'user_id': user_id,
            'users_chat': users_chats,
            'users_with_chat': users_with_chat,
            'users_without_chat': users_without_chat
        }

        return render(request, template_name=self.template_name, context=context)

class ChatView(TemplateView):
    template_name = "chatView.html"

    def get(self, request, user_id, chat_id):
        user = User.objects.get(pk=user_id)
        chat = Chat.objects.get(pk=chat_id)

        messages = Message.objects.filter(chat=chat)
        print messages

        form = ChatForm()

        context = {
            'user': user,
            'chat': chat,
            'messages': messages,
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request, user_id, chat_id):
        m = request.POST.get('message', "")
        chat = Chat.objects.get(pk=chat_id)
        user = User.objects.get(pk=user_id)
        message = Message.objects.create(chat=chat, user=user, message=m)

        return redirect("/" + user_id + "/" + chat_id)

def createChatView(request, user_id, user2_id):
        user1 = User.objects.get(pk=user_id)
        user2 = User.objects.get(pk=user2_id)
        chat = Chat.objects.create(user1=user1, user2=user2)
        return redirect("/" + user_id + "/" + str(chat.id))