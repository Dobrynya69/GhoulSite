document.querySelector(".content").innerHTML += '<div id="ball" class="person"></div>'
document.querySelector(".content").innerHTML += '<div class="omg_text"></div>'
var ball = document.querySelector("#ball")
var counter = document.querySelector("#counter")
var omg_text_ = document.querySelector(".omg_text")
var exit_button = document.querySelector("#exit")
var width = ball.offsetWidth
var height = ball.offsetHeight
var user_height = $(document).height()
var user_width = $(document).width()
var scores = 0
var streak = 0
var clicked = true
var time = 2000
const global_time = 1300
const remove = el => el.parentElement.removeChild(el);

function set_pos(top, left) {
    ball.style.top = String(top) + "px"
    ball.style.left = String(left) + "px"
}

function set_url(scores) {
    exit_button.href = pk + "/" + token + "/" + scores +"/"
}

function getRandomInt(min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min + 1)) + min
}

function set_rand_pos() {
    ball.style.top = String(getRandomInt(0, user_height - height)) + "px"
    ball.style.left = String(getRandomInt(0, user_width - width)) + "px"
    
}

function omg_text(block, text) {
    omg_text_.innerHTML = '<b>' + text + '</b>'
    omg_text_.style.transition = '300ms'
    omg_text_.classList.add("active")
    
    setTimeout(() => {
        omg_text_.style.transition = '0ms'
        omg_text_.classList.remove("active")
    }, 300);
}

function end() {
    counter.innerHTML = "You have enough scores to level up!<br/>You can leave!"
    ball.style.display = "none"
}

ball.addEventListener('click', function (e) {
    
    
    if (ball.classList.contains("ghoul")) {
        clicked = false
        set_rand_pos()
        scores -= 100
        set_url(scores)
        streak = 0
        time = 2000
        omg_text(ball, "GHOUL! +100!")
        set_url(scores)
        counter.innerHTML = "Eat a man!<br/>Or ghoul?<br/>Scores: -" + scores + "<br/>Streak: " + streak
    }
    else{
        clicked = true
        scores += 7 * streak
        set_url(scores)
        streak++
        counter.innerHTML = "Eat a man!<br/>Or ghoul?<br/>Scores: -" + scores + "<br/>Streak: " + streak
        if (need_scores - scores <= 0) {
            end()
        }
        if (global_time - streak * 100 <= 500) {
            time = global_time - streak * 70
        }
        set_rand_pos()
        omg_text(ball, "-7 " * streak)
        var streak_at_time = streak
        setTimeout(() => {
            if (streak_at_time == streak) {
                if (ball.classList.contains("ghoul")) {
                    ball.classList.remove('ghoul')
                    ball.classList.add('person')
                    set_rand_pos()
                    scores += 7 * streak
                    set_url(scores)
                    streak++
                    omg_text(ball, "-7 " * streak)
                    counter.innerHTML = "Eat a man!<br/>Or ghoul?<br/>Scores: -" + scores + "<br/>Streak: " + streak
                    if (need_scores - scores <= 0) {
                        end()
                    }
                }
                else{
                    clicked = false
                    set_rand_pos()
                    streak = 0
                    time = 2000
                    omg_text(ball, "TOO LATE!")
                    counter.innerHTML = "Eat a man!<br/>Or ghoul?<br/>Scores: -" + scores + "<br/>Streak: " + streak                    
                }
            }  
        }, time);
    }
    var what = getRandomInt(0, 4)
    if (what == 0) {
        ball.classList.remove('person')
        ball.classList.add('ghoul')
    }
    else{
        ball.classList.remove('ghoul')
        ball.classList.add('person')
    }
})

set_pos((user_height / 2) - (height / 2),  (user_width / 2) - (width / 2))

var myInterval = setInterval(function() {
    if (!clicked){
        set_rand_pos()
        streak = 0
        time = global_time
        counter.innerHTML = "Eat a man!<br/>Or ghoul?<br/>Scores: -" + scores + "<br/>Streak: " + streak
        var what = getRandomInt(0, 5)
        if (what == 0) {
            ball.classList.remove('person')
            ball.classList.add('ghoul')
        }
        else{
            ball.classList.remove('ghoul')
            ball.classList.add('person')
        }
    }
}, global_time);


