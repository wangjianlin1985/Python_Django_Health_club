var zyemail="",
    zyUname="",
    hash={
        'qq.com': 'http://mail.qq.com',
        'gmail.com': 'http://mail.google.com',
        'sina.com': 'http://mail.sina.com.cn',
        '163.com': 'http://mail.163.com',
        '126.com': 'http://mail.126.com',
        'yeah.net': 'http://www.yeah.net/',
        'sohu.com': 'http://mail.sohu.com/',
        'tom.com': 'http://mail.tom.com/',
        'sogou.com': 'http://mail.sogou.com/',
        '139.com': 'http://mail.10086.cn/',
        'hotmail.com': 'http://www.hotmail.com',
        'live.com': 'http://login.live.com/',
        'live.cn': 'http://login.live.cn/',
        'live.com.cn': 'http://login.live.com.cn',
        '189.com': 'http://webmail16.189.cn/webmail/',
        'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
        'yahoo.cn': 'http://mail.cn.yahoo.com/',
        'eyou.com': 'http://www.eyou.com/',
        '21cn.com': 'http://mail.21cn.com/',
        '188.com': 'http://www.188.com/',
        'foxmail.coom': 'http://www.foxmail.com'
    },
    zy_c_num=60,
    zy_str="";

//激活邮箱事件
function zy_Countdown(){
    zy_c_num--;
    $(".sendE2 span").html(zy_c_num+"s");
    $(".zy_success span").html(zy_str);
    (zy_c_num<58)&&$(".zy_success").addClass("upmove");
    if(zy_c_num<=0){
        zy_c_num=60;
        $(".sendE2").hide();
        $(".sendE").show()
        return false;
    }
    setTimeout("zy_Countdown()",1000);
}






$(function() {
    //兼容IE9下placeholder不显示问题
    function isPlaceholder(){
        var input = document.createElement('input');
        return 'placeholder' in input;
    }
    if(!isPlaceholder()){
        $("input").not("input[type='password']").each(
            function(){
                if($(this).val()=="" && $(this).attr("placeholder")!=""){
                    $(this).val($(this).attr("placeholder"));
                    $(this).focus(function(){
                        if($(this).val()==$(this).attr("placeholder")) $(this).val("");
                    });
                    $(this).blur(function(){
                        if($(this).val()=="") $(this).val($(this).attr("placeholder"));
                    });
                }
        });
        $("textarea").each(
            function(){
                if($(this).val()=="" && $(this).attr("placeholder")!=""){
                    $(this).val($(this).attr("placeholder"));
                    $(this).focus(function(){
                        if($(this).val()==$(this).attr("placeholder")) $(this).val("");
                    });
                    $(this).blur(function(){
                        if($(this).val()=="") $(this).val($(this).attr("placeholder"));
                    });
                }
        });
        var pwdField    = $("input[type=password]");
        var pwdVal      = pwdField.attr('placeholder');
        pwdField.after('<input id="pwdPlaceholder" type="text" value='+pwdVal+' autocomplete="off" />');
        var pwdPlaceholder = $('#pwdPlaceholder');
        pwdPlaceholder.show();
        pwdField.hide();

        pwdPlaceholder.focus(function(){
            pwdPlaceholder.hide();
            pwdField.show();
            pwdField.focus();
        });

        pwdField.blur(function(){
            if(pwdField.val() == '') {
                pwdPlaceholder.show();
                pwdField.hide();
            }
        });
    }

    $('.imgslide').unslider({
        speed: 500,
        delay: 3000,
        complete: function() {},
        keys: true,
        dots: true,
        fluid: false
    });
    var unslider = $('.imgslide').unslider();
    $('.unslider-arrow').click(function() {
        var fn = this.className.split(' ')[1];
        unslider.data('unslider')[fn]();
    });

    $('.tab > h2').click(function(){
        var _self = $(this),
            index = _self.index();
        _self.addClass('active').siblings().removeClass('active');
        $('.tab-form').eq(index).removeClass('hide').siblings('.tab-form').addClass('hide');
    });

    //input的focus和blur效果
	$('input[type=text]').focus(function(){
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=text]').blur(function(){
		$(this).parent().removeClass('focus').addClass('blur');
	});
    //input的focus和blur效果
	$('input[type=password]').focus(function(){
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=password]').blur(function(){
		$(this).parent().removeClass('focus').addClass('blur');
	});

    //弹出框关闭按钮
	$('.jsCloseDialog').on('click', function(){
		$(this).parents('.dialogbox').hide();
        $('#dialogBg').hide();
        if($(this).siblings('form')[0]){
            $(this).siblings('form')[0].reset();
        }
	});




    //登录表单键盘事件
    $("#jsLoginForm").keydown(function(event){
        if(event.keyCode == 13) {
            $('#jsLoginBtn').trigger('click');
        }
    });


});
