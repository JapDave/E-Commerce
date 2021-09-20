$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type:"POST",
            url:"http://127.0.0.1:8000/enterprise/products/",
            data:{
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success:searchsuccess,
            datatype:'html'
        });
    });
});

function searchsuccess(data, textstatus, jqXHR)
{
    $('#search-results').html(data);
}