$(document).ready(function() {
    var usermenu = document.querySelector(".menuContainer")
    var closeandopen = document.querySelector(".openandclosebtn")
    var menudetils = document.querySelector('.menudetils')
    var shortcuts = document.querySelector('.shortcuts')

    $(closeandopen).click(function(){
        if (closeandopen.innerHTML === '<i class="fa-solid fa-bars" style="color: #ffffff;"></i>') {
            closeandopen.innerHTML = ''
            closeandopen.innerHTML = '<i class="fa-solid fa-xmark" style="color: #ffffff;"></i>'

        }else {
            closeandopen.innerHTML = '<i class="fa-solid fa-bars" style="color: #ffffff;"></i>'
        }
        $(usermenu).toggleClass("menutoggle")
        $(menudetils).toggleClass("menuContainerOpacity")
        $(shortcuts).toggleClass("shortcutsopacity")
    })
})