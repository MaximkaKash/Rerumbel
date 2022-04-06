const min_header = document.getElementById('min_menu')
const burger = document.getElementById('burger')

const header_club = document.getElementById('header_club')
const menu_item = document.getElementById('menu_item')



function club_start() {
   

    burger.onclick=()=>{
        if(min_header.style.display=="none"){
            min_header.style.display="block";
    
        }
        else{
            min_header.style.display="none";
    
        }
    }

    header_club.onmouseover=()=>{
        
        menu_item.style.display="block";
        
    }

    header_club.onmouseout=()=>{
        
        menu_item.style.display="none";
        
    }

    menu_item.onmouseover=()=>{
        
        menu_item.style.display="block";
        
    }

    menu_item.onmouseout=()=>{
        
        menu_item.style.display="none";
        
    }
   
}





/*----------------------------------------------------------------------------------------------*/

club_start();
