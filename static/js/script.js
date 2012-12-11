/* Script for CSCE 470 search engine
 *
 */

var movie_template = _.template($('#movie_template').html());
var result_template = _.template($('#result_template').html());
var alert_template = _.template($('#alert_template').html());

$('#moviesearch form').submit(function(ev) {
    var q = $(this).find('input[name=query]').val();
    ajax_search();
    return false;
});

$('#movie').click(function(ev) {
    var id = $(this).find('input[name=id]').val();
    ajax_getMovie(id);
    return false;
});

function submitForm() {
    $('#form').submit();
}


function ajax_search() {
  $.ajax('/search',{
      timeout:15000,
      success: function(data) {
        var movie_divs = _.map(data.movie, movie_template);
        var predictions_div = $('#predictions');
        predictions_div.append(movie_divs.join(''));
      },
      error: function(jqXHR,textStatus,errorThrown) {
        var error;
        if(textStatus=='error') {
          if(jqXHR.status==0)
            error = "Could not connect to server. Try running ./serve.py.";
          else
            error = jqXHR.status+" : "+errorThrown;
        } else {
          error = textStatus;
        }

        var alert = alert_template({error:error});
        $('#predictions form').after(alert);
        $('#predictions .results').hide();
      },
      dataType: 'json',
  });
}

function get_movie() {
    $.ajax('/get',{
       timeout:15000,
       success: function(data) {
       var movie_divs = _.map(data.result, movie_template);
       var predictions_div = $('#predictions')
       predictions_div.append(movie_divs.join(''));
       },
       error: function(jqXHR,textStatus,errorThrown) {
       var error;
       if(textStatus=='error') {
       if(jqXHR.status==0)
       error = "Could not connect to server. Try running ./serve.py.";
       else
       error = jqXHR.status+" : "+errorThrown;
       } else {
       error = textStatus;
       }
       
       var alert = alert_template({error:error});
       $('#predictions form').after(alert);
       $('#predictions .results').hide();
       },
       dataType: 'json',
    });
}

