from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max

# Create your models here.
class ProjectCode(models.Model):
    pcode = models.CharField(db_column='PCODE', max_length=50)
    pname = models.CharField(db_column='PNAME', max_length=100)
    is_active = models.BooleanField(db_column='IS_ACTIVE',
                                    default=True)  # Field name made lowercase.
    is_deleted = models.BooleanField(db_column='IS_DELETED',
                                     default=False)  # Field name made lowercase.
    created_date = models.DateTimeField(db_column='CREATED_DATE',
                                        auto_now_add=True, null=True, blank=True)  # Field name made lowercase.
    last_updated_date = models.DateTimeField(db_column='LAST_UPDATED_DATE', auto_now=True, null=True,
                                             blank=True)  # Field name made lowercase.

    class Meta(object):
        app_label = 'todoapp'
    def __str__(self):
        return str(self.id)


class TodoList(models.Model):
    pcode = models.ForeignKey(ProjectCode,db_column='PCODE', on_delete=models.CASCADE,)
    user_id = models.ForeignKey(User,db_column='USER_ID', on_delete=models.CASCADE,)
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)
    content = models.CharField(db_column='CONTENT', max_length=1000, blank=True, null=True)
    is_complete = models.IntegerField(db_column='IS_COMPLETE', blank=True, null=True)
    priority = models.IntegerField(db_column='PRIORITY', blank=True, null=True)
    end_date = models.DateField(db_column='END_DATE', blank=True, null=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE',
                                    default=True)  # Field name made lowercase.
    is_deleted = models.BooleanField(db_column='IS_DELETED',
                                     default=False)  # Field name made lowercase.
    created_date = models.DateTimeField(db_column='CREATED_DATE',
                                        auto_now_add=True, null=True, blank=True)  # Field name made lowercase.
    last_updated_date = models.DateTimeField(db_column='LAST_UPDATED_DATE', auto_now=True, null=True,
                                             blank=True)  # Field name made lowercase.

    def todo_save(self):
        self.is_complete = 0
        if TodoList.objects.all().aggregate(Max('priority'))['priority__max'] is None : self.priority = 1
        else : self.priority = int(TodoList.objects.latest('priority').priority) + 1
        self.pcode = 1
        self.user_id = 1
        self.save()

    def todo_update_is_complete(self, complete):
        self.is_complete = complete
        self.save()

    class Meta(object):
        app_label = 'todoapp'
    def __str__(self):
        return str(self.id)