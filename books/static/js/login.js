function hasClass(elem, cls) {
    cls = cls || '';
    if (cls.replace(/\s/g, '').length == 0) return false; //当cls没有参数时，返回false
    return new RegExp(' ' + cls + ' ').test(' ' + elem.className + ' ');
}

function addClass(ele, cls) {
    if (!hasClass(ele, cls)) {
        ele.className = ele.className == '' ? cls : ele.className + ' ' + cls;
    }
}

function removeClass(ele, cls) {
    if (hasClass(ele, cls)) {
        var newClass = ' ' + ele.className.replace(/[\t\r\n]/g, '') + ' ';
        while (newClass.indexOf(' ' + cls + ' ') >= 0) {
            newClass = newClass.replace(' ' + cls + ' ', ' ');
        }
        ele.className = newClass.replace(/^\s+|\s+$/g, '');
    }
}

document.querySelector(".login-button").onclick = function () {


$('.login-button').on('click', function () {
    alert(123)
});
    $.ajax({
        url: '/home/login/',   //往哪里提交数据   --路由里面提交
        type: 'post',     //默认请求时GET，要修改成post，小写
        data: {           //提交的数据由好多，所以以字典的形式提交
            'name': $('#username').val(),
            'password': $('#password').val(),  //这里获取的主要时用户名和密码
            'code': $('#code').val()
        },
        success: function (val) {     //返回之后的操作，还有返回的数据
            if (val.start == 1) {
                console.log(val.msg)
                window.location.href = '/show/'
            }
            else {
                console.log(val.msg)
                window.location.href='/register/'
            }

        },
        // error:function () {  //当请求资源不存在的时候会返回一个错误消息
        //   console.log(345678)
        // }

    })
})
