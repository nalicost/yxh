let sta = Number(location.search.split('?').join('').split('&')[0].split('=')[1])
let file_choose
const menuBar = document.querySelector('.left-menu-bar')
const coreBar = document.querySelector('.core-bar')
const tit = document.querySelector('.title')
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
switchBallBtn.addEventListener('click', function(){
    this.classList.toggle('right-translate')
    lChoice.classList.toggle('hidden')
    rChoice.classList.toggle('hidden')
    switchDoc.classList.toggle('z-minus')
    switchFile.classList.toggle('z-minus')
})



// 界面切换逻辑
function changePage(){
    sta = -sta
    tit.innerText = title[sta]
    switchDecoration[0].classList.toggle('switch')
    switchDecoration[1].classList.toggle('switch')
    addFile.classList.toggle('z-minus')
    indexFile.classList.toggle('z-minus')
    coreBar.classList.toggle('change-bk-blue')
}

// 返回
const retBtn = document.querySelector('.return')
retBtn.addEventListener('click', function(){
    const patBarText = document.querySelector('.cont-relative-path').innerText
    if(patBarText === '/'){
        alert('已在根目录')
        return
    }
    get(`/simulation_visible/query_main/?file_mode=3&path_cur=${patBarText}`, returnPreviousLayer)
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
    document.querySelector('#layer').value = 1
}


// 选择
const indexBtn = document.querySelector('.select')
indexBtn.addEventListener('click', function(){
    const file=document.querySelector(".file-active")
    if(!file){
        alert('请先选择文件')
        return
    }else if(document.querySelector('#layer').value >= 2){
        alert('超出层数')
        return
    }else{
        const fileName = file.innerText
        const route = document.querySelector(".cont-relative-path").innerText
        get(`/simulation_visible/query_main/?file_mode=2&file_name=${route + fileName}`, param_forward)
    }
})


// 文件选择服务器信息回调处理
function param_forward(data){
    if(data.code === 1){
        document.querySelector("#files>.wrapper").innerHTML = ''
        const path = document.querySelectorAll(".cont-relative-path")
        document.querySelector('#pageId').value = 1
        document.querySelector('#layer').value = 2
        for(let i=0;i<path.length;i++){
            path[i].innerText = data.newLayer
            path[i].style.width = getTextWidth(data.newLayer, 'normal 18px STZhongsong') + 'px'
        }
        orign_genetate(data)
    }else if(data.code===2){
        alert('非目录，无法选择')
    }
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
    get(`/simulation_visible/query_main/?file_mode=4&file_path=${route}&file_page=${pageIt.value}`, prePageSwitch)
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
    get(`/simulation_visible/query_main/?file_mode=4&file_path=${route}&file_page=${pageIt.value}`, aftPageSwitch)
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

// 初始化页面文件信息
get("/simulation_visible/query_main/?file_mode=1", orign_genetate)

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

//返回查询界面键
const retQuery = document.querySelector('.back')
retQuery.addEventListener('click', function(){
    changePage()
})

// 可视化
const visibleBtn = document.querySelector('.visible')
visibleBtn.addEventListener('click', function(){
    if(document.querySelector('#layer').value === '2'){
        const file = document.querySelector(".file-active").innerText
        const route = document.querySelector(".cont-relative-path").innerText
        get(`/simulation_visible/gen/?file_path=${route}&file_name=${file}&file_mode=1`, visibleSt)
    }else{
        alert('非模拟文件夹')
        return
    }
})

function visibleSt(data){
    if(data.code === 1){
        changePage()
    }
}