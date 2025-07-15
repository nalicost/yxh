let sta = Number(location.search.split('?').join('').split('&')[0].split('=')[1])
let file_choose
const menuBar = document.querySelector('.left-menu-bar')
const coreBar = document.querySelector('.core-bar')
const tit = document.querySelector('.title')
const switchBtn = document.querySelector('.point-set')
const switchDecoration = document.querySelectorAll('.decoration-bar')
const files = document.querySelectorAll('.show')
const addFile = document.querySelector('.right-add-file')
const indexFile = document.querySelector('.right-file-index')
const switchBallBtn = document.querySelector('.ball-btn')
const lChoice = document.querySelector('.l-choice')
const rChoice = document.querySelector('.r-choice')
const switchFile = document.querySelector('.add-file')
const switchDoc = document.querySelector('.add-dir')

const title = {
    '1':'查询界面', 
    '-1':'添加界面'
} 
const showUI = {
    '1': addFile,
    '-1': indexFile
}
showUI[sta].classList.add('z-minus')
tit.innerText = title[sta]
menuBar.addEventListener('mouseenter', function(){
    this.style.width = '148px'
    switchDecoration[1].classList.remove('hidden')
    tit.classList.remove('hidden')
})
menuBar.addEventListener('mouseleave', function(){
    this.style.width = '68px'
    switchDecoration[1].classList.add('hidden')
    tit.classList.add('hidden')
})
switchBtn.addEventListener('click', function(){
    sta = -sta
    tit.innerText = title[sta]
    switchDecoration[0].classList.toggle('switch')
    switchDecoration[1].classList.toggle('switch')
    addFile.classList.toggle('z-minus')
    indexFile.classList.toggle('z-minus')
    coreBar.classList.toggle('change-bk-blue')
})

switchBallBtn.addEventListener('click', function(){
    this.classList.toggle('right-translate')
    lChoice.classList.toggle('hidden')
    rChoice.classList.toggle('hidden')
    switchDoc.classList.toggle('z-minus')
    switchFile.classList.toggle('z-minus')
})


// 初始化页面文件信息
get("/re_crtl/query_main/?file_mode=1", orign_genetate)

// 文件样式生成
function file_select(){
    const files = document.querySelectorAll(".show")
    for(let i=0;i<files.length;i++){
    files[i].addEventListener('click', function(){
        if (this.classList.contains('file-active')) {
            this.classList.remove('file-active');
            return;
        }
        for(let j=0;j<files.length;j++){
            files[j].classList.remove('file-active')
        }
        this.classList.add('file-active')
    })
}
}

// 文件元素生成服务器信息返回处理回调
function orign_genetate(data){
    const filesName = data.filesArr
    for(let i=0;i<filesName.length;i++){
        addElement(clsArr=["show"], wrapEleSel='#files>.wrapper', filesName[i])
    }
    file_select()
}


//删除
const delBtn = document.querySelector('.delete')

delBtn.addEventListener('click',function(){
    const file=document.querySelector(".file-active")
    if(!file){
        alert('请先选择文件')
        return
    }
    else{
        const fileName = file.innerText
        const route = document.querySelector(".cont-relative-path").innerText
        const page = document.querySelector('#pageId').value
        get(`/re_crtl/del/?file_name=${route + fileName}&file_page=${page}`, param_delete)

    }
})

// 文件删除服务器信息回调处理
function param_delete(data){
    if(data.code === 1){
        alert('删除成功')
        document.querySelector("#files>.wrapper").innerHTML = ''
        orign_genetate(data)
    }
    else{
        alert('删除失败')
    }
}
// 查看
const indexBtn = document.querySelector('.seek')
indexBtn.addEventListener('click', function(){
    const file=document.querySelector(".file-active")
    if(!file){
        alert('请先选择文件')
        return
    }else{
        const fileName = file.innerText
        const route = document.querySelector(".cont-relative-path").innerText
        get(`/re_crtl/query_main/?file_mode=2&file_name=${route + fileName}`, param_forward)
    }
})


// 文件查看服务器信息回调处理
function param_forward(data){
    if(data.code === 1){
        document.querySelector("#files>.wrapper").innerHTML = ''
        const path = document.querySelectorAll(".cont-relative-path")
        document.querySelector('#pageId').value = 1
        for(let i=0;i<path.length;i++){
            path[i].innerText = data.newLayer
            path[i].style.width = getTextWidth(data.newLayer, 'normal 18px STZhongsong') + 'px'
        }
        orign_genetate(data)
    }else if(data.code===2){
        document.querySelector("#files>.wrapper").innerHTML = data.fileCon
        const path = document.querySelectorAll(".cont-relative-path")
        for(let i=0;i<path.length;i++){
            path[i].innerText = data.newLayer
            path[i].style.width = getTextWidth(data.newLayer, 'normal 18px STZhongsong') + 'px'
        }     
        // 生成展示文件内容元素
        addElement(clsArr=["file"], wrapEleSel='#files>.wrapper', '', 'iframe')
        for(let i=0;i<data.fileTags.length;i++){
            addElement(clsArr=['tag'], '.tag-set', content=data.fileTags[i])
        }
        const ifrDoc = document.querySelector('iframe').contentWindow.document
        ifrDoc.write(data.fileCon)
    }
}

// 返回
const retBtn = document.querySelector('.return')
retBtn.addEventListener('click', function(){
    const patBarText = document.querySelector('.cont-relative-path').innerText
    if(patBarText === '/'){
        alert('已在根目录')
        return
    }
    document.querySelector('.tag-set').innerHTML = ''
    get(`/re_crtl/query_main/?file_mode=3&path_cur=${patBarText}`, returnPreviousLayer)
})

// 处理返回逻辑中服务器返回的数据
function returnPreviousLayer(data){
    const patBars = document.querySelectorAll('.cont-relative-path')
    for(let i=0;i<patBars.length;i++){
        patBars[i].style.width = getTextWidth(data.pathInfo, 'normal 18px STZhongsong') + 'px'
        setTimeout(()=> {
            patBars[0].innerText = data.pathInfo
            patBars[1].innerText = data.pathInfo
        }, 500)
        document.querySelector("#files>.wrapper").innerHTML = ''
        orign_genetate(data)
    }
    document.querySelector('#pageId').value = 1
}


// 处理上一页页码跳转
const perPage = document.querySelector('.last')
perPage.addEventListener('click', function(){
    const pageIt = document.querySelector('#pageId')
    if(pageIt.value === '1'){
        alert('没有上一页了')
        return
    }
    pageIt.value = +pageIt.value - 1
    const route = document.querySelector('.cont-relative-path').innerText
    get(`/re_crtl/query_main/?file_mode=4&file_path=${route}&file_page=${pageIt.value}`, prePageSwitch)
})

// 上一页切换逻辑
function prePageSwitch(data){
    document.querySelector("#files>.wrapper").innerHTML = ''
    orign_genetate(data)
}


// 处理下一页页码跳转
const aftPage = document.querySelector('.next')
aftPage.addEventListener('click', function(){
    const pageIt = document.querySelector('#pageId')
    pageIt.value = +pageIt.value + 1
    const route = document.querySelector('.cont-relative-path').innerText
    get(`/re_crtl/query_main/?file_mode=4&file_path=${route}&file_page=${pageIt.value}`, aftPageSwitch)
})


// 下一页切换逻辑
function aftPageSwitch(data){
    if(data.code === 1){
        document.querySelector("#files>.wrapper").innerHTML = ''
        orign_genetate(data)
    }else{
        document.querySelector('#pageId').value -= 1
        alert('已经在最后一页了')
    }
}

//上传文件夹
const fileUpload = document.querySelector('.confirm')
fileUpload.addEventListener('click', function(){
    const isNotDir = document.querySelector('.add-dir.z-minus')
    if(!isNotDir){
        const dirName = document.querySelector('.dir-name>input')
        if(dirName){
            const reg = /^[a-z]{3,8}$/
            if(!reg.test(dirName.value)){
                alert('请输入3-8位小写字母')
                return
            }
            else{
                const route = document.querySelector('.cont-relative-path').innerText 
                post(`/re_crtl/upload/?add_mode=1&file_path=${route}`, {
                    dir_name: dirName.value
                }, successUpload)
            }
        }
        else{
            alert('请输入内容')
            return
        }
    }
    else{
        const dirOnlyFile = document.querySelector('.upload-param-file>input').value
        const tagIt = document.querySelector('.upload-tag>input').value
        const route = document.querySelector('.cont-relative-path').innerText
        if(dirOnlyFile && tagIt){
            post(`/re_crtl/upload/?add_mode=2&file_path=${route}`, {
                'file_name': dirOnlyFile,
                'tag_sel': tagIt
            },successUpload)
        }
        else{
            alert('请输入内容')
            return
        }
    }
})
function successUpload(data){
    if(data.code === 1){
        alert('标签新增成功')
    }
    else if(data.code === 2){
        alert('文件新增标签成功')
    }
    else if(data.code === 3){
        alert('该路径无法新增标签或为文件增加标签')
    }
    else{
        alert('文件或标签不存在')
    }
}

//返回查询界面键
const retQuery = document.querySelector('.back')
retQuery.addEventListener('click', function(){
    switchBtn.click()
})
