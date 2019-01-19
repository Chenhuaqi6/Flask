/**
 * Created by tarena on 19-1-5.
 */
function createXhr() {
    var xhr = null;
    //判断浏览器对xhr的支持性
    if(window.XMLHttpRequest){
        xhr = new XMLHttpRequest();

    }else{
        xhr = new ActiveXObject('Microsoft.XMLHTTP');
    }
        return xhr;
    }