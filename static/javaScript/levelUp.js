document.querySelector('#levelUp').addEventListener('click', function (e) {
    this.classList.add("active")
    document.querySelector('.levelUp_gif').classList.add("active")
    if (audio.played) {
        audio.play();
    }
    setTimeout(() => {  
        document.querySelector('.levelUp_gif').classList.remove("active")
    }, 10000);
    setTimeout(() => {  
        location.replace(url)
    }, 10300);
})