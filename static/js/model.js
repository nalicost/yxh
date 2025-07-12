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
        file_choose = this
    })
}
