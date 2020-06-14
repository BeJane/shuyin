# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acomment(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    audioid = models.ForeignKey('Audio', models.DO_NOTHING, db_column='AudioID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'acomment'


class Admonistrators(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=8)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admonistrators'


class Audio(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.ForeignKey('Chapter', models.DO_NOTHING, db_column='chapterID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(unique=True, max_length=50)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'audio'


class Audiothumbsup(models.Model):
    thumbsup = models.BigAutoField(db_column='Thumbsup', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    worksid = models.ForeignKey(Audio, models.DO_NOTHING, db_column='worksID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audiothumbsup'


class Book(models.Model):
    bookid = models.BigAutoField(db_column='bookID', primary_key=True)  # Field name made lowercase.
    introduction = models.CharField(db_column='Introduction', max_length=100)  # Field name made lowercase.
    author = models.CharField(max_length=20)
    bookname = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'book'


class Ccomment(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.ForeignKey('Chapter', models.DO_NOTHING, db_column='chapterID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=100)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ccomment'


class Chapter(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(unique=True, max_length=50)
    cname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'chapter'


class ChapterthumbsUp(models.Model):
    thumbs_up = models.BigAutoField(db_column='Thumbs_up', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chapterthumbs_up'


class Feedback(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    audioid = models.ForeignKey(Audio, models.DO_NOTHING, db_column='AudioID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=100)  # Field name made lowercase.
    state = models.IntegerField(db_column='State')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feedback'


class User(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=8)  # Field name made lowercase.
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, blank=True, null=True)
    personalsignature = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
