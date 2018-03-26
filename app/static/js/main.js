
function onDelete(postid, curl) {
    if (confirm("Are You sure?")) {
        window.location.href = curl+postid;
    }
}