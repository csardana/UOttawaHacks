$('.toggle').on('click', function() {
    $('.container').stop().addClass('active');
  });
  
  $('.close').on('click', function() {
    $('.container').stop().removeClass('active');
  });

function get_inputs(){
    var first_name = document.getElementById('#{label}')[0];
    var Last_name = document.getElementById('#{label}')[1];
    var DOB = document.getElementById('#{label}')[2];
    var entry = {
    firstname : first_name.value
    lastname : Last_name.value
    dob : DOB.value
    };

      fetch(`${window.origin}/createNickname`,{
      method : "POST"
      credentials : "include"
      body : JSON.stringify(entry),
      cache : "no-cache",
      headers : new Headers({
      "content-type" : "application/json"})})
          .then(function (response) {
              return response.text();
          }).then(function (text) {
              console.log('GET response text:');
              console.log(text);
          });

}
