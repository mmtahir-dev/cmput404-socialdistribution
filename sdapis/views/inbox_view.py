from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import *
from sdapis.serializers import *
from .helper import is_valid_node
from sdapis.permissions import AccessPermission, CustomAuthentication

def get_followers(author_id):
    follow = Follow.objects.filter(author1=author_id)
    serializer = FollowSerializer(follow, many=True)
    followers = []
    remote = []
    for author in serializer.data:
        follower_id = author['author2']
        try:
            follower = Author.objects.get(author_id=follower_id)
            serializer = AuthorSerializer(follower)
            followers.append(serializer.data)
        # used to connect remote nodes' authors
        except not follow.exists():
            if follower_id in remote:
                followers.append(follower)
    return followers

def get_followings(author_id):
    follow = Follow.objects.filter(author2=author_id)
    follow_serializer = FollowSerializer(follow, many=True)
    followings = []
    remote = []
    for author in follow_serializer.data:
        following_id = author['author1']
        try:
            following_author = Author.objects.get(author_id=following_id)
            author_serializer = AuthorSerializer(following_author)
            followings.append(author_serializer.data)
        # used to connect remote nodes' authors
        except not follow.exists():
            if following_id in remote: 
                followings.append(following_author)
    return followings

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def inbox_detail(request, author_id):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        obj, created = Inbox.objects.get_or_create(author_id=author_id)
        serializer = InboxSerializer(obj)
        output = serializer.data
        return Response(output)

    elif request.method == 'DELETE':
        inbox, created = Inbox.objects.get_or_create(author_id=author_id)
        if not created:
            inbox.delete()
        return Response({'message':'inbox cleared'}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        content_type = request.data['type']

        if content_type == 'follow':
            new_follower_id = request.data['new_follower_id']
            new_follower = Author.objects.get(author_id=new_follower_id)
            

            if not Follow.objects.filter(author1=author_id, author2=new_follower_id).exists():
                follow = Follow(author1=author_id, author2=new_follower_id) # let new follower follow author
                follow.save()
            author = get_object_or_404(Author, author_id=author_id)
            actor_name = new_follower.username
            object_name = author.username
            summary = actor_name + " wants to follow " + object_name
            new_follower_serialized = AuthorSerializer(new_follower).data
            author_serialized = AuthorSerializer(author).data

            inbox, _ = Inbox.objects.get_or_create(author_id=author_id)
            inbox.items.insert(0, {"type": "Follow","summary":summary,"actor":new_follower_serialized,"object":author_serialized}) # append to items list
            inbox.save()
            return Response({'message':'sent successfully!'}, status=status.HTTP_200_OK)

        elif content_type == "post":
            post_id = request.data['post_id']
            post = Post.objects.get(post_id=post_id)
            item_serializer = PostSerializer(post)
            data = item_serializer.data

            try:
                Author.objects.get(author_id=author_id) # check if local author
                inbox, _ = Inbox.objects.get_or_create(author_id=author_id)
                inbox.items.insert(0, data) # append to items list
                inbox.save()
                return Response({'message':'sent successfully!'}, status=status.HTTP_200_OK)
            except Author.DoesNotExist:
                return Response({'message': 'sent unsuccessfully!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def friend(request, authorID):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)

    followers_objects = get_followers(authorID) # get followers of author
    friends = []
    for f in followers_objects: # foreach follower f of author
        follower_id = f['id'].split("/")[-1]
        if Follow.objects.filter(author1=follower_id, author2=authorID).exists(): # check if author is also a follower of f
            friends.append(f)
    return Response({"type": "friends","items":friends}, status=status.HTTP_200_OK)
            