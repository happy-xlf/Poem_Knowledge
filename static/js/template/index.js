
layui.use(['layer','element','util','laypage'],function () {

    var $=layui.$,layer=layui.layer;
    var element=layui.element;
    util = layui.util;//引入util
    laypage=layui.laypage;

});


// show_name = function (name){
//     alert("成功啦！"+name);
// };

show_name = function(name) {
    alert(name);
    xadmin.add_tab_f('图谱','/author/'+name);
};
