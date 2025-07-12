//实现视觉上的东西需要的
let sta = Number(location.search.split('?').join('').split('&')[0].split('=')[1])
const menuBar = document.querySelector('.left-menu-bar')
const coreBar = document.querySelector('.core-bar')
const tit = document.querySelector('.title')
const switchBtn = document.querySelector('.point-set')
const switchDecoration = document.querySelectorAll('.decoration-bar')
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

//初始化文件信息，拿到数据
get("/param_crtl/query_main/?file_all=1",param_success)

function file_select(){
    const files=document.querySelectorAll(".show")
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
//传文件和实现功能需要的


function param_success(data){
    const filesName=data.filesArr
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
        nAme=file.innerText
        route=document.querySelector(".cont-relative-path").innerText
        console.log(route)
        wholeRoute=`${route+nAme}`
        get("/param_crtl/query_main/?file_all=0&file_name="+wholeRoute,param_delete)

    }
})

function param_delete(data){
    if(data.code===1){
        document.querySelector("#files>.wrapper").innerHTML=''
        alert('删除成功')
        param_success(data)
    }
    else{
        alert('删除失败')
    }
}

