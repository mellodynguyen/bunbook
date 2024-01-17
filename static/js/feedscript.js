// const createPostBtn = document.querySelector('#createpost')

// createPostBtn.addEventListener('submit',)

// use setInterval to send a request to the server to check if there are any 
// new posts, every 1 minute = 60,000 milliseconds 

// function checkForPosts()


// setInterval(checkForPosts, 60000)





// for reply form under each post 
// select by class is .classname
document.querySelectorAll('.createreply').addEventListener('submit', (evt) => {
    evt.preventDefault();

    // use event target to get particular form that was submitted
    evt.target.document.querySelector('#postid').value

    // fetch(route)
    fetch('/create-reply')
        // response done => response text
        .then((response) => response.text())
        .then((reply) => {
            // add reply to display 
            document.querySelector('.replyblock').insertAdjacentHTML(`${reply}`)
        })
})