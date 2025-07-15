let sta = Number(location.search.split('?').join('').split('&')[0].split('=')[1])
let file_choose
const menuBar = document.querySelector('.left-menu-bar')
const coreBar = document.querySelector('.core-bar')
const tit = document.querySelector('.title')
const switchBtn = document.querySelector('.point-set')
const switchDecoration = document.querySelectorAll('.decoration-bar')
const files = document.querySelectorAll('.show')
const indexFile = document.querySelector('.right-file-index')



tit.innerText = '查询界面'
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

// 初始化页面文件信息
get("/model_crtl/query_main/?file_mode=1", orign_genetate)//笑死了，crtl,orign,genetate,0bj


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
        if(data.choose === filesName[i]){
            addElement(clsArr=["show"], wrapEleSel='.wrapper', filesName[i])
            const chooseModel = document.querySelector('#modelTitle')
            chooseModel.innerText = 'LLM:'+filesName[i]
        }
        else{
            addElement(clsArr=["show"], wrapEleSel='.wrapper', filesName[i])
        }
    }
    file_select()
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
    get(`/model_crtl/query_main/?file_mode=2&file_page=${pageIt.value}`, prePageSwitch)
})

// 上一页切换逻辑
function prePageSwitch(data){
    document.querySelector(".wrapper").innerHTML = ''
    orign_genetate(data)
}


// 处理下一页页码跳转
const aftPage = document.querySelector('.next')
aftPage.addEventListener('click', function(){
    const pageIt = document.querySelector('#pageId')
    pageIt.value = +pageIt.value + 1
    get(`/model_crtl/query_main/?file_mode=2&file_page=${pageIt.value}`, aftPageSwitch)
})


// 下一页切换逻辑
function aftPageSwitch(data){
    if(data.code === 1){
        document.querySelector(".wrapper").innerHTML = ''
        orign_genetate(data)
    }else{
        document.querySelector('#pageId').value -= 1
        alert('已经在最后一页了')
    }
}

//切换
const switchButn = document.querySelector('.change')
switchButn.addEventListener('click', function(){
    const switchAi = document.querySelector('.file-active')
    console.log(switchAi)
    if(!switchAi){
        alert('请先选择模型')
        return
    }
    else if(switchAi){
        get(`/model_crtl/query_switch/?switchAi=${switchAi.innerText}`, switchSuccess)
    }
})
function switchSuccess(data){
    if(data.code === 1){
        alert('切换成功')
        const chooseModel = document.querySelector('#modelTitle')
        chooseModel.innerText = 'LLM:'+data.text
    }
    else{
        alert('切换失败')
    }
}