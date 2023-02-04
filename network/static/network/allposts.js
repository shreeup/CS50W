document.addEventListener('DOMContentLoaded', () => {
document.addEventListener('click', (event)=>{
    const btnobj=event.target;
    if(btnobj.classList.contains("likeactionbutton") 
    && btnobj.tagName.toLowerCase() === 'button')
    {
        btnobj.setAttribute('disabled','disabled');
        
        let postid=btnobj.getAttribute("data-postid");
        
    
        fetch('/likeaction/'+postid)
        .then(response => response.text())
            .then(text => {
                debugger;
                result = JSON.parse(text)
                document.querySelectorAll('#likecount_'+postid)[0].textContent=result.likecount;
                btnobj.innerHTML=result.liketext;
                console.log(result);
            })
            .catch(error => {
                
                console.log(error);
            });
            btnobj.removeAttribute('disabled');
    }
});


});