# シリアライズについて
# 例としてフロントエンドからgetメソッドでJSONのデータがほしいとDBにアクセスした際
# これはreadonlyなど、細かく設定できる。
# シリアライザーというものはモデルのクラスに対してい一対一で作成する。
# そしてフロント側にはこのfieldsが返ってくる。
# そのためそれを型定義すればよい。

from rest_framework import serializers
from .models import Task, Category, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:  # Metaクラスの中に一つずつテーブルに対して記載する決まり
        model = User  # まずはUserテーブル
        fields = ['id', 'username', 'password']  # Userテーブルからどのカラムを使用したいか
        #  そのカラムに更なるオプション
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    #  シリアライザーではハッシュ化した状態でDBに保存しないといけないため

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_profile', 'img']
        extra_kwargs = {'user_profile': {'read_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'item']


class TaskSerializer(serializers.ModelSerializer):
    #  Taskのテーブル一覧にあるcategory_itemは実際は外部キー参照でcategory_itemのprimary keyが入っているだけ
    #  すなわち、Taskテーブルのcategoryをみてもidしかわからない。実際はユーザはidよりはcategoryのitemを知りたいため
    #  それをシリアライズで実現する。その処理が以下の三行
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)  # noqa: E501
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)  # noqa: E501
    responsible_username = serializers.ReadOnlyField(source='responsible.username', read_only=True)  # noqa: E501
    #  tuple STATUSの中身を取得できる
    status_name = serializers.CharField(source='get_status_display', read_only=True)  # noqa: E501
    #  デフォルトのデータがかなり細かいためこちらで加工
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)  # noqa: E501
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)  # noqa: E501

    class Meta:
        model = Task
        fields = ['id', 'Task', 'description', 'criteria', 'status', 'status_name', 'category',  # noqa: E501
                  'category_item', 'estimate', 'responsible_username', 'owner', 'owner_username',  # noqa: E501
                  'created_at', 'updated_at']
        #  ownerはDjangoがuserから自動で認識し、ownerに割り当てる
        extra_kwargs = {'owner': {'read_only': True}}
