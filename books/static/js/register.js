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

document.querySelector(".register-button").onclick = function () {
$('.register-button').on('click', function () {
    $.ajax({
        url: '/user/register/',   //往哪里提交数据   --路由里面提交
        type: 'post',     //默认请求时GET，要修改成post，小写
        data: {           //提交的数据由好多，所以以字典的形式提交
            'username': $('#username').val(),
            'password': $('#password').val(),  //这里获取的主要时用户名和密码
            'msg': $('#msg').val(),
        },
        success: function (data) {     //返回之后的操作，还有返回的数据
            if (data.start === 100) {
                console.log(data.msg)
                //window.location.href = '/show/'
            }
            else {
                console.log(data.msg)
                //window.location.href='/home/'
            }

        },
    })
})
