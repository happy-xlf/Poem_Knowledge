
layui.use(['layer','element','util'],function () {

    var $=layui.$,layer=layui.layer;
    var element=layui.element;
    util = layui.util;//引入util

    util.fixbar({
        top:true
        , css: { right: 15, bottom: 35 }
        , bgcolor: '#19CAAD !important;display:block;'
        ,showHeight:100
        , click: function (type) {
            if (type === 'top') {
                $('.layui-body').animate({//主要代码
                    scrollTop: 0
                }, 200);
          }
      }
    });
    //查找触发
    $("#search").click(function () {
        search_name=$("#search_name").val();
        //alert(search_name);
        if(search_name==""){
            alert("不为空！！");
            return false;
        }
        //alert(search_name);
        //诗词信息汇总
        $.ajax({
                url: "/create_poem",
                type: "POST",
                data:{"search_name":search_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    text="<br>" +
                        "                                        <br>" +
                        "                                        <br>";
                    for(i=0;i<4;i++)
                    {
                        ju=res[i];
                        if(i%2===0)
                            ju=ju+'，';
                        else
                            ju=ju+'。';
                        text+="<p id='sent'>"+ju+"</p>";
                    }
                    $("#poem").html(text);
                    $("#ag_div").css("display","block");//使id为mazey的div显示出来
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });

    });

    //再来一次触发
    $("#again").click(function () {
        search_name=$("#search_name").val();
        if(search_name==""){
            alert("不为空！！");
            return false;
        }
        //alert(search_name);
        //诗词信息汇总
        $.ajax({
                url: "/create_poem",
                type: "POST",
                data:{"search_name":search_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    text="<br>" +
                        "                                        <br>" +
                        "                                        <br>";
                    for(i=0;i<4;i++)
                    {
                        ju=res[i];
                        if(i%2===0)
                            ju=ju+'，';
                        else
                            ju=ju+'。';
                        text+="<p id='sent'>"+ju+"</p>";
                    }
                    $("#poem").html(text);
                    $("#again").css("display","block");//使id为mazey的div显示出来
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });

    });


});
