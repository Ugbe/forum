function deleteNote(noteId) {
    fetch("/delete-note", {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
    window.location.href = "/mynotes";
    });
}

function deletePost(postId) {
    fetch("/delete-post", {
        method: 'POST',
        body: JSON.stringify({ postId: postId }),
    }).then((_res) => {
    window.location.href = "/forum";
    });
}

function likePost(postId) {
const likeCount = document.getElementById("likes-count-${postId}");
const likeButton = document.getElementById("like-button-${postId}");

    fetch('/like-post/${postId}', {method: "POST"})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
            likeButton.className = "fas fa-thumbs-up";
        } else {
            likeButton.className = "far fa-thumbs-up";
        }
    })
    .catch((e) => alert("Could not like post."));
}