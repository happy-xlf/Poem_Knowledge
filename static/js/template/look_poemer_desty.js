
layui.use(['layer','element','util','laypage'],function () {

    var $=layui.$,layer=layui.layer;
    var element=layui.element;
    util = layui.util;//引入util
    laypage=layui.laypage;

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

    function flushPage(num,curr){
        layui.use(['laypage', 'layer'], function(){
        var laypage = layui.laypage,layer = layui.layer;
        laypage.render({
            elem: 'demo11'	//渲染的对象
            ,count: num		//注意这里的count是数据条数
            ,limit: 20		//每页显示8条数据
            ,curr : curr	//当前高亮页
            ,theme: '#1E9FFF'
            ,layout:['page','count']
            ,jump: function (obj, first) { //obj为当前页的属性和方法，第一次加载first为true
                //do SomeThing
                if (!first) {	//非首次加载
                    console.log(obj.curr);
                    getSongByPage(obj.curr);	//执行跳页方法，刷新显示内容，然后再在跳页方法中调用该方法，来改变总页数
                    //注意这里的总页数是，layui自己给我们算出来的，我们需要提供后台返回的总记录数，以及一页显示记录条数
                }
            }
            });
        });
    }
//Tab初始化唐代诗人
    var index =  layer.load(2,{ //icon支持传入0-2
            shade: [0.4, '#d0d0d0'], //0.5透明度的灰色背景
            offset: ['40%', '45%'], //位置
            content: '加载中...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'color':'#fff',
                    'padding-top': '78px',
                    'padding-left': '13px',
                    'width': '60px',
                    'font-size':'16px'

                });
            }
        });
    getSongByPage(1);



    function getSongByPage(page) {
        if (page <= 0) {
            page = 1;
        }
        sql_page = (page - 1) * 20;

        $.ajax({
            url: "/look_poemer_desty",
            type: "POST",
            data: {"desty": $("#desty_name").val(), "page": sql_page},
            dataType: "json",
            async: true,
            success: function (res) {
                text = "";
                total_sum = res[0].sum;
                slen=res.length;
                for(i=0;i<5;i++)
                {
                    j=i*4;
                    maxl=j+4;
                    if(maxl>slen)
                        maxl=slen;
                    text+="<div class='layui-card'>" +
                        "                    <div class='layui-card-body '>" +
                        "                        <div class='layui-row'>";
                    for(;j<maxl;j++)
                    {
                        author=res[j].author;
                        produce=res[j].produce;
                        img_src=res[j].src;
                        text+="<div class='layui-col-md1' style='padding-left: 5px'>" +
                            "                                <a href='javascript:;' onclick=show_name("+"'"+author+"'"+")  >" +
                            "                                    <img id='author_img' src='"+img_src+"'>" +
                            "                                </a>" +
                            "                                <br>" +
                            "                                <br>" +
                            "                                <a style='font-size: 16px' href='javascript:;' onclick=show_name("+"'"+author+"'"+") >"+author+"</a>" +
                            "                            </div>" +
                            "                            <div class='layui-col-md2' style='padding-left: 10px'>" +
                            "                                <a id='produce'>" +
                            "                                    "+produce+" " +
                            "                                </a>" +
                            "                                <br>" +
                            "                                <a href='javascript:;' onclick=show_name("+"'"+author+"'"+") style='color: #5f9ea0;font-size: 16px;margin-left: 100px'>查看详情</a>" +
                            "                            </div>";
                    }
                    text+="</div>" +
                        "</div>";
                }
                text+="</div>";
                var songNum = total_sum;		//取出总记录数
                flushPage(songNum, page);
                $("#pomer_show").html(text);
                layer.close(index);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });
    }

    $("#search").click(function () {
        poemer_name=$("#search_name").val();
        desty_name=$("#desty_name").val();
        ans=poemer_name+","+desty_name;
        parent.xadmin.add_tab('诗人查找','/tz_find_poemerByDestyAndName/'+ans);
    });

    show_name = function(name) {
        parent.xadmin.add_tab(name+'图谱','/author/'+name);
    };

});


