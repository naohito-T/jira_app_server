from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):

    #  SAFE_METHODS = getメソッドでアクセスした場合には無条件でtrueとなる
    #  理由 データを取得するだけのため書き換えたりなどをする恐れがないため
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        #  書き換えをするユーザがownerでrequestのidと一致した時にokとする。
        return obj.owner.id == request.user.id
