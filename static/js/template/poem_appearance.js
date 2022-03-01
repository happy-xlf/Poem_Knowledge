
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
        if(poem_name==""||poem_name==null)
            poem_name="登岳阳楼";
        $.ajax({
                url: "/get_poem_message",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    title=res[0].title;
                    desty=res[0].desty+"·";
                    author=res[0].author;
                    content=res[0].content;
                    tag=res[0].tag;
                    formal=res[0].formal;
                    $("#poem_title").html(title);
                    $("#poem_desty").html(desty);
                    $("#poem_author").html(author);
                    if(formal!='无')
                        $("#poem_formal").html(formal);
                    if(tag!='无')
                        $("#tag").html(tag);
                    text='';
                    for(var i=0;i<content.length;i++)
                        text+="<a href='javascript:;' style='position: relative' onclick=emotion_ci("+"'"+content[i]+"'"+","+i+")><div class='word'>"+content[i]+"</div></a>";
                    $("#poem_content").html(text);
                    $("#poem_begin").click();
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });
    }

    poem_emotion=function(){
        $("#poem_begin").click();
    };


    emotion_ci = function(name,index) {
        var index2 =  layer.load(2,{ //icon支持传入0-2
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

        text='<p>诗句“<font style="color: red" >'+name+'</font>”表达的情感</p>';
        text+='<a style="float: right" href="#" onclick="poem_emotion()">查看整首诗表达的情感</a>';
            text+='<div id="main" style="margin:0 auto;width: 600px;height:400px;"></div>';
            $("#poem_tab").html(text);
            $.ajax({
                url: "/get_emotion_by_ju",
                type: "POST",
                data:{"ju_name":name,"poem_name":poem_name,"index":index},
                dataType: "json",
                async: true,
                success: function (res) {
                    emotion_name=res[0].name;
                    value=res[0].value;
                    appear=res[0].appear;
                    trans_content=res[0].trans_content;
                    ntext='<span id="big_title">翻译如下：</span><p id="senten">'+trans_content+'</p>';
                    ntext+='<span id="big_title">鉴赏如下：</span><p id="senten">'+appear+'</p>';
                    $("#poem_tab").append(ntext);
                    var myChart = echarts.init(document.getElementById('main'));
                    // 指定图表的配置项和数据
                    var option = {
                        tooltip : {
                            trigger: 'axis',
                            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                                type : 'shadow'       // 默认为直线，可选为：'line' | 'shadow'
                            },
                            formatter: function(datas)
                              {
                                  var res = datas[0].name + '<br/>', val;
                                  for(var i = 0, length = datas.length; i < length; i++) {
                                        val = (datas[i].value) + '%';
                                        res += datas[i].seriesName + '：' + val + '<br/>';
                                    }
                                    return res;
                               }
                        },
                        xAxis: {
                            data: emotion_name
                        },
                        yAxis: {},
                        series: [
                            {
                                name: '预测值',
                                type: 'bar',
                                itemStyle: {
                                    normal: {
                                        //好，这里就是重头戏了，定义一个list，然后根据所以取得不同的值，这样就实现了，
                                        color: function (params) {
                                            // build a color map as your need.
                                            var colorList = [
                                                '#26C0C0', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                                            ];
                                            return colorList[params.dataIndex]
                                        }
                                    }
                                },
                                data: value
                            },
                            {
                                type: 'pie',
                                itemStyle: {
                                    normal: {
                                        //好，这里就是重头戏了，定义一个list，然后根据所以取得不同的值，这样就实现了，
                                        color: function (params) {
                                            // build a color map as your need.
                                            var colorList = [
                                                '#26C0C0', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                                            ];
                                            return colorList[params.dataIndex]
                                        }
                                    }
                                },
                                data: [
                                    {value:value[0],name:emotion_name[0]},
                                    {value:value[1],name:emotion_name[1]},
                                    {value:value[2],name:emotion_name[2]},
                                    {value:value[3],name:emotion_name[3]},
                                    {value:value[4],name:emotion_name[4]},
                                    {value:value[5],name:emotion_name[5]},
                                    {value:value[6],name:emotion_name[6]}
                                ],
                                radius:'40%',
                                center:['75%','30%']
                            }
                            ]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart.setOption(option);
                    layer.close(index2);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });

    };


    $("#search").click(function () {
        poem_name=$("#search_name").val();
        parent.xadmin.add_tab('诗词查找','/tz_find_poem/'+poem_name);
    });

    element.on('tab(docDemoTabBrief)', function(data){
        poem_name=$("#search_name").val();
        if(poem_name===""||poem_name==null)
            poem_name="登岳阳楼";
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
        if(data.index===0)
        {
           $.ajax({
                url: "/get_poem_message",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    title=res[0].title;
                    desty=res[0].desty;
                    author=res[0].author;
                    content=res[0].content;
                    tag=res[0].tag;
                    formal=res[0].formal;
                    trans_content=res[0].trans_content;
                    appear=res[0].appear;
                    background=res[0].background;
                    text='<br>' +
                        '                                            <span id="big_title">译文</span>' +
                        '                                            <p id="senten">' +
                        ''+ trans_content+
                        '                                            </p>' +
                        '                                            <span id="big_title">创作背景</span>' +
                        '                                            <p id="senten">' +
                        ''+background +
                        '                                            </p>' +
                        '                                            <span id="big_title">赏析</span>' +
                        '                                            <p id="senten">' +
                        ''+appear +
                        '                                            </p>';
                    $("#poem_tab").html(text);
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });
        }
        else if(data.index===1)
        {
            $.ajax({
                url: "/get_poem_author_message",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    author=res[0].author;
                    produce=res[0].produce;
                    experience=res[0].experience;
                    text='<br>' +
                        '                                            <span id="big_title">简介</span>' +
                        '                                            <p id="senten">' +
                        ''+ produce+
                        '                                            </p>' +
                        '                                            <span id="big_title">诗人经历</span>' +
                        '                                            <p id="senten">' +
                        ''+experience +
                        '                                            </p>';
                    $("#poem_tab").html(text);
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });
        }
        else if(data.index===2)
        {
            $.ajax({
                url: "/get_poem_zhu",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    zhu=res[0].zhu;
                    text='<br>' +
                        '                                            <span id="big_title">注释</span>' +
                        '                                            <div id="senten_shi">' +
                        ''+ zhu+
                        '                                            </div>';
                    $("#poem_tab").html(text);
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });
        }
        else if(data.index===3)
        {
            text='<p>整首诗表达的情感</p>';
            text+='<div id="main" style="margin:0 auto;width: 600px;height:400px;"></div>';
            $("#poem_tab").html(text);
            $.ajax({
                url: "/get_emotion_by_poem_name",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    emotion_name=res[0].name;
                    value=res[0].value;
                    appear=res[0].appear;
                    trans_content=res[0].trans_content;
                    ntext='<span id="big_title">翻译如下：</span><p id="senten">'+trans_content+'</p>';
                    ntext+='<span id="big_title">鉴赏如下：</span><p id="senten">'+appear+'</p>';
                    $("#poem_tab").append(ntext);
                    var myChart = echarts.init(document.getElementById('main'));
                    // 指定图表的配置项和数据
                    var option = {
                        tooltip : {
                            trigger: 'axis',
                            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                                type : 'shadow'|'pie'       // 默认为直线，可选为：'line' | 'shadow'
                            },
                            formatter: function(datas)
                              {
                                  var res = datas[0].name + '<br/>', val;
                                  for(var i = 0, length = datas.length; i < length; i++) {
                                        val = (datas[i].value) + '%';
                                        res += datas[i].seriesName + '：' + val + '<br/>';
                                    }
                                    return res;
                               }
                        },
                        // grid: [
                        //     {x: '7%', y: '7%', width: '38%', height: '38%'},
                        // ],
                        xAxis: {
                            data: emotion_name
                        },
                        yAxis: {},
                        series: [
                            {
                                name: '预测值',
                                type: 'bar',
                                itemStyle: {
                                    normal: {
                                        //好，这里就是重头戏了，定义一个list，然后根据所以取得不同的值，这样就实现了，
                                        color: function (params) {
                                            // build a color map as your need.
                                            var colorList = [
                                                '#26C0C0', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                                            ];
                                            return colorList[params.dataIndex]
                                        }
                                    }
                                },
                                data: value
                            },
                            {
                                type: 'pie',
                                itemStyle: {
                                    normal: {
                                        //好，这里就是重头戏了，定义一个list，然后根据所以取得不同的值，这样就实现了，
                                        color: function (params) {
                                            // build a color map as your need.
                                            var colorList = [
                                                '#26C0C0', '#B5C334', '#FCCE10', '#E87C25', '#27727B',
                                                '#FE8463', '#9BCA63', '#FAD860', '#F3A43B', '#60C0DD',
                                                '#D7504B', '#C6E579', '#F4E001', '#F0805A', '#26C0C0'
                                            ];
                                            return colorList[params.dataIndex]
                                        }
                                    }
                                },
                                data: [
                                    {value:value[0],name:emotion_name[0]},
                                    {value:value[1],name:emotion_name[1]},
                                    {value:value[2],name:emotion_name[2]},
                                    {value:value[3],name:emotion_name[3]},
                                    {value:value[4],name:emotion_name[4]},
                                    {value:value[5],name:emotion_name[5]},
                                    {value:value[6],name:emotion_name[6]}
                                ],
                                radius:'40%',
                                center:['75%','30%']
                            }
                            ]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart.setOption(option);
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });

        }
        else if(data.index===4)
        {
            $.ajax({
                url: "/get_poemtime_about_poem",
                type: "POST",
                data:{"poem_name":poem_name},
                dataType: "json",
                async: true,
                success: function (res) {
                    text="<div class='layui-row'>" +
                        "                                            <ul class='layui-timeline'>";
                    for(var i=0;i<res.length;i++)
                    {
                        time=res[i].time;
                        back=res[i].back;
                        title=res[i].title;
                        content=res[i].content;
                        text+="<li class='layui-timeline-item'>" +
                            "                                                    <i class='layui-icon layui-timeline-axis'></i>" +
                            "                                                    <div class='layui-timeline-content layui-text'>" +
                            "                                                      <h3 class='layui-timeline-title'>"+time+"</h3>" +
                            "                                                      <div class='layui-card-body' id='shown'>" +
                            "                                                        "+back+"" +"<br>"+"<p id='poem_content'>"+title+"</p>";
                        for(var k=0;k<content.length;k++)
                        {
                            text+="<p id='poem_content'>"+content[k]+"</p>";
                        }
                        text+=
                            "                                                      </div>" +
                            "                                                    </div>" +
                            "                                                  </li>";
                    }
                    text+="</ul>" +
                        "                                        </div>";
                    $("#poem_tab").html(text);
                    layer.close(index);
                },
                error: function (e) {
                    alert("出现错误！！");
                }
            });
        }

    });





});
