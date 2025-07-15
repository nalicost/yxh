const btns = document.querySelectorAll('.btn')
const msgs= document.querySelectorAll('.msg')
for(let i=0;i<btns.length;i++){
    btns[i].addEventListener('mouseenter', function(){
        if(this != document.querySelector('.active')){
            for(let j=0;j<btns.length;j++){
                btns[j].classList.remove('active')
                msgs[j].classList.remove('active-text')
            }
            btns[i].classList.add('active')
            msgs[i].classList.add('active-text')    
        }
    })
}
