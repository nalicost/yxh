function get(url, successFunction= function (data){}, asyncio=true, errorData=''){
    /*
        get上传或获取


        url: 要访问的url地址
        successFunction: 成功后的回调函数，要求只能接受一个json字符串格式的参数
        asyncio:是否异步
        errorData:报错的信息

        return: 如果同步会返回服务器传回的json信息
    */
    let reData
    const xhr = new XMLHttpRequest()
    xhr.open('get', url, asyncio)
    if(asyncio){
        xhr.onerror = () => alert(errorData)
        xhr.onload = function () {
            reData = JSON.parse(this.responseText)
            successFunction(reData)
        }
    }else{
        return JSON.parse(xhr.responseText)
    }
    xhr.send(null)
}


function post(url, jsObj,successFunction = function (data){}, asyncio=true, errorData='') {
    /*
        非文件post上传或获取


        url: 要访问的url地址
        jsObj: 要送给后端的提交内容，js对象
        successFunction: 成功后的回调函数，要求只能接受一个json字符串格式的参数
        asyncio:是否异步
        errorData:报错的信息

        return: 如果同步会返回服务器传回的json信息
    */
    let reData
    const xhr = new XMLHttpRequest()
    xhr.open('post', url, asyncio)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    let data = ''
    for (let k in jsObj) {
        let piece = `${k}=${jsObj[k]}&`
        data = data + piece
    }
    if (asyncio) {
        xhr.onerror = () => alert(errorData)
        xhr.onload = function () {
            reData = JSON.parse(this.responseText)
            successFunction(reData)
        }
    }else{
        return JSON.parse(xhr.responseText)
    }
    xhr.send(data)
}


function postFile(url, fileObj, successFunction = function (data){}, asyncio=true, errorData=''){
    /*
        文件post上传或获取


        url: 要访问的url地址
        fileObj: 要送给后端的文件，文件对象
        successFunction: 成功后的回调函数，要求只能接受一个json字符串格式的参数
        asyncio:是否异步
        errorData:报错的信息

        return: 如果同步会返回服务器传回的json信息
    */
    let reData
    const xhr = new XMLHttpRequest()
    xhr.open('post', url, asyncio)
    let data = new FormData()
    data.append('fileObj', fileObj)
    if (asyncio) {
        xhr.onerror = () => alert(errorData)
        xhr.onload = function () {
            reData = JSON.parse(this.responseText)
            successFunction(reData)
        }
    }else{
        return JSON.parse(xhr.responseText)
    }
    xhr.send(data)
}


function creEle(clsArr, typ='div'){
    const newEle = document.createElement(typ)
    for(let i=0;i<clsArr.length;i++){
        newEle.classList.add(clsArr[i])
    }
    return newEle
}


function addElement(clsArr, wrapEleSel, content="",typ='div'){
    /*
        生成元素，增加类与文本内容并放入某个元素内

        typ: 需要生成的标签
        clsArr: 需要增加的类的数组
        wrapEleSel: 包裹的元素选择器

    */
    const newEle = document.createElement(typ)
    const wrapEle = document.querySelector(wrapEleSel)
    for(let i=0;i<clsArr.length;i++){
        newEle.classList.add(clsArr[i])
    }
    newEle.innerText=content
    wrapEle.appendChild(newEle)
}


function generatePoint(x, y){
    /*
        生成点

        x: 横坐标
        y: 纵坐标
    */
    const point = document.createElement('div')
    point.classList.add('point')
    point.style.left = x + 'px'
    point.style.top = y + 'px'
    map.appendChild(point)
}


function generateLine(pos_arr){
    /*
        生成线

        pos_arr: 两个点的坐标集
    */
    const line = document.createElement('div')
    const pos_vec = switchVec(pos_arr[0], pos_arr[1])
    line.classList.add('line')
    line.style.width = calLen(pos_arr[0], pos_arr[1]) + 'px'
    line.style.rotate = calAng(pos_vec) + 'deg'
    line.style.left = pos_arr[0][0] + 'px'
    line.style.top = pos_arr[0][1] + 'px'
    map.appendChild(line)
}


function calPos(longitude, latitude){
    /*
        经纬度换算坐标

        longitude: 经度
        latitude: 维度

        return: 返回坐标
    */
    const x = (longitude - x_start) / x_range * 600
    const y = (latitude - y_start) / y_range * 400
    return [x, y]
}


function calLen(pos_p, pos_a){
    /*
        计算两个点之间的距离

        pos_p: 第一个点
        pos_a: 第二个点

        return: 返回长度
    */
    return  Math.sqrt(Math.pow(pos_p[0] - pos_a[0], 2) + Math.pow(pos_p[1] - pos_a[1], 2))
}


function switchVec(pos_p, pos_a){
    /*
        两点转换向量

        pos_p: 起始点
        pos_a: 终止点

        return: 返回向量
    */
    return [pos_a[0] - pos_p[0], pos_a[1] - pos_p[1]]
}


function calAng(vec){
    /*
        计算向量的角度

        vec: 需要计算角度的向量

        return: 返回角度
    */
    const len_vec = calLen(vec, [0, 0])
    return Math.acos(vec[0] /  len_vec) / Math.PI * 180
}


function getTextWidth(text, font) {
  // re-use canvas object for better performance
  var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement("canvas"));
  var context = canvas.getContext("2d"); 
  context.font = font;
  var metrics = context.measureText(text);
  return metrics.width;
}