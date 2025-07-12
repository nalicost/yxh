let i = 0
const btn = document.querySelectorAll('.btn')
const text = document.querySelectorAll('.content-1-1-bottom')
const tp = document.querySelectorAll('.content-1-1-top')//top被占用了
let timer = setInterval(function () {
    if(i<6){
        btn[i].classList.remove('active')
        btn[i+1].classList.add('active')
        text[i].classList.remove('active-text')
        text[i+1].classList.add('active-text')
        tp[i].classList.remove('active-text')
        tp[i+1].classList.add('active-text')
        i++
    }
    else{
        btn[6].classList.remove('active')
        text[6].classList.remove('active-text')
        tp[6].classList.remove('active-text')
        i=0
        btn[0].classList.add('active')
        text[0].classList.add('active-text')
        tp[0].classList.add('active-text')
    }
}, 3000)
const img = document.querySelector('.content>img')
img.addEventListener('mouseenter',function(){
    clearInterval(timer)
})
img.addEventListener('mouseleave',function(){
    timer = setInterval(function () {
    if(i<6){
        btn[i].classList.remove('active')
        btn[i+1].classList.add('active')
        text[i].classList.remove('active-text')
        text[i+1].classList.add('active-text')
        tp[i].classList.remove('active-text')
        tp[i+1].classList.add('active-text')
        i++
    }
    else{
        btn[6].classList.remove('active')
        text[6].classList.remove('active-text')
        tp[6].classList.remove('active-text')
        i=0
        btn[0].classList.add('active')
        text[0].classList.add('active-text')
        tp[0].classList.add('active-text')
    }
}, 3000)
})
for(let j=0;j<btn.length;j++){
    btn[j].addEventListener('click',function(){
        btn[i].classList.remove('active')
        btn[j].classList.add('active')
        text[i].classList.remove('active-text')
        text[j].classList.add('active-text')
        tp[i].classList.remove('active-text')
        tp[j].classList.add('active-text')
        i=j
    })
}

