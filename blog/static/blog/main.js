<script>
      $(document).ready(function(){
          $("#loadmoreBtn").on('click',function(){
              var _currentResult=$(".blog-box").length;
              // Run Ajax
              $.ajax({
                  url:"{% url 'blog:load_more' %}",
                  type:'blog',
                  data:{
                      'offset':_currentResult,
                      'csrfmiddlewaretoken':"{{csrf_token}}"
                  },
                  dataType:'json',
                  beforeSend:function(){
                      $("#loadmoreBtn").addClass('disabled').text('Loading..');
                  },
                  success:function(res){
                      var _html='';
                      var json_data=$.parseJSON(res.blogs);
                      $.each(json_data,function(index,data){
                          _html+='<div class="card my-3 blog-box">\
              <h5 class="card-header">'+data.fields.title+'</h5>\
              <div class="card-body">\
                  <p class="card-text">'+data.fields.detail+'</p>\
                  <p>\
                      <a href="/update/'+data.fields.id+'" class="btn btn-success">Update</a>\
                      <a href="/delete/'+data.fields.id+'" class="btn btn-danger">Delete</a>\
                  </p>\
              </div>\
          </div>';
                      });
                      $(".blog-wrapper").append(_html);
                      var _countTotal=$(".blog-box").length;
                      if(_countTotal==res.totalResult){
                          $("#loadmoreBtn").remove();
                      }else{
                          $("#loadmoreBtn").removeClass('disabled').text('Load More');
                      }
                  }
              })
          })
      })
  </script>