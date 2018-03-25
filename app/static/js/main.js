
    function onDelete(postid) {
        if (confirm("Are You sure?")) {
            window.location.href = "/posts/delete/"+postid;
        }
    }
