$(function() {
    var request_id, id;
    $(".modify-btn").click(function(event) {
        request_id = $(this).parents(".detail-table").children('td:first-child').attr("id");
        $.post('{% url "show_apply_machinedetail" %}', { "id": request_id }, function(data) {
            var detail_list = eval($.parseJSON(data));
            //数据获取
            $(".dropdownMenu1").text(detail_list[0].fields.appro_env_type).append('&nbsp;<span class="caret"></span>');
            $("#" + request_id + "modal input[value='" + detail_list[0].fields.appro_fun_type + "']").prop("checked", true).parent("label").addClass('active').siblings('label').removeClass('active');
            $(".dropdownMenu2").text(detail_list[0].fields.appro_os_type).append('&nbsp;<span class="caret"></span>');
            $("#" + request_id + "modal ." + detail_list[0].fields.appro_cpu + "C").prop('checked', true).parent("label").addClass('active').siblings('label').removeClass('active');
            $("#" + request_id + "modal ." + detail_list[0].fields.appro_memory_gb + "G").prop('checked', true).parent("label").addClass('active').siblings('label').removeClass('active');
            $("#" + request_id + "modal input[name='data_volume']").val(detail_list[0].fields.appro_datadisk_gb);
            $("#" + request_id + "modal input[name='request_num']").val(detail_list[0].fields.appro_vm_num);
        });
        var saving_data_disk = $("#" + request_id + "data_volume").val();
        var saving_request_num = $("#" + request_id + "request_num").val();

        $("#" + request_id + "modifyslider").slider({
            range: "min",
            min: 0,
            max: 100,
            value: parseInt(saving_data_disk),
            slide: function(event, ui) {
                $("#" + request_id + "data_volume").val(ui.value);
            }
        });
        $("#" + request_id + "modifyslider_num").slider({
            value: parseInt(saving_request_num),
            min: 0,
            max: 6,
            step: 1,
            slide: function(event, ui) {
                $("#" + request_id + "request_num").val(ui.value);
            }
        });
    });

    $(".agree-btn").click(function(event) {
        id = $(this).parents(".detail-table").children('td:first-child').attr("id");
        $.post('{% url "ajax_get_agree_form" %}', { "id": parseInt(id) }, function(data, textStatus) {
            if (textStatus == "success") {
                var detail_list = eval($.parseJSON(data));
                var show_list = [detail_list[0].fields.appro_env_type, detail_list[0].fields.appro_fun_type, detail_list[0].fields.appro_cpu, detail_list[0].fields.appro_memory_gb, detail_list[0].fields.appro_datadisk_gb, detail_list[0].fields.appro_vm_num, detail_list[0].fields.appro_os_type];
                for (var i = 0; i < show_list.length; i++) {
                    $("#" + id + "AgreeForm em").eq(i).text(show_list[i])
                }
                $.post('{% url "ajax_select_IP" %}', { "id": parseInt(id) }, function(data, textStatus) {
                    if (textStatus == "success") {
                        for (var vm_num = 0; vm_num < data.length; vm_num++) {
                            v_id = vm_num + 1
                            $("#" + id + v_id + "ipaddress").text(data[vm_num].ipaddress)
                        }
                    } else {
                        alert("ajax异常")
                    }
                });
            } else {
                alert("ajax 异常")
            }
        });
    });
    $(".delete-btn").click(function(event) {
        id = $(this).parents(".detail-table").children('td:first-child').attr("id");
        application_id = $(this).parents(".detail-table").children('td').eq(1).attr('id');
        var reason = prompt("确认删除？填写原因，将会退回给申请人哦")
        if (reason) {
            reason = $.trim(reason);
            var dict = {
                "id": id,
                "application_id": application_id,
                "reason": reason,
            }
            $.post('{% url "delete_apply" %}', dict, function(data) {
                alert("删除成功");
                setTimeout(function(e) {
                    $("#" + id + "tr").remove()
                }, 200);
            });
        }
    });
    $(".modify-save-btn").click(function(event) {
        var saving_fun_type = $("#" + request_id + "modal input[name='fun_type']:checked").val();
        var saving_env_type = $("#" + request_id + "modal input[name='env_type']").val();
        var saving_cpu_num = $("#" + request_id + "modal input[name='cpu']:checked").val();
        var saving_memory_num = $("#" + request_id + "modal input[name='memory']:checked").val();　　
        var saving_os_type = $("#" + request_id + "modal input[name='os_type']").val();
        var saving_data_disk = $("#" + request_id + "modal input[name='data_volume']").val();
        var saving_request_num = $("#" + request_id + "modal input[name='request_num']").val();
        var saving_form = {
            "request_id": request_id,
            "saving_fun_type": saving_fun_type,
            "saving_env_type": saving_env_type,
            "saving_cpu_num": saving_cpu_num,
            "saving_memory_num": saving_memory_num,
            "saving_os_type": saving_os_type,
            "saving_data_disk": saving_data_disk,
            "saving_request_num": saving_request_num,
        }
        $.post('{% url "modify_machine_detail" %}', saving_form, function(data) {
            alert("保存成功！");
            setTimeout(function(e) {
                location.href = '{% url "VM_list" %}'
            }, 200);
        });

    });

    $(".change-ip").click(function(event) {
        vm_num = $(this).attr('name');
        $.ajax({
            url: '{% url "ajax_select_IP" %}',
            type: 'post',
            dataType: 'json',
            data: { "id": parseInt(id) },
            success: function(data) {
                $("#" + id + vm_num + "ipaddress").text(data[Math.random(1, data.length)].ipaddress)
            },
            error: function() {
                alert("ajax 异常");
            }
        })

    });

    $(".cluster").focus(function(event) {
        vm_num = $(this).siblings('strong').text()
        $("#" + id + vm_num + "cluster").empty().append("<option value='value'></option>");
        $.post('{% url "ajax_get_cluster" %}', { "id": parseInt(id) }, function(data, textStatus) {
            if (textStatus == "success") {
                for (var i = 0; i < data.length; i++) {
                    $("#" + id + vm_num + "cluster").append("<option value='" + data[i].cluster_id + "'>" + data[i].cluster_name + "</option>")
                }
            } else {
                alert("获取下拉列表出错")
            }
        });
    });
    $(".cluster").change(function(event) {
        /*$("#"+id+$(this).get(0).selectedIndex+"block").css("display","block");*/
        vm_num = $(this).siblings('strong').text()
            /*vm_num = $("#"+id+"uni").text()*/
        $("#" + id + vm_num + "resourcepool").empty();
        $("#" + id + vm_num + "storage").empty();
        $.ajax({
            url: '{% url "ajax_get_resource" %}',
            type: 'post',
            dataType: 'json',
            data: { "id": parseInt($(this).val()) },
            success: function(data) {
                $("#" + id + vm_num + "resourcepool").empty();
                for (var i = 0; i < data.length; i++) {
                    $("#" + id + vm_num + "resourcepool").append("<option value='" + data[i].resp_id + "'>" + data[i].resp_name + "</option>")
                }
            },
            error: function() {
                alert("ajax 异常");
            }
        });
        $.ajax({
            url: '{% url "ajax_get_storage" %}',
            type: 'post',
            dataType: 'json',
            data: { "id": parseInt($(this).val()) },
            success: function(data) {
                $("#" + id + vm_num + "storage").empty();
                for (var i = 0; i < data.length; i++) {
                    $("#" + id + vm_num + "storage").append("<option value='" + data[i].datastore_id + "'>" + data[i].datastore_name + "</option>")
                }
            },
            error: function() {
                alert("ajax 异常");
            }
        })

    });
    $(".conf-agree-btn").click(function(event) {
        var basic_data_array = []
        var assign_data_array = []
        var temp_array = []
        for (var i = 0; i < $("#" + id + "AgreeForm em").length; i++) {
            basic_data_array.push($("#" + id + "AgreeForm em").eq(i).text())
        }
        for (var j = 1; j <= $("#" + id + "AgreeForm strong").length - 1; j++) {
            temp_array.push($("#" + id + j + "ipaddress").text())
            temp_array.push($("#" + id + j + "machinename").text())
            temp_array.push($("#" + id + j + "cluster").val())
            temp_array.push($("#" + id + j + "resourcepool").val())
            temp_array.push($("#" + id + j + "storage").val())

        }
        var confirm_form = {
            "request_id": id,
            "basic_data": basic_data_array,
            "assign_data": temp_array,
        }
        alert(JSON.stringify(confirm_form))
        $.post('{% url "agree_apply" %}', confirm_form, function(data) {
            alert("提交成功！" + data);
            setTimeout(function(e) {
                location.href = '{% url "VM_list" %}'
            }, 200);
        });
        console.log("get data successfully!")
    });

    $(".gen-btn").click(function(event) {
        var str = ""
        $("#agree-table input[name='checkbox']:checkbox").each(function() {
            if ($(this).prop("checked")) {
                str += $(this).val() + ","
            }
        });
        //ajax传输数据
        $.ajax({
            url: '{% url "generate_machine" %}',
            type: 'post',
            dataType: 'json',
            data: { "id": parseInt(id) },
            success: function(data) {
                alert(data)
                $(".gen-btn").text('正在生成资源');
                var count = 0;
                setInterval(function() {
                    $(".gen-btn").append('<span>.</span>');
                    count += 1;
                    if (count == 4) {
                        $(".gen-btn span").remove();
                        count = 0;
                    }
                }, 200)
            },
            error: function() {
                alert("ajax 异常");
            }
        });
    });

    function selectMenu(factor, name) {
        factor.next().find("a").click(function() {
            factor.text($(this).text()).append('&nbsp;<span class="caret"></span>');
            name.val($(this).attr("name"));
        })
    }

    selectMenu($(".dropdownMenu1"), $(".env_type"));
    selectMenu($(".dropdownMenu2"), $(".os_type"));
    $("#selectall").click(function() {
        if ($("#selectall").prop("checked")) {
            $("#agree-table :checkbox").prop("checked", true);
        } else {
            $("#agree-table :checkbox").prop("checked", false);
        }
    });

    function select_binding(type, cpu, memory) {
        type.click(function(event) {
            /* Act on the event */
            $("." + cpu + "C").parent("label").addClass('active').siblings('label').removeClass('active');
            $("." + cpu + "C").val(cpu)
            $("." + memory + "G").parent("label").addClass('active').siblings('label').removeClass('active');
            $("." + memory + "G").val(memory)
        });
    }
    select_binding($(".normal-type"), 2, 4);
    select_binding($(".was-type"), 4, 8);
    select_binding($(".database-type"), 4, 16);
});