// use setInterval to send a request to the server to check if there are any 
// new posts, every 1 minute = 60,000 milliseconds 

let latestPostTimestamp = 0;

function createLatestTimestamp(posts) {
    const maxTimestamp = Math.max(...posts.map(post => post.timestamp));

    latestPostTimestamp = maxTimestamp
};
// asynchronous request to '/api/latest-posts' 
function checkForPosts() {
    console.log('Checking for posts');
    fetch('/api/latest-posts')
        .then(response => response.json())
        .then(data => {
            // log response
            console.log('Server Response:', data);
            // if latest_post is in the data object, it will be assigned to latestPosts
            // if it is undefined it will become an empty array
            const latestPosts = data.latest_posts || [];
            const maxTimestamp = Math.max(...latestPosts.map(post => post.timestmap));
            
            if (maxTimestamp > latestPostTimestamp) {
                console.log('new posts found!');
                latestPostTimestamp = maxTimestamp;

                displayNewPosts(latestPosts)
            } else {
                console.log('no new posts')
            }
        
        })
        .catch(error => {
            console.error('Error fetching new posts:', error);
        });
};


function displayNewPosts(newPosts) {
    console.log('Displaying new posts:', newPosts);
    
    const timelineFeed = document.getElementById('timeline')

    newPosts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.innerHTML = `
        <div class='postblock'>
            username: ${post.user.screenname}</p>
            body: ${post.body}
            time: ${post.timestamp}
            Post_id: ${post.post_id}
        </div>
        `;
        // use prepend to add new posts to the beginning (top)
        timelineFeed.prepend(postElement);
    });
}


setInterval(() => {
    checkForPosts();
}, 60000);


document.getElementById('load-new-posts-button').addEventListener('click', () => {
    // check if the right button is being selected
    console.log('Button clicked');
    checkForPosts();
});


// create reply and create likes for posts/likes functions

// for reply form under each post 
// select by class is .classname
// document.querySelectorAll('.createreply')  = is a NodeList so it needs forEach
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
            document.querySelector(evt.target.document.querySelector('#postid')
                                    .value).insertAdjacentHTML(`${reply}`)
        })
});

// for liking a post 
document.querySelectorAll('.likeapost').addEventListener('submit', (evt) => {
    evt.preventDefault();

    evt.target.document.querySelector('#likepostid').value

    // fetch('/like-post')
    //     .then((response) => response.text())
    //     .then((like) => {
            
    //     })

});

// for liking a reply
document.querySelectorAll('.likeareply').addEventListener('submit', (evt) => {
    evt.preventDefault();

    evt.target.document.querySelector('#likereplyid').value

});