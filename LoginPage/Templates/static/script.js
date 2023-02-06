let username = document.getElementById("loginName");
let password = document.getElementById("loginPassword");
let flag = 1;
function validateForm(){
    /*Checking User Name validation*/
    if(username.value == ""){
        document.getElementById("userError").innerHTML = "User Name is empty";
        flag = 0;
    }else if(username.value.length<3){
        document.getElementById("userError").innerHTML = "User Name require minimum 3 characters";
        flag = 0;
    }
    else{
        document.getElementById("userError").innerHTML = "";
        flag = 1;
    }
    /*Checking Password validation*/
    if(password.value == ""){
        document.getElementById("passError").innerHTML = "Password is empty";
        flag = 0;
    }
    else{
        document.getElementById("passError").innerHTML = "";
        flag = 1;
    }
    if(flag){
        return true;
    }
    else{
        return false;
    }
}