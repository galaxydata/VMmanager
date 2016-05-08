# coding:utf-8
from django.conf.urls import patterns, include, url
from jVM.views import *

urlpatterns = patterns('',
                       url(r'^list/$', VM_list, name='VM_list'),
                       url(r'^apply/$', apply_machine, name='apply_machine'),
                       url(r'^resource/$', resource_view, name='resource_view'),
                       url(r'^saving_resource/$', saving_resource_view,
                           name='saving_resource_view'),
                       url(r'^ajax_show_apply_machinedetail',
                           show_apply_machinedetail, name='show_apply_machinedetail'),
                       url(r'^ajax_confirm_machine_detail/$', modify_machine_detail,
                           name='modify_machine_detail'),
                       url(r'^ajax_agree_apply/$', agree_apply, name='agree_apply'),
                       url(r'^ajax_delete_apply/$', delete_apply, name='delete_apply'),
                       url(r'^ajax_submit_saving_resource/$',
                           submit_saving_resource, name='submit_saving_resource'),
                       url(r'^set_vm/$',set_vm,name='set_vm'),
                       )