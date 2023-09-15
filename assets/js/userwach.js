let adcontainer = document.querySelector(".adimageVideo")
let adcontainervideo = adcontainer.getElementsByTagName("video")
let adcontainervimg = adcontainer.getElementsByTagName("img")

if (adcontainervideo.length !== 0){
    forvideo()
}else if (adcontainervimg.length !== 0){
    console.log("salam")
    forimg()
}
function forvideo(){
    var advideo = document.getElementById("advideo")
    var startproject = document.querySelector(".startproject")
    var startbtn = document.getElementById("start")
    let timernum = null
    $(startbtn).hide()
    advideo.addEventListener("loadeddata", function (){
        $("#wait").hide()
        $("#start").show()
    })

    const url = window.location.href
    advideo.pause()
    var count;
    $(startbtn).click(function (e){
        e.preventDefault()
        var fd = new FormData()
        fd.append("start", "start")
        fd.append("csrfmiddlewaretoken", csrftoken)
        fd.append("adid", document.getElementById("adid").value)
        axios.post(url, fd)
            .then(
                res =>{
                    console.log("start")
                }
            )
            .catch(
                err =>{
                    console.log(err)
                }
            )
        advideo.play()
        startproject.style.background = "transparent";
        startbtn.style.display = "none";
        var timer = $('.timer');
        function clearCountdown(interval) {
            clearInterval(interval);
        }
        let flag = 1
        function timerfunc(timecount){
            let counttime = timecount
            count = setInterval(function(){
            if (counttime <= 0) {
                timer.html('تبلیغ برای شما ثبت شد!');
                var next = new FormData()
                next.append("next", "next");
                next.append("csrfmiddlewaretoken", csrftoken)
                next.append("adid", document.getElementById("adid").value)
                axios.post(url, next)
                    .then(
                        res =>{
                            console.log("Next Video")
                            window.location.href =  res.data.url
                        }
                    )
                    .catch(
                        err =>{
                            console.log("Error in Next")
                        }
                    )
                clearCountdown(count);
                } else {
                --counttime;
                timer.html(counttime);
                }
            }, 1000);

        }
        timerfunc(countdownBegin)
        let newcount = null
        setInterval(()=>{
            if(document.visibilityState === 'visible'){
                if(flag === 0){
                    advideo.play()
                    startproject.style.background = "transparent";
                    let returntab = new FormData()
                    returntab.append("csrfmiddlewaretoken", csrftoken)
                    returntab.append("return", "return")
                    axios.post(url, returntab)
                        .then(
                            res=>{
                                console.log("return")
                            }
                        ).catch(
                            err=>{
                                console.log(err)
                            }
                        )
                    flag = 1
                    clearInterval(timerfunc.count)
                    timerfunc(newcount)

                }
            }else if (document.visibilityState === "hidden"){
                if(flag === 1){
                    advideo.pause()
                    startproject.style.background = "rgba(0, 0, 0, 0.668)";
                    clearInterval(count)
                    let leave = new FormData()
                    leave.append("csrfmiddlewaretoken", csrftoken)
                    leave.append("leave", "leave")
                    axios.post(url, leave)
                        .then(
                            res=>{
                                console.log("Leave")
                            }
                        ).catch(
                            err=>{
                                console.log(err)
                            }
                        )
                    flag = 0
                    newcount = parseInt(timer.html())
                }
            }

        },1)

    })
    let reject = document.getElementById("reject")
    reject.addEventListener("click", function (e){
        e.preventDefault()
        let reject = new FormData()
        reject.append("csrfmiddlewaretoken", csrftoken)
        reject.append("reject", "reject")
        reject.append("adid", document.getElementById("adid").value)
        axios.post(url, reject)
            .then(
                res=>{
                    console.log("reject")
                    console.log(res.data.url)
                    window.location.href = res.data.url
                }
            ).catch(
                err=>{
                    console.log(err)
                }
            )
    })
}
function forimg(){
    var adimg = document.getElementById("adimg")
    var startproject = document.querySelector(".startproject")
    var startbtn = document.getElementById("start")
    let timernum = null

    const url = window.location.href
    var count;
    $(startbtn).click(function (e){
        e.preventDefault()
        var fd = new FormData()
        fd.append("start", "start")
        fd.append("csrfmiddlewaretoken", csrftoken)
        fd.append("adid", document.getElementById("adid").value)
        axios.post(url, fd)
            .then(
                res =>{
                    console.log("start")
                }
            )
            .catch(
                err =>{
                    console.log(err)
                }
            )
        startproject.style.background = "transparent";
        startbtn.style.display = "none";
        var timer = $('.timer');
        function clearCountdown(interval) {
            clearInterval(interval);
        }
        let flag = 1
        function timerfunc(timecount){
            let counttime = timecount
            count = setInterval(function(){
            if (counttime <= 0) {
                timer.html('تبلیغ برای شما ثبت شد!');
                var next = new FormData()
                next.append("next", "next");
                next.append("csrfmiddlewaretoken", csrftoken)
                next.append("adid", document.getElementById("adid").value)
                axios.post(url, next)
                    .then(
                        res =>{
                            console.log("Next Video")
                            window.location.href =  res.data.url
                        }
                    )
                    .catch(
                        err =>{
                            console.log("Error in Next")
                        }
                    )
                clearCountdown(count);
                } else {
                --counttime;
                timer.html(counttime);
                }
            }, 1000);

        }
        timerfunc(countdownBegin)
        let newcount = null
        setInterval(()=>{
            if(document.visibilityState === 'visible'){
                if(flag === 0){
                    startproject.style.background = "transparent";
                    let returntab = new FormData()
                    returntab.append("csrfmiddlewaretoken", csrftoken)
                    returntab.append("return", "return")
                    axios.post(url, returntab)
                        .then(
                            res=>{
                                console.log("return")
                            }
                        ).catch(
                            err=>{
                                console.log(err)
                            }
                        )
                    flag = 1
                    clearInterval(timerfunc.count)
                    timerfunc(newcount)

                }
            }else if (document.visibilityState === "hidden"){
                if(flag === 1){
                    startproject.style.background = "rgba(0, 0, 0, 0.668)";
                    clearInterval(count)
                    let leave = new FormData()
                    leave.append("csrfmiddlewaretoken", csrftoken)
                    leave.append("leave", "leave")
                    axios.post(url, leave)
                        .then(
                            res=>{
                                console.log("Leave")
                            }
                        ).catch(
                            err=>{
                                console.log(err)
                            }
                        )
                    flag = 0
                    newcount = parseInt(timer.html())
                }
            }

        },1)

    })
    let reject = document.getElementById("reject")
    reject.addEventListener("click", function (e){
        e.preventDefault()
        let reject = new FormData()
        reject.append("csrfmiddlewaretoken", csrftoken)
        reject.append("reject", "reject")
        reject.append("adid", document.getElementById("adid").value)
        axios.post(url, reject)
            .then(
                res=>{
                    console.log("reject")
                    console.log(res.data.url)
                    window.location.href = res.data.url
                }
            ).catch(
                err=>{
                    console.log(err)
                }
            )
    })
}