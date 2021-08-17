document.addEventListener('DOMContentLoaded', function(e) { 
    like();

    // document.getElementById(`like-${id}`).className = localStorage.getItem("class")


})





function like(){ 

    const likebtn = document.querySelectorAll('.like');
    likebtn.forEach((btn) => { 
      
        btn.addEventListener("click", function(event) { 
            let id = event.target.id;
            id = id.substring(id.indexOf('-') + 1);
            console.log(id)

            fetch(`/like/${id}`, { 
                method: "PUT", 
                headers: { 
                    'X-CSRFToken': csrftoken,
             },
            })
                .then((response) => response.json())
                
                .catch((error) => console.log(error))
                .then( ()=> { 

                    var className = document.getElementById(`like-${id}`).getAttribute("class");
                    if(className == "like far fa-heart") { 
                        btn.className = "like fas fa-heart"
                    }
                    else{ 
                        btn.className = "like far fa-heart";
                    }

                    // //the above code works, but after i added the localStorage thing it doesn't
                    // //store
                    // localStorage.setItem("class", className);

                    // //Page Load 
                    // var iconClass = localStorage.getItem("class")
                    // if(iconClass){ 
                    //     document.getElementById(`like-${id}`).className = iconClass;
                    // }


                    

                    // if(btn.classList.contains('far')){ 
                        
                    //     btn.classList.toggle('fas')
                    // } else { 
                    //     btn.classList.toggle('far')
                    // }


                    
                    let get = document.getElementById(`count-${id}`);
                    let like = get.innerHTML;
                    console.log(like);


                    if(btn.classList.contains('fas')){ 
                        like++;
                        get.innerHTML = like;
                        
                     }else { 
                        like--;
                        get.innerHTML = like;
                    }

                })
            
        })

    })
        
} 

