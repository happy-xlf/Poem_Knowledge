

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

    //Tab初始化唐代诗人
    var index =  layer.load(2,{ //icon支持传入0-2
            shade: [0.4, '#000'], //0.5透明度的灰色背景
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

    show_shici = function(name) {
        parent.xadmin.add_tab(name+'诗词','/tz_look_poem_desty/'+name);
    };
    show_poemer = function(name) {
        parent.xadmin.add_tab(name+'诗人','/tz_look_poemer_desty/'+name);
    };

    //诗词信息汇总
    $.ajax({
            url: "/desty_sum",
            type: "POST",
            dataType: "json",
            async: true,
            success: function (res) {
                // alert(res['宋代']);
                var text="";
                var sum=0;
                for(var key in res) {
                    text += "<li class='layui-col-md2 layui-col-xs6'>" +
                        "                                    <a href='javascript:;' onclick=show_shici("+"'"+key+"'"+") class='x-admin-backlog-body'>" +
                        "                                        <h3>" + key + "</h3>" +
                        "                                        <p>" +
                        "                                            <cite>" + res[key] + "</cite>个</p>" +
                        "                                    </a>" +
                        "                                </li>";
                    sum += res[key];
                }
                text+="<li class='layui-col-md2 layui-col-xs6'>" +
                        "                                    <a href='javascript:;' class='x-admin-backlog-body'>" +
                        "                                        <h3>总计</h3>" +
                        "                                        <p>" +
                        "                                            <cite>"+sum+"</cite>个</p>" +
                        "                                    </a>" +
                        "                                </li>";
                $("#poem_sum").html(text);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });
    //诗人信息汇总
    $.ajax({
            url: "/poemer_sum",
            type: "POST",
            dataType: "json",
            async: true,
            success: function (res) {
                // alert(res['宋代']);
                var text="";
                var sum=0;
                for(var key in res) {
                    text += "<li class='layui-col-md2 layui-col-xs6'>" +
                        "                                    <a href='javascript:;' onclick=show_poemer("+"'"+key+"'"+") class='x-admin-backlog-body'>" +
                        "                                        <h3>" + key + "</h3>" +
                        "                                        <p>" +
                        "                                            <cite>" + res[key] + "</cite>个</p>" +
                        "                                    </a>" +
                        "                                </li>";
                    sum += res[key];
                }
                text+="<li class='layui-col-md2 layui-col-xs6'>" +
                        "                                    <a href='javascript:;' class='x-admin-backlog-body'>" +
                        "                                        <h3>总计</h3>" +
                        "                                        <p>" +
                        "                                            <cite>"+sum+"</cite>个</p>" +
                        "                                    </a>" +
                        "                                </li>";
                $("#poemer_sum").html(text);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });

    $.ajax({
            url: "/poemer_produce",
            type: "POST",
            data:{"desty":"0"},
            dataType: "json",
            async: true,
            success: function (res) {
                // alert(res['宋代']);
                var text="<div class='layui-card'>" +
                    "                                              <div class='layui-card-body'>" +
                    "                                                  <div class='layui-row'>";
                for(i=0;i<4;i++)
                {
                    author_name=res[i].name;
                    author_src=res[i].src;
                    author_produce=res[i].produce;
                    text+="<div class='layui-col-md1' style='padding-left: 5px'>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>" +
                        "                                                                <img src='"+author_src+"'>" +
                        "                                                            </a>" +
                        "                                                            <br>" +
                        "                                                            <br>" +
                        "                                                            <a style='font-size: 16px' href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>"+author_name+"</a>" +
                        "                                                        </div>" +
                        "                                                        <div class='layui-col-md2' style='padding-left: 10px'>" +
                        "                                                            <a id='produce'>" +
                        "                                                              "+author_produce+"" +
                        "</a>" +
                        "                                                            <br>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+") style='color: #5f9ea0;font-size: 16px;padding-left: 100px'>查看详情</a>" +
                        "                                                        </div>"
                }
                text+="</div>" +
                    "                                              </div>";
                text+=text="<div class='layui-card'>" +
                    "                                              <div class='layui-card-body'>" +
                    "                                                  <div class='layui-row'>";

                for(var i=4;i<8;i++)
                {
                    author_name=res[i].name;
                    author_src=res[i].src;
                    author_produce=res[i].produce;
                    text+="<div class='layui-col-md1' style='padding-left: 5px'>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>" +
                        "                                                                <img src='"+author_src+"'>" +
                        "                                                            </a>" +
                        "                                                            <br>" +
                        "                                                            <br>" +
                        "                                                            <a style='font-size: 16px' href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>"+author_name+"</a>" +
                        "                                                        </div>" +
                        "                                                        <div class='layui-col-md2' style='padding-left: 10px'>" +
                        "                                                            <a id='produce'>" +
                        "                                                              "+author_produce+"" +
                        "</a>" +
                        "                                                            <br>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+") style='color: #5f9ea0;font-size: 16px;padding-left: 100px'>查看详情</a>" +
                        "                                                        </div>"
                }
                text+="</div>" +
                    "                                              </div>" +
                    "</div>";
                $("#pomer_tab").html(text);
                layer.close(index);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });

    //Tab面板
    element.on('tab(docDemoTabBrief)', function(data){
        $.ajax({
            url: "/poemer_produce",
            type: "POST",
            data:{"desty":data.index},
            dataType: "json",
            async: true,
            success: function (res) {
                // alert(res['宋代']);
                var text="<div class='layui-card'>" +
                    "                                              <div class='layui-card-body'>" +
                    "                                                  <div class='layui-row'>";
                for(i=0;i<4;i++)
                {
                    author_name=res[i].name;
                    author_src=res[i].src;
                    author_produce=res[i].produce;
                    text+="<div class='layui-col-md1' style='padding-left: 5px'>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>" +
                        "                                                                <img src='"+author_src+"'>" +
                        "                                                            </a>" +
                        "                                                            <br>" +
                        "                                                            <br>" +
                        "                                                            <a style='font-size: 16px' href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>"+author_name+"</a>" +
                        "                                                        </div>" +
                        "                                                        <div class='layui-col-md2' style='padding-left: 10px'>" +
                        "                                                            <a id='produce'>" +
                        "                                                              "+author_produce+"" +
                        "</a>" +
                        "                                                            <br>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+") style='color: #5f9ea0;font-size: 16px;padding-left: 100px'>查看详情</a>" +
                        "                                                        </div>"
                }
                text+="</div>" +
                    "                                              </div>";
                text+=text="<div class='layui-card'>" +
                    "                                              <div class='layui-card-body'>" +
                    "                                                  <div class='layui-row'>";

                for(var i=4;i<8;i++)
                {
                    author_name=res[i].name;
                    author_src=res[i].src;
                    author_produce=res[i].produce;
                    text+="<div class='layui-col-md1' style='padding-left: 5px'>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>" +
                        "                                                                <img src='"+author_src+"'>" +
                        "                                                            </a>" +
                        "                                                            <br>" +
                        "                                                            <br>" +
                        "                                                            <a style='font-size: 16px' href='javascript:;' onclick=show_name("+"'"+author_name+"'"+")>"+author_name+"</a>" +
                        "                                                        </div>" +
                        "                                                        <div class='layui-col-md2' style='padding-left: 10px'>" +
                        "                                                            <a id='produce'>" +
                        "                                                              "+author_produce+"" +
                        "</a>" +
                        "                                                            <br>" +
                        "                                                            <a href='javascript:;' onclick=show_name("+"'"+author_name+"'"+") style='color: #5f9ea0;font-size: 16px;padding-left: 100px'>查看详情</a>" +
                        "                                                        </div>"
                }
                text+="</div>" +
                    "                                              </div>" +
                    "</div>";
                $("#pomer_tab").html(text);
            },
            error: function (e) {
                alert("出现错误！！");
            }
        });
    });

    show_name = function(name) {
        parent.xadmin.add_tab(name+'图谱','/author/'+name);
    };

});
