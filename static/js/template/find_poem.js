
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

    init();
    function init()
    {
        poem_name=$("#search_name").val();
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
        bk_img=['../static/bk_img/01.jfif','../static/bk_img/02.jfif','../static/bk_img/03.jpg','../static/bk_img/04.jpg',
    '../static/bk_img/05.jfif','../static/bk_img/06.jpg','../static/bk_img/07.jpg','../static/bk_img/08.jpg',
    '../static/bk_img/09.jfif','../static/bk_img/10.jpg','../static/bk_img/11.jfif','../static/bk_img/12.jfif',
    '../static/bk_img/13.jpg','../static/bk_img/14.jpg','../static/bk_img/15.jpg','../static/bk_img/16.jpg'];

        $.ajax({
            url: "/get_poem_by_name",
            type: "POST",
            data:{"poem_name":poem_name},
            dataType: "json",
            async: true,
            success: function (res) {
                text="";
                if(res.length>16)
                    len=16;
                else
                    len=res.length;
                for(var i=0;i<len;i++)
                {
                    title=res[i].title;
                    desty=res[i].desty;
                    author=res[i].author;
                    content=res[i].content;
                    tag=res[i].tag;
                    formal=res[i].formal;
                    img_src = bk_img[i];
                    text += "<a href='javascript:;' onclick=show_poem("+"'"+title+"'"+")>" +
                        "                <div id='he'>" +
                        "                    <div class='layui-card'>" +
                        "                        <div class='layui-card-body'>" +
                        "                            <div class='poem-title'>" +
                        "                                <span>" + title + "</span>" +
                        "                                <span>" +
                        "                                    <font color='#d75b66'>" + desty + "</font>·" + author + "" +
                        "                                </span>" +
                        "                            </div>" +
                        "                            <div class='poem-tag'>" +
                        "                                <span>" + formal + "</span>" +
                        "                            </div>" +
                        "                        </div>" +
                        "                        <div>" +
                        "                            <img class='bk_img' src='" + img_src + "'>" +
                        "                        </div>" +
                        "                        <div class='shici'>";
                        for(var j=0;j<content.length;j++)
                        {
                            text+="<p>" + content[j] + "</p>";
                        }
                        text+=
                        "                        </div>" +
                        "                    </div>" +
                        "                </div>" +
                        "            </a>"
                }
                $("#all_shici").html(text);
                layer.close(index);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });
    }

    $("#search").click(function () {
        poem_name=$("#search_name").val();
        parent.xadmin.add_tab('诗词查找','/tz_find_poem/'+poem_name);
    });

    show_poem = function(name) {
        parent.xadmin.add_tab(name+'——诗词鉴赏','/tz_poem_appearance/'+name);
    };







});
