"use strict";
// use setInterval to send a request to the server to check if there are any 
// new posts, every 1 minute = 60,000 milliseconds 

let latestPostTimestamp = 0;

function createLatestTimestamp(posts) {
    const maxTimestamp = Math.max(...posts.map(post => new Date (post.timestamp).getTime()));

    latestPostTimestamp = maxTimestamp
};
// asynchronous request to '/api/latest-posts' 
function checkForPosts() {
    console.log('Checking for posts');
    fetch('/api/latest-posts')
        .then(response => response.json())
        .then(data => {
            // console.log('Server Response:', data);
            // if latest_post is in the data object, it will be assigned to latestPosts
            // if it is undefined it will become an empty array
            const latestPosts = data.latest_posts || [];
            
            const newPosts = latestPosts.filter(post => new Date(post.timestamp).getTime() > latestPostTimestamp);
            // const newPosts = latestPosts.filter(post => post.timestamp > latestPostTimestamp);

            if (newPosts.length > 0) {
                // console.log('new posts found!');
                // latestPostTimestamp = maxTimestampClient;
                latestPostTimestamp = Math.max(...latestPosts.map(post => new 
                    Date(post.timestamp).getTime()));
                displayNewPosts(newPosts);
            } else {
                // console.log('no new posts')
            }
        
        })
        .catch(error => {
            console.error('Error fetching new posts:', error);
        });
};


function displayNewPosts(newPosts) {
    // console.log('Displaying new posts:', newPosts);
    
    const timelineFeed = document.getElementById('timeline')

    newPosts.forEach(post => {
        const postElement = document.createElement('div');
        
        postElement.innerHTML = `
        <div class='postblock'>
            username: ${post.user.screenname}</p>
            <br>
            body: ${post.body}
            <br>
            time: ${post.timestamp}
            Post_id: ${post.post_id}
        </div>
        `;
        // use prepend to add new posts to the beginning (top)
        timelineFeed.prepend(postElement);
    });
}

// Initialize latestPostTimestamp when the page loads
window.onload = () => {
    fetch('/api/latest-posts')
        .then(response => response.json())
        .then(data => {
            const latestPosts = data.latest_posts || [];
            createLatestTimestamp(latestPosts);
        })
        .catch(error => {
            console.error('Error fetching initial posts:', error);
        });
};

setInterval(() => {
    checkForPosts();
}, 60000);

// load new posts button
// document.getElementById('load-new-posts-button').addEventListener('click', () => {
//     // check if the right button is being selected
//     console.log('Button clicked');
//     checkForPosts();
// });

// for creating a reply
const replybuttons = document.querySelectorAll(".createreply")

for (const replybutton of replybuttons) {
    replybutton.addEventListener("submit", (evt) => {

        evt.preventDefault();

        const reply_post_id = evt.target.getAttribute("data-postid");
        // console.log(reply_post_id)

        const reply_body = evt.target.querySelector(".replyarea").value
        // console.log(reply_body)

        const reply_object = {post_id: reply_post_id, body: reply_body}

        fetch('/create-reply', {
            method: 'POST',
            body: JSON.stringify(reply_object),
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then((response) => response.json())
            .then((responseJson) => { 
                // console.log(responseJson)
                // put reply into hidden reply div
                // change the text area back to default
                // implement a replies counter that will dynamically change as well
                document.querySelector.innerHTML = 'Reply!'
                
            })
    })
};

// for liking a post 
// create a variable to store all the selected elements
//  this creates a list of HTML elements
const likebuttons = document.querySelectorAll(".likeapost");

// throw it [the elements] into a for loop
for (const likebutton of likebuttons) {
    // for each button we want to add an event listener
    likebutton.addEventListener('submit', (evt) => {
        // we need the event target so we need (evt) and need to cancel default
        evt.preventDefault();
        // we want to grab the value from the input
        // console.log(document.querySelector('#likepostid')) 
        // selecting by #likepostid is wrong because piles of input have same ID

        // console.log(evt.target)
        // this will get the event object (form [which contains value])
        const like_post_id = evt.target.getAttribute('data-postid');
        // console.log(like_post_id)

        // take value that we grabbed, tuck into object so we can tuck it into
        const like_object = {
            post_id: like_post_id
        }
        // fetch request, this will be a POST request [post because we are sending info]
        fetch('/like-post', {
            method: 'POST',
            body: JSON.stringify(like_object),
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then((response) => response.json())
            .then((responseJson) => {
                // console.log(responseJson)
                // select finish line and update what's inside of it
                const likecounter = "#likecounter" + responseJson.post_id 
                // console.log(likecounter);
                // // this should say {num_likes: 3, post_id: 21}
                // console.log(responseJson);
                // setting the HTML displaying number of likes to the new count of likes
                document.querySelector(likecounter).innerHTML = `Likes: ${responseJson.num_likes}`
            })
    })
}


// for liking a reply
const replylikebuttons = document.querySelectorAll(".likeareply")

for (const replylikebutton of replylikebuttons) {
    replylikebutton.addEventListener('submit', (evt) => {
        evt.preventDefault();

        const like_reply_id = evt.target.getAttribute('data-replyid');
        console.log(like_reply_id)

        const reply_like_object = {
            reply_id: like_reply_id
        }
        
        fetch('/like-reply', {
            method: 'POST',
            body: JSON.stringify(reply_like_object),
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then((response) => response.json())
            .then((responseJson) => {
                // console.log(responseJson)
                const replylikecounter = "#replylikecounter" + responseJson.reply_id
                // console.log(replylikecounter)
                // console.log(responseJson)
                document.querySelector(replylikecounter).innerHTML = `Likes: ${responseJson.replynum_likes}`
            })
    })
}

// show/hide reply forms
// getElementsByClassName will get every element and the func will need
// to target a specific element 
// button inside for loop so buttons with same ID (cant share same ID) 
const replyButtons = document.querySelectorAll('.showreplies');
  function showHideReply(evt) {

    // console.log(evt.target.getAttribute('data-postid'))
    
    
    const postId = evt.target.getAttribute('data-postid');
    const replyDiv = document.getElementById(`replyblock-${postId}`);

    // console.log(replyDiv)

    if (replyDiv.style.display === "none" || replyDiv.style.display === "") {
      replyDiv.style.display = "block";
    } else {
      replyDiv.style.display = "none";
    }
  };

  for (const replyButton of replyButtons) {
    replyButton.addEventListener('click', showHideReply)
};


// function search for users 
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('search-input');
// const searchResults = document.getElementById('searchResults');
const searchResults = document.querySelector('.results-list')

// handler function for the listener, should take in etv (evt will get the sn)
function fetchUser(evt) {
    const screenname = evt.target.value
    
    // fetch route needs to match server route
    // fetchUser(screenname)
    return fetch(`/api/search/${screenname}`)
        .then(response => response.json())
        .then(data => {
            // console.log(data)
            // get the UL from the DOM  - /results-list
            // document.querySelector('.results-list')
            // clear out any existing results from prev. searches
            searchResults.innerHTML = '';
            // loop over data and add new li for each result
            for (let i = 0; i < data.length; i++) {
                const user = data[i];
                const resultItem = document.createElement('li');
                // resultItem.textContent = `${user.screenname}`;
                // searchResults.appendChild(resultItem);

                // create a link with href to user profile by using user_id
                const link = document.createElement('a');
                link.classList.add("search-user-url")
                link.href = `/user/${user.user_id}`;
                link.textContent = `${user.screenname}`;

                // add event listener to click link
                link.addEventListener('click', (event) => {
                    // Prevent default link behavior
                    event.preventDefault(); 
                    // Call a function to handle navigation
                    navigateToUserProfile(user.user_id); 
                });
                
                resultItem.appendChild(link);
                searchResults.appendChild(resultItem);
            }
            })
};

// searchForm add event listener
searchInput.addEventListener('input', fetchUser);


// Function to handle navigation to the user profile route
function navigateToUserProfile(userId) {
    // Redirect or navigate to the user profile route
    window.location.href = `/user/${userId}`;
};

const bunbookMascot = document.querySelector('.bunbook-mascot')

function changeMascot() {
    bunbookMascot.getAttribute('src');
    bunbookMascot.setAttribute('src', '../static/images/BunKnife.png');
};

bunbookMascot.addEventListener('mouseover', changeMascot);
