function EditPost(postid){
    let form=document.querySelector('[data-postid="'+postid+'"]');
    form.querySelector("#contenttextarea").removeAttribute("disabled");
    form.classList.remove('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    

    document.querySelector('#editpostform').addEventListener('submit', (event)=>{
        event.preventDefault();
        let form=document.querySelector('#editpostform');
        const formData = new FormData(form);
        form.classList.add('hidden');
        
        let postid=form.getAttribute("data-postid");
        
        // $.post('/editpost/'+postid, {"newcontent":newcontent}, function(data){ 
        //     //$('.message').html(data.message);
        //     // of course you can do something more fancy with your respone
        //  });
         fetch('/editpost/'+postid, {
            method: 'POST',
            body: formData
          })
          .then(response => 
            {
                response.json()
            }).catch(error => {
                
                // we hope this code is never executed, but who knows?
                console.log(error);
            });
         form.querySelector("#contenttextarea").setAttribute("disabled","disabled");
        
    });

    
});

