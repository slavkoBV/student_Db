# -*- coding: utf-8 -*-

from django.db import models

# Exams Model
class Exam(models.Model):

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    subject = models.CharField(
    	max_length=256,
    	blank=False,
    	verbose_name=u"Назва предмету")

    dataAndTime = models.DateTimeField(
    	blank=False,
    	verbose_name=u'Дата та час іспиту',
    	null=True)

    teacher = models.CharField(
    	max_length=256,
    	blank=False,
    	null=True,
    	verbose_name=u'Викладач')

    exam_group = models.ForeignKey(
    	'Group',
    	verbose_name=u'Група',
    	blank=False,
    	null=True,
    	on_delete = models.PROTECT)
    

    def __unicode__(self):
       	return u'%s (%s %s)' % (self.subject, self.teacher, self.exam_group)
      