
$(document).ready(function(){
    $(".images").click(function(event){
        var val = event.target.parentElement
        // console.log(val.getAttribute("src"))
        console.log(val)
    });
    $("#dropdownNavbarLink").click(function(){
        var navbar = document.getElementById("dropdownNavbar");
        if (navbar.style.display == "")
        {
            console.log("yes")
            navbar.style.display = "block"
        }
        else
        navbar.style.display = ""
        
    })
})
