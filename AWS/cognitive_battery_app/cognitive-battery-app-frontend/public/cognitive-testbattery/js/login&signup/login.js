function login()
{   
    var username=document.getElementById("username").value;
    sessionStorage.setItem("username", username);
    let data=sessionStorage.getItem("username");
    //alert(data);
    window.location.href = "../cognitive-testbattery/include/main.html";
    return username;    
}


