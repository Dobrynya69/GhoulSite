buttons = document.querySelectorAll(".invite_button")
message = document.querySelector(".message")
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function (e) {
        e.preventDefault();
        var action_url = $(this).attr("href")
        $.ajax({
            type: "GET",
            url: action_url,
            contentType: false,
            processData: false,
            success: function(response){
                if (response['message']) {
                    message.classList.remove('active')
                    setTimeout(() => {
                        message.classList.add('active')
                    }, 300);
                    message.innerHTML = response['message']
                    setTimeout(() => {
                        message.classList.remove('active')
                    }, 5000);
                }else{
                    message.classList.remove('active')
                    setTimeout(() => {
                        message.classList.add('active')
                    }, 300);
                    message.innerHTML = 'Please login!'
                    setTimeout(() => {
                        message.classList.remove('active')
                    }, 5000);
                }
                
            }
        })
    })
    
}