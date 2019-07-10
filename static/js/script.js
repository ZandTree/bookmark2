
    $('.collection-modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var infoButton = button.data('bookmark');
        //console.log(infoButton);
        var modal = $(this);
        modal.find("input[type='hidden']").val(infoButton);
  })
    $('.collection-modal .btn-primary').on('click',function(e){
          e.preventDefault();
          var form = $(this).closest('.modal-content').find('form');
          // console.log("form is: ",form);
          var url = form.attr('action');
          var data = form.serialize()
          console.log(data);
          $.ajax({
              url:url,
              method:'GET',
              data:data,
              complete:function(jqxhr,textstatus){
                  console.log(textstatus);
                  $('.collection-modal').modal('hide');
              }
              // success:function(resp){
              //     console.log('YES')
              
          })
      })
