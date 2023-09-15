let file = document.getElementById("id_adfile")
let id_time = document.getElementById("id_time")
file.addEventListener("change", function (){
    let adfile = file.files[0]
    if (adfile.name.endsWith(".mp4")){
        const video = document.createElement("video")
        video.src = URL.createObjectURL(adfile)
        video.addEventListener("loadedmetadata", function (){
            id_time.value = parseInt(video.duration)
        })
    }
})