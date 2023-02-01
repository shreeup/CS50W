document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', ()=> compose_email());
  document.querySelector('#compose-form').addEventListener('submit', submit_email);
  // By default, load the inbox
  load_mailbox('inbox');



});


function compose_email(recip,subject,body) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#detail-view').style.display = 'none';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recip??'';
  document.querySelector('#compose-subject').value = subject??'';
  document.querySelector('#compose-body').value = body??'';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';

  mailBox(mailbox);
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}



function submit_email(event) {
  event.preventDefault()
  // Post email to API route
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
    .then(response => { load_mailbox('sent') });
}

async function mailBox(mailbox) {
  await fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      emails.forEach(element => {
        var div = document.createElement('div');
        div.classList.add('mailviewdiv');
        div.setAttribute("data-id", element.id);
        div.setAttribute("onclick", "load_detailview(this,'" + mailbox + "')");
        if (!element.read)
          div.classList.add('graybg');
        div.innerHTML = `<div class="one">${element.sender}</div><div class="two">${element.subject}</div>
           <div class="timestamp">${element.timestamp}</div>`;
        document.querySelector('#emails-view').append(div);
      });
    });

}

function load_detailview(thisobj, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'block';
  viewemail(thisobj,mailbox);
}

function viewemail(evt, mailbox) {
  
  let mailid = evt.getAttribute("data-id");

  let actionbtn = '';
  if (mailbox != 'sent') {
    let replybtn = '';
    let actiontext = 'Archive';
    if (mailbox.toLowerCase() == 'archive'){
      actiontext = 'UnArchive';
    }
    if (mailbox.toLowerCase() == 'inbox'){
      replybtn = `<button id='mailaction_btn' class="btn btn-sm btn-outline-primary"
      onclick="reply(${mailid})">Reply</button>`;
    }
    actionbtn = `<div><p><button id='mailaction_btn' class="btn btn-sm btn-outline-primary"
    onclick="markarchiveaction(${mailid},'${actiontext}')">${actiontext}</button>${replybtn}</p></div>`;
  }

  fetch(`/emails/${mailid}`)
    .then(response => response.json())
    .then(element => {
      markmailasread(mailid);
      let div = document.createElement('div');
      div.classList.add('maildetailviewdiv');
      div.setAttribute("data-id", element.id);

      div.innerHTML = `<div><span><b>From: </b></span>${element.sender}</div>
        <div><span><b>To: </b></span> ${element.recipients}</div>
        <div><span><b>Subject: </b></span> ${element.subject}</div>
         <div><span><b>Timestamp: </b></span>${element.timestamp}</div>
         ${actionbtn}
         <hr/><p>${element.body}</p>
         </div>
        `;
      document.querySelector('#detail-view').style.display = 'block';
      document.querySelector('#detail-view').innerHTML = div.outerHTML;
    });
}

function markmailasread(mailid) {
  fetch(`/emails/${mailid}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function markarchiveaction(mailid,actionval) {
   let isarchive=false;
   if(actionval.toLowerCase()=='archive')
   isarchive=true;
  fetch(`/emails/${mailid}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: isarchive
    })
  }).then(()=>{
    load_mailbox('inbox');
  });
  
}

function reply(mailid){
  let newrecipient='';
  let newsubject='';
  let newbody='';
  fetch(`/emails/${mailid}`)
    .then(response => response.json())
    .then(element => {
      newrecipient=element.sender;
      newsubject=element.subject;
      if(!element.subject.startsWith("Re"))
      newsubject="Re: "+newsubject;
      newbody=`On ${element.timestamp} ${element.sender} wrote: ${element.body}`;
      compose_email(newrecipient,newsubject,newbody);
    });
}

