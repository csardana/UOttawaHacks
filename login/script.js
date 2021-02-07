$('.toggle').on('click', function() {
    $('.container').stop().addClass('active');
  });
  
  $('.close').on('click', function() {
    $('.container').stop().removeClass('active');
  });

function get_inputs(){
    var first_name = document.getElementById('#{label}')[0].value
    var Last_name = document.getElementById('#{label}')[1].value
    var DOB = document.getElementById('#{label}')[2]


      fetch(`/createNickname`)
          .then(function (response) {
              return response.text();
          }).then(function (text) {
              console.log('GET response text:');
              console.log(text);
          });
}
