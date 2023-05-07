
$(function(){
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache: false,
            type: "POST",
            dataType:'json',
            url:"/users/update/pwd/",
            data:$('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {
                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'提交成功',
                        h2:'修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                }else if(data.msg){
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({ Img: ".js-img-show", Width: 94, Height: 94 ,Callback:function(){
        $('#jsAvatarForm').submit();
    }});


    $('.changeemai_btn').click(function(){
        Dml.fun.showDialog('#jsChangeEmailDialog', '#jsChangePhoneTips' ,'jsChangeEmailTips');
    });
    $('#jsChangeEmailCodeBtn').on('click', function(){
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function(){
        changeEmailSubmit($(this));
    });


    //input获得焦点样式
    $('.perinform input[type=text]').focus(function(){
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function(){
        $(this).parent('li').removeClass('focus');
    });



    //保存个人资料
    $('#jsEdit').on('click', function(){
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')



        var token =$('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/users/info",
            data:{'data':$jsEditUserForm.serialize(),'csrfmiddlewaretoken':token},
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
                if(data.status == "fail"){
                     Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function(){window.location.href = '/users/info';},1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });


});


$.fn.serializeObject = function() {

    var o = {};

    var a = this.serializeArray();

    $.each(a, function() {

        if (o[this.name]) {

            if (!o[this.name].push) {

                o[this.name] = [ o[this.name] ];

            }

            o[this.name].push(this.value || '');

        } else {

            o[this.name] = this.value || '';

        }

    });

    return o;}

