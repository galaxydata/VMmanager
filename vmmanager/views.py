# -*- coding:utf-8 -*-

from .jvm_api import *
from .vc_api import *
import json
from .models import VCenter, Application, Approvel, VMOrder
from .tasks import vmtask_clone_vm
from datetime import datetime

# Create your views here.


@require_role('admin')
def VM_list(request):
    username = request.user.username
    applylist = Approvel.objects.filter(appro_status='AI').order_by('-id')
    apply_confirm_list = Approvel.objects.filter(
        appro_status='AP').order_by('-appro_date')
    applylist, p, applys, page_range, current_page, show_first, show_end = pages(applylist, request)

    return my_render('jvmanager/test_manage.html', locals(), request)


@require_role('admin')
def show_apply_machinedetail(request):
    """ajax获取机器详细信息"""
    if request.method == "POST":
        id = int(request.POST.get('id', ''))
        applydetail = Approvel.objects.filter(application_id=id)
        applydetail_dict = simplejson.dumps(applydetail, cls=QuerySetEncoder)
        return JsonResponse(applydetail_dict)
    else:
        error_dict = {'error': 'ajax not good'}
        return JsonResponse(error_dict)


def modify_machine_detail(request, *call_args):
    """
    修改用户单个机器详细信息
    """
    if request.method == "POST":
        request_id = int(request.POST.get('request_id', ''))
        saving_env_type = request.POST.get('saving_env_type', '')
        saving_fun_type = request.POST.get('saving_fun_type', '')
        saving_cpu_num = int(request.POST.get('saving_cpu_num', ''))
        saving_memory_num = int(request.POST.get('saving_memory_num', ''))
        saving_os_type = request.POST.get('saving_os_type', '')
        saving_data_disk = int(request.POST.get('saving_data_disk', ''))
        saving_apply_num = int(request.POST.get('saving_request_num', ''))
        saving_apply_status = 'AI'
        saving_datetime = datetime.now()
        try:
            Approvel.objects.filter(application_id=request_id).update(appro_fun_type=saving_fun_type, appro_os_type=saving_os_type,
                                                             appro_cpu=saving_cpu_num, appro_env_type=saving_env_type,
                                                             appro_memory_gb=saving_memory_num, appro_datadisk_gb=saving_data_disk,
                                                             appro_vm_num=saving_apply_num,
                                                             appro_date=saving_datetime,
                                                             appro_status=saving_apply_status)
        except Exception, e:
            raise e
        else:
            info_dict = {'success': "ajax post successfully!"}
            return JsonResponse(info_dict)
    else:
        error_dict = {'error': 'ajax post not good!'}
        return JsonResponse(error_dict)


@require_role('admin')
def agree_apply(request):
    """
    同意申请
    """
    if request.method == "POST":
        request_id = int(request.POST.get('request_id', ''))
        application = Application.objects.get(id=request_id)
        approving_env_type = request.POST.get('confirm_env_type', '')
        approving_fun_type = request.POST.get('confirm_fun_type', '')
        approving_cpu_num = int(request.POST.get('confirm_cpu_num', ''))
        approving_memory_num = int(request.POST.get('confirm_memory_num', ''))
        approving_os_type = request.POST.get('confirm_os_type', '')
        approving_data_disk = int(request.POST.get('confirm_data_disk', ''))
        approving_apply_num = int(request.POST.get('confirm_vm_num',''))
        approving_dist_plan = request.POST.get('confirm_dist_plan', '')
        approving_status = "AP"
        approving_datetime = datetime.now()
        try:
            Approvel.objects.filter(id=request_id).update(appro_status=approving_status)
            approvel = Approvel.objects.get(application_id=request_id)
            # src_template = Template.objects.get()
            # loc_ip = IPUsage.objects.get()
            # loc_cluster = ComputeResource.objects.get()
            # loc_resp = ResourcePool.objects.get()
            # loc_storage = Datastore.get_object()
            vmorder = VMOrder(approvel=approvel)
            vmorder.save()
            # for x in xrange(1,approving_apply_num):
            #     dist_plan = approving_dist_plan[:5*x]
            #     vmorder = VMOrder(approvel=approvel,loc_resp=dist_plan[0], loc_ip=dist_plan[1],
            #                          loc_storage=dist_plan[2],
            #                          src_template=dist_plan[3], loc_cluster=dist_plan[4])
            #     vmorder.save()
        except Exception, e:
            raise e
        else:

            # confirmlist = Approvel.objects.filter(application=application)
            # list_dict = simplejson.dumps(confirmlist, cls=QuerySetEncoder)
            # return JsonResponse(list_dict)
            success_dict = {"info": "success"}
            return JsonResponse(success_dict)
    else:
        error_dict = {'error': 'pajax post not good'}
        return JsonResponse(error_dict)


@require_role('admin')
def delete_apply(request):
    """删除申请"""
    if request.method == 'POST':
        id = int(request.POST.get("id", ""))
        reason = request.POST.get("reason", "")
        try:
            Application.objects.filter(id=id).update(apply_status='RB', apply_reason=reason)
        except Exception, e:
            raise e
        else:
            success_dict = {"info": "success"}
            return JsonResponse(success_dict)
    else:
        error_dict = {"error": "ajax not good"}
        return JsonResponse(error_dict)


@require_role('admin')
def agree_apply_list(request):
    """
    通过列表
    """
    pass


@require_role(role='user')
def apply_machine(request):
    """
    用户申请机器
    """
    username = request.user.username
    user = get_object(User, username=username)

    if request.method == 'POST':
        env_type = request.POST.get('env_type', '')
        fun_type = request.POST.get('fun_type', '')
        cpu = int(request.POST.get('cpu', ''))
        memory = int(request.POST.get('memory', ''))
        os_type = request.POST.get('os_type', '')
        data_disk = int(request.POST.get('data_disk', ''))
        request_num = int(request.POST.get('request_num', ''))
        apply_reason = request.POST.get('apply_reason', '')
        app_name = request.POST.get('app_name', '')
        submitt = request.POST.get('submit', '')
        if submitt == 'submit':
            apply_status = "SM"
            try:
                application = db_add_userapply(env_type=env_type, fun_type=fun_type, cpu=cpu, memory_gb=memory, os_type=os_type,
                             datadisk_gb=data_disk, request_vm_num=request_num,
                             apply_status=apply_status, app_name=app_name, apply_reason=apply_reason,
                             apply_date=datetime.now(), user=user)
                db_add_approvel(application=application, appro_env_type=env_type, appro_fun_type=fun_type, appro_cpu=cpu, appro_memory_gb=memory, appro_os_type=os_type, appro_datadisk_gb=data_disk, appro_vm_num=request_num, appro_status='AI', appro_date=datetime.now())

            except ServerError:
                pass
            else:
                return HttpResponseRedirect(reverse('resource_view'))
        else:
            apply_status = "HD"
            try:
                application = db_add_userapply(env_type=env_type, fun_type=fun_type, cpu=cpu, memory_gb=memory, os_type=os_type,
                             datadisk_gb=data_disk, request_vm_num=request_num,
                             apply_status=apply_status, app_name=app_name, apply_reason=apply_reason,
                             apply_date=datetime.now(), user=user)
            except Exception, e:
                raise e
            else:
                return HttpResponseRedirect(reverse('saving_resource_view'))
    return my_render('jvmanager/apply_machine.html', locals(), request)


@require_role(role='user')
def resource_view(request):
    """
    用户资源概览
    """
    username = request.user.username
    applylist = Application.objects.exclude(apply_status="HD").order_by('-id')
    applylist, p, applys, page_range, current_page, show_first, show_end = pages(
        applylist, request)
    return my_render('jvmanager/resource_view.html', locals(), request)


@require_role('user')
def saving_resource_view(request):
    s_apply_list = Application.objects.filter(apply_status="HD")
    s_apply_list, p, s_applys, page_range, current_page, show_first, show_end = pages(
        s_apply_list, request)
    return my_render('jvmanager/savingresource_view.html', locals(), request)


@require_role('user')
def submit_saving_resource(request):
    """ajax提交保存资源"""
    if request.method == 'POST':
        id = int(request.POST.get('id', ''))
        try:
            Application.objects.filter(id=id).update(apply_status="SM")
        except Exception, e:
            raise e
        else:
            success_dict = {"info": "success"}
            return JsonResponse(success_dict)
    else:
        error_dict = {"error": "ajax not good"}
        return JsonResponse(error_dict)


@require_role('admin')
def set_vm(request):
    return my_render('jvmanager/set_vm.html', locals(), request)


def generate_machine(request):
    """
    前端返回一个ID列表{json}，然后根据ID去approv表获取相关参数生成机器，包括台数等
    """
    if request.method == 'POST':
        idlist = str(request.POST.get('id', ''))
        id = [int(x) for x in idlist.split(',')]
        try:
            for x in id:
                vmorder = VMOrder.objects.get(pk=x)
                if not vmorder.gen_status:
                    vmtask_clone_vm.delay(vmorder)
        except Exception, e:
            raise e
        else:
            success_dict = {"info": "success"}
            return JsonResponse(success_dict)
    else:
        error_dict = {"error": "ajax not good"}
        return JsonResponse(error_dict)


def ajax_get_process(request):
    """
    根据ID列表获取生成进度
    """
    if request.method == 'POST':
        result_list = []
        idlist = str(request.POST.get('id', ''))
        id = [int(x) for x in idlist.split(',')]
        try:
            for x in id:
                vmorder = VMOrder.objects.get(pk=x)
                if vmorder.gen_status:
                    result_list.append({'id': x, 'progress': vmorder.gen_progress, 'log': vmorder.gen_log, 'status': vmorder.gen_status})
        except Exception, e:
            raise e
        else:
            return json.dumps(result_list)
    else:
        error_dict = {"error": "ajax not good"}
        return JsonResponse(error_dict)


def ajax_get_generatestatus():
    """
    根据ID列表获取生成日志
    """
    pass


def ajax_get_template():
    """
        前端返回cluster名称clustername，获取对应的template
        """
    pass


def ajax_get_cluster(request):
    """
    动态获取集群信息，需返回所有可用集群名称以及权重比(CPU+内存＋存储)
    参数对照
    id: Approvel id
    """
    if request.method == 'POST':
        approvel_id = int(request.POST['id'])
        try:
            approvel = Approvel.objects.get(pk=approvel_id)
            env_type = approvel.appro_env_type
            result_list = get_capi_cluster(env_type)
        except Exception, e:
            raise e
        else:
            return json.dumps(result_list)
    else:
        error_dict = {"error": "ajax not good"}
        return JsonResponse(error_dict)


def ajax_get_resource():
    """
        获取资源称名称
        """
    pass


def ajax_get_storage():
    """
        获取相关集群的剩余容量，前端返回集群名称clustername，需返回剩余容量值及百分比
        """
    pass


# VM参数配置页面
def ajax_add_IP():
    """
        动态激活IP段
        """
    pass


def ajax_get_IP():
    """
        获取可用IP列表，用于下拉框选择
        """
    pass


def ajax_add_template():
    """
        添加template
        """
    pass


def get_templates():
    """
        获取所有模板信息
        """
    pass